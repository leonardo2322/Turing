from django.contrib import admin
from .models import Ingrediente, Receta, CantidadIngrediente, Producto, Gastos, Ingresos,  Saldo, Categoria,Tienda, Inventario_producto,Inventario_materia
# Register your models here.
admin.site.register(Ingrediente)
admin.site.register(Receta)
admin.site.register(CantidadIngrediente)
admin.site.register(Producto)
admin.site.register(Gastos)
admin.site.register(Ingresos)
admin.site.register(Saldo)
admin.site.register(Categoria)
admin.site.register(Tienda)
admin.site.register(Inventario_producto)
admin.site.register(Inventario_materia)