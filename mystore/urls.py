from django.contrib import admin
from django.urls import path
from . import views

app_name= 'mystore'

urlpatterns = [
   
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),
    path('store', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('colors/', views.colors, name='colors'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
   
]
