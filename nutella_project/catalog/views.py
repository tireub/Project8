from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Category, Product, Contact, Research


from .apiload import fillelement, Db_product


# Create your views here.
def index(request):

    return render(request, 'catalog/index.html')

def listing(request):
    products = Product.objects.all()
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {'products': list, 'paginate': True}
    return render(request, 'catalog/list.html', context)

def search(request):

    query = request.GET.get('search')


    if not query:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            categories__name__icontains=query).order_by('nutri_score')

    if not products.exists():
        products = Product.objects.filter(
            name__icontains=query).order_by('nutri_score')


    paginator = Paginator(products, 9)
    page = request.GET.get('page')

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {'products': list, 'paginate': True, 'name': query}
    return render(request, 'catalog/list.html', context)

def search_cat(request, cat):
    products = Product.objects.filter(
        categories__name__icontains=cat).order_by('nutri_score')

    if not products.exists():
        products = Product.objects.filter(
            name__icontains=cat).order_by('nutri_score')

    paginator = Paginator(products, 9)
    page = request.GET.get('page')

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {'products': list, 'paginate': True, 'name': cat}
    return render(request, 'catalog/list.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    message = "Le nom du produit est {}.".format(product.name)
    context = {
        'product_name': product.name,
        'product_score': product.nutri_score,
        'thumbnail': product.picture,
        'product_id': product.id,
        'categories': product.categories.all,
        'link': product.link,
    }
    return render(request, 'catalog/detail.html', context)


def fill_db(request):
    for a in range(3990,4000):
        link = ('https://world.openfoodfacts.org/country/france/%d.json' % a)
        fillelement(link)

    product = get_object_or_404(Product, pk=1015)
    message = "Le nom du produit est {}.".format(product.name)
    context = {
        'product_name': product.name,
        'product_score': product.nutri_score,
        'thumbnail': product.picture,
        'product_id': product.id,
    }
    return render(request, 'catalog/detail.html', context)

@login_required
def account(request):
    return render(request, 'catalog/account.html')

def conditions(request):
    return render(request, 'catalog/conditions.html')

@login_required
def save(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    try:
        query = Research(contact=user, product=product)
        query.save()
    except IntegrityError:
        Research.objects.filter(contact=user, product=product).delete()

    products = Product.objects.filter(
        research__contact=user)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {'products': list, 'paginate': True,
               'name': "Produits sauvegardés"}
    return render(request, 'catalog/list.html', context)

@login_required
def saved_products(request):
    user = request.user
    products = Product.objects.filter(
        research__contact=user)


    paginator = Paginator(products, 9)
    page = request.GET.get('page')

    try:
        list = paginator.page(page)
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)

    context = {'products': list, 'paginate': True, 'name': "Produits sauvegardés"}
    return render(request, 'catalog/list.html', context)


