from django.urls import path

from . import views


urlpatterns = [
    path('', views.listing, name="listing"),
    path('search/', views.search, name="search"),
    path('<product_id>/', views.detail, name="detail"),
    path('load', views.fill_db, name="fill_db" ),

    ]