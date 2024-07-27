from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Ingresos, Gastos, Saldo
from django.db import models

@receiver(post_save, sender=Ingresos)
@receiver(post_save, sender=Gastos)
@receiver(post_delete, sender=Ingresos)
@receiver(post_delete, sender=Gastos)
def actualizar_saldo(sender, instance, **kwargs):
    fecha_actual = timezone.now().date()
    ingresos_total = Ingresos.objects.aggregate(total=models.Sum('ingreso'))['total'] or 0
    gastos_total = Gastos.objects.aggregate(total=models.Sum('gasto'))['total'] or 0
    saldo_total = ingresos_total - gastos_total
    
    saldo, created = Saldo.objects.get_or_create(fecha=fecha_actual)
    saldo.saldo = saldo_total
    saldo.save()

