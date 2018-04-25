from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from .models import Category, Product, Contact, Research

# Create your views here.
def index(request):

    return render(request, 'catalog/index.html')

def listing(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/list.html', context)

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

    name = "Résultats pour la requète %s"%query
    context = {
        'products': products,
        'name': name

    }
    return render(request, 'catalog/search.html', context)

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    message = "Le nom du produit est {}.".format(product.name)
    context = {
        'product_name': product.name,
        'product_score': product.nutri_score,
        'thumbnail': product.picture,
        'product_id': product.id,
    }
    return render(request, 'catalog/detail.html', context)

