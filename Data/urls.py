from django.urls import path
from .views import *

urlpatterns = [
    path('', Producto.as_view() ,name='home'),

    
    ]