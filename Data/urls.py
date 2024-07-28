from django.urls import path
from .views.home import Home
from .views.view_list import View_product
urlpatterns = [
    path('', Home.as_view() ,name='home'),
    path("list_view/", View_product.as_view(), name="list")
    ]