from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from .mixins import DictMixin
# Create your models here.

class Categoria(models.Model,DictMixin):
    nombre = models.CharField(max_length=50,unique=True)
    
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ["-id"]
class Ingrediente(models.Model,DictMixin):

    CHOICES_GRAMAJE = {
        "kilogramos":"kg"  ,
        "gramos" : "g",
        "mililitros":"ml"
    }
    nombre = models.CharField(max_length=50, unique=True,blank=False,null=False)
    cantidad_granel = models.DecimalField(max_digits=10, decimal_places=2,default=1000)
    cantidad = models.IntegerField(default=0)
    gramaje = models.CharField(choices=CHOICES_GRAMAJE)
    costo_granel_kg = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_insercion = models.DateTimeField(auto_now=True)

    def costo_granel(self):
        costo_Gramo = self.costo_granel_kg / self.cantidad_granel 
        return costo_Gramo

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        
        inventario, created = Inventario_materia.objects.get_or_create(stock_ingrediente=self)
        inventario.cantidad = self.cantidad
        inventario.cantidad_kg = self.cantidad_granel
        inventario.save()

    def delete(self,*args,**kwargs):
        Inventario_materia.objects.filter(stock_ingrediente=self).delete()
        super().delete(*args,**kwargs)
        
    def __str__(self) -> str:
        return self.nombre
    
class Receta(models.Model,DictMixin):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    ingredientes = models.ManyToManyField(Ingrediente, through="CantidadIngrediente")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def costo_receta(self):
        cantidades_ingredientes = CantidadIngrediente.objects.filter(receta=self)
        costo_total = sum(cantidad_ingrediente.costo_total() for cantidad_ingrediente in cantidades_ingredientes)
        return costo_total
    def __str__(self) -> str:
        return self.nombre+"_receta"

class CantidadIngrediente(models.Model,DictMixin):
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
    

class Producto(models.Model,DictMixin):
    nombre = models.CharField(max_length=70,unique=True)
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    porcentaje_ganancia = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    cantidad_en_stock = models.PositiveIntegerField(default=0) 
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @property
    def costo_venta(self):
        cantidades_ingredientes = CantidadIngrediente.objects.filter(receta=self.receta)
        costo_total = sum(cantidad_ingrediente.costo_total() for cantidad_ingrediente in cantidades_ingredientes)

        return costo_total
    
    @property
    def precio_venta_calculado(self):
        if self.precio_venta is not None:
                return self.precio_venta  # Retorna el precio de venta establecido por el usuario
        costo = self.costo_venta
        if costo > 0 and self.porcentaje_ganancia >= 0:
                # Calcula el precio de venta con el porcentaje de ganancia
            return costo * (1 + self.porcentaje_ganancia / 100)
        return 0
    # def margen_ganancia(self):
    #     return self.precio_venta - self.costo_venta()
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        
        inventario, created = Inventario_producto.objects.get_or_create(stock_producto=self)
        inventario.cantidad = self.cantidad_en_stock
        inventario.save()

    def delete(self,*args,**kwargs):
        Inventario_producto.objects.filter(stock_producto=self).delete()
        super().delete(*args,**kwargs)

    def __str__(self):
        return self.nombre
    

class Ingresos(models.Model,DictMixin):

    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    opciones = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    ingreso = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now().date()
        super(Ingresos, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.fecha} - {self.descripcion}: {self.cantidad}{self.opciones} costo:{self.ingreso}$"
    
    class Meta:
        verbose_name = 'Ingreso'
        verbose_name_plural = 'Ingresos'
        ordering = ["-id"]


class Gastos(models.Model,DictMixin):

    fecha = models.DateField(blank=True, null=True)
    descripcion = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2,default=1)
    opciones = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    gasto = models.DecimalField(max_digits=5, decimal_places=2)


    def save(self, *args, **kwargs):
        if not self.fecha:
            self.fecha = timezone.now().date()
        super(Gastos, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.fecha} - {self.descripcion}: {self.cantidad}{self.opciones} costo: {self.gasto}$"
    
    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ["-id"]


class Saldo(models.Model,DictMixin):
    fecha = models.DateField(auto_now=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    
        
    def __str__(self):
        return f"{self.fecha} - Saldo: {self.saldo}"
    
    class Meta:
        verbose_name = 'Saldo'
        verbose_name_plural = 'Saldos'
        ordering = ["-id"]


class Tienda(models.Model,DictMixin):
    nombre = models.CharField(max_length=50, unique=True)
    ubicacion = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre
    
class Inventario_producto(models.Model,DictMixin):
    stock_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    @property
    def total_almacen(self):
        return self.cantidad
    
    def __str__(self):
        return self.stock_producto.nombre +" "+ str(self.total_almacen)


class Inventario_materia(models.Model,DictMixin):
    stock_ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)
    cantidad_kg = models.PositiveIntegerField(default=0)
    @property
    def total_almacen(self):
        cantidad_kilos = self.cantidad * self.cantidad_kg
        return [self.cantidad , cantidad_kilos]
    
    def __str__(self):
        return f"Producto: {self.stock_ingrediente.nombre} Unidades: {self.total_almacen[0]} cantidad_kilos {self.total_almacen[1]}"


class Cliente(models.Model,DictMixin):
    nombre = models.CharField(max_length=50,unique=True)
    dni = models.IntegerField(
         validators=[
            MinValueValidator(10000000),  
            MaxValueValidator(99999999)  
        ],unique=True
    )
    apellidos = models.CharField(max_length=50)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Venta(models.Model,DictMixin):
    fecha = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Producto)
    client = models.ForeignKey(Cliente,  null=True, blank=True, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tienda,  null=True, blank=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        # Asegúrate de que al menos uno de `client` o `tienda` esté presente
        if not self.client and not self.tienda:
            raise ValidationError('Debe especificar al menos un cliente o una tienda para la venta.')
        
        if self.client and self.tienda:
            raise ValidationError('No se puede especificar tanto un cliente como una tienda en una sola venta.')
    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)    
# crear para que las clases devuelta a dictionario la informacion