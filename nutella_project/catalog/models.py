from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    picture = models.URLField()
    link = models.URLField()
    nutri_score = models.IntegerField()
    created_at = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=20, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Research(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.contact.name


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=200)
    products = models.ManyToManyField(Product, related_name='stores', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name

