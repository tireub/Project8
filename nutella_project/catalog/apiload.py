import json
import MySQLdb
import requests
import unicodedata
import datetime


from .models import Category, Product, Store


def fillelement(link):
    resp = requests.get(link)
    for i in range(0, 19):
        element = resp.json()['products'][i]
        test = Db_product()
        test.jsonread(element)
        if test.name != '':
            test.add_aliment()



class Db_product:

    def __init__(self):
        self.name = ''
        self.picture = ''
        self.link = ''
        self.nutri_score = 6
        self.created_at = ''
        self.categories = []
        self.stores = []



    def jsonread(self, json_file):
        if 'product_name_fr' in json_file:
            self.name = json_file['product_name_fr'][:199]

        if 'code' in json_file:
            self.link = 'https://fr.openfoodfacts.org/produit/' + \
                        json_file['code']
        if 'nutrition_grade_fr' in json_file:
            if json_file['nutrition_grade_fr'] == 'a':
                self.nutri_score = 1
            elif json_file['nutrition_grade_fr'] == 'b':
                self.nutri_score = 2
            elif json_file['nutrition_grade_fr'] == 'c':
                self.nutri_score = 3
            elif json_file['nutrition_grade_fr'] == 'd':
                self.nutri_score = 4
            elif json_file['nutrition_grade_fr'] == 'e':
                self.nutri_score = 5
        if 'entry_dates_tags' in json_file:
            self.created_at = json_file['entry_dates_tags'][0]
        if 'stores' in json_file:
            self.stores = json_file['stores'].split(',')
            self.stores = list(map(str.lstrip, self.stores))
            tmp = []
            for store in self.stores:
                tmp.append(store[:39])
            self.stores = tmp
        if 'categories' in json_file:
            # Separate the categories into a list and nromalise the name
            self.categories = json_file['categories'].split(',')
            self.categories = list(map(str.lstrip, self.categories))
            tmp = []
            for cat in self.categories:
                tmp.append(cat[:39])
            self.categories = tmp
        if 'image_url' in json_file:
            self.picture = json_file['image_url']

    def add_aliment(self):
        if len(self.categories) != 0:
            if len(Product.objects.filter(name=self.name)) == 0:

                query = Product(name=self.name, picture=self.picture,
                                link=self.link, nutri_score=self.nutri_score,
                                created_at=self.created_at)
                query.save()

                self.add_categories(query)
                if len(self.stores) != 0 :
                    self.add_stores(query)


    def add_categories(self, product):
        for cat in self.categories:
            if len(Category.objects.filter(name = cat)) != 0 :
                c = Category.objects.get(name = cat)
                c.products.add(product.pk)

            else:
                query = Category(name = cat)
                query.save()
                c = Category.objects.get(name=cat)
                c.products.add(product.pk)

    def add_stores(self, product):
        for store in self.stores:
            if len(Store.objects.filter(name = store)) != 0 :
                c = Store.objects.get(name = store)
                c.products.add(product.pk)

            else:
                query = Store(name = store)
                query.save()
                c = Store.objects.get(name=store)
                c.products.add(product.pk)

def right_ns(product):
    score = product.nutri_score
    return ('catalog/img/icons/Score/nutriscore-'+score+'.svg')



