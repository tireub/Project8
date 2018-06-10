from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField('Nom', max_length=200, unique=True)
    picture = models.URLField('Image')
    link = models.URLField('Lien')
    nutri_score = models.IntegerField('Score Nutritionnel')
    created_at = models.DateField('Date de création')
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Produit"


class Contact(models.Model):
    name = models.CharField('Nom', max_length=40, unique=True)
    email = models.EmailField('Adresse Mail' ,max_length=100, unique=True)
    password = models.CharField('Mot de Passe', max_length=20, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.name



class Research(models.Model):

    contact = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.product.name
    class Meta:
        verbose_name = "Réservation"

class Category(models.Model):
    name = models.CharField('Nom', max_length=200, unique=True)
    products = models.ManyToManyField(Product, related_name='categories', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Catégorie"


class Store(models.Model):
    name = models.CharField('Nom', max_length=200)
    products = models.ManyToManyField(Product, related_name='stores', blank=True)
    objects = models.Manager()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Magasin"

