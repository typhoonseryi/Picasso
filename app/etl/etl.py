import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from distutils.util import strtobool

from aiohttp import ClientSession, client_exceptions
from dotenv import load_dotenv

from parser import ParserLinks
from pg_saver import PostgresSaver

# Настройки логгера
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("ETL")

# Настройки БД
table = "domain"
schema = "id, url_name, domain, create_date, update_date, country, is_dead, a, ns, cname, mx, txt"
values = "%(id)s, %(url_name)s, %(domain)s, %(create_date)s, %(update_date)s, %(country)s, %(isDead)s," \
         " %(A)s, %(NS)s, %(CNAME)s, %(MX)s, %(TXT)s"

# URL API
api_url = "https://api.domainsdb.info/v1/domains/search"

# Загрузка переменных окружения
load_dotenv()
search_url = os.environ.get("SEARCH_URL")
pg_dsn = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST", "127.0.0.1"),
    "port": os.environ.get("DB_PORT", 5432),
}


def transform_data(data, found_url):
    """Метод перобразования данных для записи в БД"""
    domains = data.get("domains", None)
    if domains:
        for domain in domains:
            domain["id"] = str(uuid.uuid4())
            domain["url_name"] = found_url

            if domain["create_date"]:
                domain["create_date"] = datetime.fromisoformat(domain["create_date"])

            if domain["update_date"]:
                domain["update_date"] = datetime.fromisoformat(domain["update_date"])

            if domain["isDead"]:
                domain["isDead"] = bool(strtobool(domain["isDead"]))

            if domain["MX"] is not None:
                domain["MX"] = json.dumps(domain["MX"])
        return domains


async def get_api_response(found_url, session):
    """Асинхронный метод получения данных с API"""
    params = {"domain": found_url}
    try:
        async with session.get(api_url, params=params) as response:
            json_body = await response.json()
            domain_list = transform_data(json_body, found_url)
            return domain_list
    except client_exceptions.ContentTypeError as e:
        logger.warning(e)


async def bound_data_transfer(sem, url, session):
    """Асинхронный метод получения и записи данных в БД"""
    async with sem:
        data_to_save = await get_api_response(url, session)
        if data_to_save:
            pg_saver = PostgresSaver(pg_dsn)
            await pg_saver.save_batch_data(data_to_save, table, schema, values)


async def run(urls):
    """Асинхронный метод сбора и выполнения задач"""
    tasks = []
    sem = asyncio.Semaphore(100)
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(bound_data_transfer(sem, url, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = ParserLinks(search_url)
    parsed_urls = parser.parse_html()

    if parsed_urls:
        logger.debug(f"Links received")
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(run(parsed_urls))
        loop.run_until_complete(future)
        logger.debug("Domains saved")
    else:
        logger.debug("No links in search url")
