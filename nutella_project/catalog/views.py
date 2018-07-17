from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Product, Research
from django.shortcuts import redirect
from .forms import RegistrationForm
from django.contrib.auth import login

from .functions import search_product, search_substitute
from .apiload import fillelement


# Create your views here.
def index(request):
    context = {'title': 'Pur Beurre'}

    return render(request, 'catalog/index.html', context)


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

    context = {'products': list, 'paginate': True, 'title': 'Listing'}
    return render(request, 'catalog/list.html', context)


def search(request):

    query = request.GET.get('search')

    searched_product = search_product(query)

    [nbr, results] = search_substitute(searched_product)

    if nbr == 0:
        context = {'title': 'Aucun résultat'}
        return render(request, 'catalog/noresults.html', context)

    else:
        context = {'searched_product': searched_product, 'cat_nbr': nbr,
                   'cat1': results[0], 'products1': results[1],
                   'cat2': results[2], 'products2': results[3],
                   'cat3': results[4], 'products3': results[5],
                   'title': 'Substitution'
                   }
        return render(request, 'catalog/results.html', context)


def search_cat(request, cat):
    if cat == '':
        return render(request, 'catalog/noresults.html')

    else:
        products = Product.objects.filter(
            categories__name=cat).order_by('nutri_score')

        paginator = Paginator(products, 9)
        page = request.GET.get('page')

        try:
            list = paginator.page(page)
        except PageNotAnInteger:
            list = paginator.page(1)
        except EmptyPage:
            list = paginator.page(paginator.num_pages)

        context = {'products': list, 'paginate': True,
                   'name': cat, 'title': 'Catégorie'}
        return render(request, 'catalog/list.html', context)


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product_name': product.name,
        'product_score': product.nutri_score,
        'thumbnail': product.picture,
        'product_id': product.id,
        'categories': product.categories.all,
        'link': product.link,
        'title': 'Aliment'
    }
    return render(request, 'catalog/detail.html', context)


def fill_db(request):
    for a in range(3990, 4000):
        link = ('https://world.openfoodfacts.org/country/france/%d.json' % a)
        fillelement(link)

    product = get_object_or_404(Product, pk=1015)

    context = {
        'product_name': product.name,
        'product_score': product.nutri_score,
        'thumbnail': product.picture,
        'product_id': product.id,
    }
    return render(request, 'catalog/detail.html', context)


@login_required
def account(request):
    context = {'title': 'Compte'}
    return render(request, 'catalog/account.html', context)


def conditions(request):
    context = {'title': 'Mentions légales'}
    return render(request, 'catalog/conditions.html', context)


@login_required
def save(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user = request.user
    try:
        query = Research(contact=user, product=product)
        query.save()
    except IntegrityError:
        Research.objects.filter(contact=user, product=product).delete()

    return redirect('saved_products')


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

    context = {'products': list, 'paginate': True,
               'name': 'Produits sauvegardés',
               'title': 'Produits sauvegardés'}
    return render(request, 'catalog/list.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')
        else:
            form = RegistrationForm()

            args = {'form': form}
            return render(request, 'registration/new_account.html', args)

    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'registration/new_account.html', args)
