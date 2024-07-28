from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = "base.html"