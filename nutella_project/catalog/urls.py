from django.urls import path

from . import views


urlpatterns = [
    path('', views.listing, name="listing"),
    path('search/<cat>/', views.search_cat, name="search_cat"),
    path('search/', views.search, name="search"),

    path('<product_id>/', views.detail, name="detail"),
    path('load', views.fill_db, name="fill_db" ),
    path('account', views.account, name="account"),
    path('save/<product_id>/', views.save, name="save"),
    path('saved_products', views.saved_products, name="saved_products"),
    path('conditions', views.conditions, name="conditions"),


    ]