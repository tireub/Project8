from django.urls import path

from . import views


urlpatterns = [
    path('', views.listing, name="listing"),
    path('search/', views.search, name="search"),
    path('<product_id>/', views.detail, name="detail"),

    ]