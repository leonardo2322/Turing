from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
# Create your views here.
# crear clases mixin
# def home(request):
#     return render(request,"base.html")

class Producto(View):
    def get(self,request,*args):
        return render(request, "base.html")