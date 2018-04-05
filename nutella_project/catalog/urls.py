from django.urls import path

from . import views


urlpatterns = [
    path('', views.listing),
    path('search/', views.search)

    ]