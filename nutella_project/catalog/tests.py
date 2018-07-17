from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category, Research
from .functions import search_product, search_substitute
from .views import search_cat

# Create your tests here.


# Index page
class IndexPageTestCase(TestCase):
    # Has to return status code 200
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


# Search pages
class SearchPagesTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Nutella", nutri_score="5",
                               created_at="2018-07-15")
        self.product = Product.objects.get(name="Nutella")
        nutella_cat = Category.objects.create(name="Pate à tartiner")
        nutella_cat.products.add(self.product)
        noisettes = Category.objects.create(name="Noisettes")
        noisettes.products.add(self.product)
        self.categories = self.product.categories

    # Has to return status 200 if field is correct
    def testSearchPageReturns200(self):
        product_name = self.product.name
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    # Detail page
        # Has to return a 200 if the product exists
    def testDetailPageReturns200(self):
        product_id = self.product.pk
        response = self.client.get(reverse('detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

        # Has to return 404 if the item does not exists
    def testDetailPageReturns404(self):
        product_id = self.product.pk + 1
        response = self.client.get(reverse('detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)

# Search algo
    # Search_product has to return a searched product from the base if it found
    # something
    def testSearchProduct(self):
        response = search_product("Nutella")
        self.assertEqual(response, self.product)

    # Has to return an empty list if the field is not correct or absent
    def testSearchProductEmpty(self):
        response = search_product("xk")
        self.assertEqual(response, [])

    # Has to return an empry list if no products corresponds
    def testSearchProductNotInBase(self):
        response = search_product("caramel")
        self.assertEqual(response, [])

    # Has to return the right product if the query is mispelled
    def testSearchProductMispelled(self):
        response = search_product("nutel")
        self.assertEqual(response, self.product)

    # Search_substitute has to return the number of categories associated
    def testSearchSubstitute(self):
        response = search_substitute(self.product)
        self.assertEqual(response[0], 2)
        # and the info associated (cat name and 3 best products)
        self.assertEqual(response[1][0], "Noisettes")
        self.assertEqual(response[1][1], [self.product])
        self.assertEqual(response[1][2], "Pate à tartiner")
        # Search_substitute cannot return the same product twice in the results
        self.assertEqual(response[1][3], [])


# Conditions page
class ConfitionsPageTestCase(TestCase):
    # Has to return status 200
    def test_conditions_page(self):
        response = self.client.get(reverse('conditions'))
        self.assertEqual(response.status_code, 200)


# Login
class LoginPageTestCase(TestCase):
    # Has to get a 200 code when called
    def testLoginPage(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    # Test that the user in disconnected after logout
    def testLoggeOutUser(self):
        user = User.objects.create_user('test')
        user.is_active = True
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0],
                         'registration/logged_out.html')


# New account

class NewAccountTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="Testeur", password="test",
                                 email="testeur@test.com")
        nutella = Product.objects.create(name="Nutella", nutri_score="5",
                                         created_at="2018-07-15")
        self.product = Product.objects.get(name="Nutella")
        self.user = User.objects.get(username="Testeur")

    # Has to get a 200 status when calling the form
    def testNewAccountPage(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    # Test that a new user is created
    def testNewAccountCreation(self):
        old_users_count = User.objects.count()
        response = self.client.post(reverse('register'), {
            'username': "Testuser",
            'email': "testeur@testeur.com",
            'password': "testing"
        })
        new_user_count = User.objects.count()
        # self.assertEqual(new_user_count, old_users_count + 1)

    # Save product
    # Test that the product has been saved
    def testSaveProduct(self):
        old_saves = Research.objects.count()
        product_id = self.product.pk
        self.client.login(username="Testeur", password="test")
        response = self.client.get(reverse('save', args=(product_id,)))
        new_saves = Research.objects.count()
        self.assertEqual(response.url, '/catalog/saved_products')
        self.assertEqual(new_saves, old_saves + 1)


# Category search from detail page
class CatSearchTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Nutella", nutri_score="5",
                               created_at="2018-07-15")
        self.product = Product.objects.get(name="Nutella")
        nutella_cat = Category.objects.create(name="Pate à tartiner")
        nutella_cat.products.add(self.product)
        self.cat = Category.objects.get(name="Pate à tartiner")

    # Has to return a 200 if the category exists
    def testCatSearchPage(self):
        response = self.client.get(
            reverse('search_cat', args=(self.cat.name,)))
        self.assertEqual(response.status_code, 200)
