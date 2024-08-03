from django.urls import path
from .views.home import Home
from .views.view_list import View_product
urlpatterns = [
    path('', Home.as_view() ,name='home'),
    path("Productos_listado/", View_product.as_view(), name="list_products")
    ]