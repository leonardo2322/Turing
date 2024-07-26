from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from django.views.generic import TemplateView
# Create your views here.
# crear clases mixin
# def home(request):
#     return render(request,"base.html")
class Home(TemplateView):
    template_name = "base.html"

