from django.db import models

# Create your models here.
class Oficina(models.Model):
    nombre = models.CharField(max_length=100)
    nombre_corto = models.CharField(max_length=10)
    
    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'
        constraints = [
            models.UniqueConstraint(fields=['nombre'], name='unique_nombre_oficina'),
            models.UniqueConstraint(fields=['nombre_corto'], name='unique_nombre_corto_oficina'),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.nombre_corto}"