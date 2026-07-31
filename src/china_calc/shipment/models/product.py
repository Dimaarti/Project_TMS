from django.db import models

from config.models import BaseModel


class Product(BaseModel):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    article = models.CharField(max_length=60, blank=True, verbose_name="Артикул")
    link = models.URLField(max_length=100, blank=True, verbose_name="Ссылка")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        ordering = ["name"]
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name
