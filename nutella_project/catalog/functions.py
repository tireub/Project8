from .models import Product
from operator import attrgetter


def search_product(query):
    # Find the closest product in the database related to the request

    # If empty field, return smthing
    if not query:
        return []

    # If text in the search field
    else:
        if Product.objects.filter(name=query):
            searched_product = Product.objects.filter(name=query)[0]
        else:
            # Get all the products with the name starting with the query
            products = Product.objects.filter(
                name__istartswith=query).order_by('name')
            if products:
                length = 300
                for product in products:
                    name = product.name
                    if len(name) < length:
                        searched_name = name
                        length = len(name)

                searched_product = Product.objects.filter(
                    name=searched_name)[0]
            else:
                products = Product.objects.filter(name__icontains=query)
                if products:
                    length = 300
                    for product in products:
                        name = product.name
                        if len(name) < length:
                            searched_name = name
                            length = len(name)

                    searched_product = Product.objects.filter(
                        name=searched_name)[0]

                else:
                    searched_product = []

    return searched_product


def search_substitute(product):
    # Get nbr of categories associated to product
    results = []
    nbr = 0
    cat1 = ''
    cat2 = ''
    cat3 = ''
    products1 = []
    products2 = []
    products3 = []

    if product != []:
        for cat in product.categories.all():
            nbr = nbr+1

        # Get categories of product (ordered from precise to general)
        if nbr >= 1:
            # Smallest category :
            cat1 = product.categories.all()[nbr-1].id

            # Find 3 best products in this category (eject redundancies)
            products = Product.objects.filter(
                categories__id=cat1).order_by('nutri_score')
            elem_num = 0
            products1 = []
            for prod in products:
                if prod not in products1:
                    products1.append(prod)
                    elem_num = elem_num + 1
                    if elem_num == 3:
                        break

            # Switch to category name to send back to the view
            cat1 = product.categories.all()[nbr-1].name

            if nbr >= 2:
                # Repeat for other 2
                cat2 = product.categories.all()[nbr-2].id

                # Find 3 best products in this category (eject redundancies)
                products = Product.objects.filter(
                    categories__id=cat2).order_by('nutri_score')
                elem_num = 0
                products2 = []
                for prod in products:
                    if prod not in products1:
                        if prod not in products2:
                            products2.append(prod)
                            elem_num = elem_num + 1
                            if elem_num == 3:
                                break
                # Switch to category name to send back to the view
                cat2 = product.categories.all()[nbr-2].name

                if nbr >= 3:
                    cat3 = product.categories.all()[nbr-3].id

                    # Find 3 best products in this category
                    # (eject redundancies)
                    products = Product.objects.filter(
                        categories__id=cat3).order_by('nutri_score')
                    elem_num = 0
                    products3 = []
                    for prod in products:
                        if prod not in products1:
                            if prod not in products2:
                                if prod not in products3:
                                    products3.append(prod)
                                    elem_num = elem_num + 1
                                    if elem_num == 3:
                                        break
                    # Switch to category name to send back to the view
                    cat3 = product.categories.all()[nbr-3].name

    results.extend([cat1, products1, cat2, products2, cat3, products3])
    # Return categories names and associated products
    return (nbr, results)
