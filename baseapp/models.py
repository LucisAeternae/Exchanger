from django.db import models
from djmoney.models.fields import MoneyField
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    purchases = models.IntegerField(default=0)
    slug = models.SlugField()
    description = models.TextField(default='', max_length=500)
    logo = models.ImageField(upload_to='images/', blank=True)
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
        verbose_name_plural = 'Categories'

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    slug = models.SlugField()
    title = models.CharField(max_length=128)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Subcategory, self).save(*args, **kwargs)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, default=" ")

def user_directory_path(instance, filename):
    return 'profile_images/user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    username = models.CharField(unique=True, max_length=191)
    avatar = models.ImageField(upload_to=user_directory_path, blank=True,
                               default='profile_images/noimage.png')
    money = MoneyField(decimal_places=2,
            default=0,
            default_currency='USD',
            max_digits=11)
    slug = models.SlugField()
    def __str__(self):
        return self.username
    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        if not self.username:
            self.username = self.user.username
        super(Profile, self).save(*args, **kwargs)


class Offer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    description = models.TextField(default="", max_length=500)
    OFFER_TYPE_CHOICES = (
        ['Base', 'Base'],
        ['Custom', 'Custom']
    )
    type = models.CharField(default='Base', choices=OFFER_TYPE_CHOICES, max_length=10)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                  MaxValueValidator(10000)])
    datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    datetimemodified = models.DateTimeField(auto_now=True, blank=True, null=True)
    rangestep = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                  MaxValueValidator(100)])
    active = models.BooleanField(default=True)
    price = MoneyField(decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,)
    def __str__(self):
        return self.title

class Purchases(models.Model):
    customer = models.ForeignKey(Profile, on_delete=models.PROTECT)
    offer_title = models.CharField(max_length=200)
    offer_seller = models.CharField(unique=True, max_length=191)
    offer_price = MoneyField(decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,)
    offer_type = models.CharField(default='Base', max_length=10)
    purchase_quantity = models.IntegerField(default=1, validators=[MinValueValidator(1),
                                  MaxValueValidator(10000)])
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.offer_title
