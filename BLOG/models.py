from django.db import models
from django.utils.text import slugify


class Article(models.Model):
    title = models.CharField(max_length=30, help_text='the title of the article')
    author = models.CharField(max_length=30, help_text='the author of the article')
    content = models.TextField(help_text='the content of the article')
    description = models.TextField(blank=True, help_text='the description of the article')
    published_date = models.DateTimeField()
    category = models.CharField(max_length=30,help_text='the category of the article')
    label = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def slug_save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
