from django.contrib import admin
from .models import Ingrediente, Receta, CantidadIngrediente, Producto
# Register your models here.
admin.site.register(Ingrediente)
admin.site.register(Receta)
admin.site.register(CantidadIngrediente)
admin.site.register(Producto)

