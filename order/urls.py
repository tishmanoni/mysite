from django.contrib import admin
from django.urls import path
from . import views

app_name= 'order'

urlpatterns = [
    path("", views.index, name="index"),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('shopcart/', views.shopcart, name='shopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
]
