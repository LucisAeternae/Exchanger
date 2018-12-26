from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    purchases = models.IntegerField(default=0)
    slug = models.SlugField()
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

class Category(models.Model):
    title = models.CharField(max_length=128)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    slug = models.SlugField()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
    class Meta():
        verbose_name_plural = "Categories"

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.SlugField()
    title = models.CharField(max_length=128)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Subcategory, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    username = models.CharField(unique=True, max_length=191)
    slug = models.SlugField()
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Profile, self).save(*args, **kwargs)

class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    description = models.TextField(default="", max_length=500)
    price = MoneyField(decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,)
    def __str__(self):
        return self.title
