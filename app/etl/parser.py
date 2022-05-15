import requests
from bs4 import BeautifulSoup


class ParserLinks:
    """Класс парсинга ссылок с произвольной web-страницы"""

    def __init__(self, url):
        self.url = url

    def get_html(self):
        """Метод загрузки html web-страницы"""
        response = requests.get(self.url)
        return response.content

    def parse_html(self):
        """Метод получения кортежа найденных ссылок без дубликатов"""
        html = self.get_html()
        soup = BeautifulSoup(html, "lxml")
        return tuple(
            set(link["href"] for link in soup.find_all("a") if link.get("href"))
        )
