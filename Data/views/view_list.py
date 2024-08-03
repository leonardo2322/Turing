from django.shortcuts import render
from django.views.generic import View,ListView
from django.http import JsonResponse
from django.views.generic import TemplateView
from ..models import Producto



class View_product(ListView):
    model = Producto
    template_name = "Data_templates/list_view.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Listado De Productos"
        return context