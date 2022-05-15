import uuid

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("url_name", models.CharField(max_length=2048)),
                ("domain", models.CharField(max_length=1024)),
                ("create_date", models.DateTimeField(null=True)),
                ("update_date", models.DateTimeField(null=True)),
                ("country", models.CharField(max_length=255, null=True)),
                ("is_dead", models.BooleanField()),
                (
                    "a",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "ns",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        null=True,
                        size=None,
                    ),
                ),
                (
                    "cname",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        null=True,
                        size=None,
                    ),
                ),
                ("mx", models.JSONField(null=True)),
                (
                    "txt",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=255),
                        null=True,
                        size=None,
                    ),
                ),
            ],
            options={
                "db_table": "domain",
            },
        ),
        migrations.AddConstraint(
            model_name="domain",
            constraint=models.UniqueConstraint(
                fields=("url_name", "domain"), name="url_domain_idx"
            ),
        ),
    ]
