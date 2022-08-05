from unicodedata import name
from django import urls
from django.urls import URLPattern, path
#from django.conf.urls import url

 #  bring in all view from views.py
from . import views             

#define url parterm
urlpatterns = [
    path('', views.home,  name='home'),                       
    path('product', views.product,  name='product'),                  
    path('getProduct/', views.getProduct, name='getProduct'),  
    path('getSelectedProduct/', views.getSelectedProduct, name='getSelectedProduct'),  
    path('addProduct/', views.addProduct, name='addProduct'),  
    path('deleteProduct/', views.deleteProduct, name='deleteProduct'),  

]   
