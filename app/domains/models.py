import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models


class Domain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url_name = models.CharField(max_length=2048)
    domain = models.CharField(max_length=1024)
    create_date = models.DateTimeField(null=True)
    update_date = models.DateTimeField(null=True)
    country = models.CharField(max_length=255, null=True)
    is_dead = models.BooleanField()
    a = ArrayField(models.CharField(max_length=255), null=True)
    ns = ArrayField(models.CharField(max_length=255), null=True)
    cname = ArrayField(models.CharField(max_length=255), null=True)
    mx = models.JSONField(null=True)
    txt = ArrayField(models.CharField(max_length=255), null=True)

    class Meta:
        db_table = "domain"
        constraints = [
            models.UniqueConstraint(
                fields=["url_name", "domain"], name="url_domain_idx"
            ),
        ]
