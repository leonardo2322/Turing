from django.db import models

# Create your models here.
class Ingrediente(models.Model):

    CHOICES_GRAMAJE = {
        "kilogramos":"kg"  ,
        "gramos" : "g",
        "mililitros":"ml"
    }
    nombre = models.CharField(max_length=50, unique=True,blank=False,null=False)
    cantidad_granel = models.DecimalField(max_digits=10, decimal_places=2,default=1000)
    gramaje = models.CharField(choices=CHOICES_GRAMAJE)
    costo_granel_kg = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_insercion = models.DateTimeField(auto_now=True)

    def costo_granel(self):
        costo_Gramo = self.costo_granel_kg / self.cantidad_granel 
        return costo_Gramo
    def __str__(self) -> str:
        return self.nombre
    
class Receta(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    ingredientes = models.ManyToManyField(Ingrediente, through="CantidadIngrediente")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def costo_receta(self):
        cantidades_ingredientes = CantidadIngrediente.objects.filter(receta=self)
        costo_total = sum(cantidad_ingrediente.costo_total() for cantidad_ingrediente in cantidades_ingredientes)
        return costo_total
    def __str__(self) -> str:
        return self.nombre

class CantidadIngrediente(models.Model):
    CHOICES_GRAMAJE = {
        "kilogramos":"kg"  ,
        "gramos" : "g",
        "mililitros":"ml"
    }
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    gramaje_cant = models.CharField(choices=CHOICES_GRAMAJE,null=True, blank=True)
    def costo_total(self):
        costo_ingrediente = self.ingrediente.costo_granel()
        costo_total_gramo = costo_ingrediente * self.cantidad / 1000
        return costo_total_gramo
  

    def __str__(self):
       
        return f"para la receta:{self.receta.nombre} ingrdiente: {self.ingrediente.nombre} la cant: {str(self.cantidad)}{self.gramaje_cant} costo x Ing:{self.costo_total()} "
    


class Producto(models.Model):
    nombre = models.CharField(max_length=70,unique=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    # precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    porcentaje_ganancia = models.IntegerField()
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def costo_venta(self):
        cantidades_ingredientes = CantidadIngrediente.objects.filter(receta=self.receta)
        costo_total = sum(cantidad_ingrediente.costo_total() for cantidad_ingrediente in cantidades_ingredientes)

        return costo_total

    # def margen_ganancia(self):
    #     return self.precio_venta - self.costo_venta()

    def __str__(self):
        return f"{self.nombre} total Producto: {str(self.costo_venta())}"