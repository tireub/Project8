#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Category, Product, Contact, Research

# Create your views here.
def index(request):
    products = Product.objects.filter(nutri_score=5).order_by('-created_at')[:12]

    formatted_products = ["<li>{}</li>".format(product.name) for product in products]
    message = """<ul>{}</ul>""".format("\n".join(formatted_products))
    template = loader.get_template('catalog/index.html')
    return HttpResponse(template.render(request=request))

def listing(request):
    products = Product.objects.all()
    formatted_products = ["<li>{}</li>".format(product.name) for product in products]
    message = """<ul>{}</ul>""".format("\n".join(formatted_products))
    return HttpResponse(message)

def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all()
    else:
            products = Product.objects.filter(name__icontains=query)

    if not products.exists():
        message = "Misère, on a rien !"
    else:
        products = ["<li>{}</li>".format(product.name) for product in products]
        message = """
            Nous avons trouvé les produits correspondants : 
            <ul>{}</ul>""".format("".join(products))

    return HttpResponse(message)

