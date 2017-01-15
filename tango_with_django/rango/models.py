from django.db import models
from django.template.defaultfilters import slugify

MAX_LENGTH_128 = 128
MAX_LENGTH_200 = 200


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_128, unique=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True)  # blank=True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=MAX_LENGTH_128)
    url = models.URLField(max_length=MAX_LENGTH_200)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
