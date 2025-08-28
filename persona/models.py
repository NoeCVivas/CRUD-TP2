from django.db import models

# Create your models here.
class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    oficina = models.ForeignKey('oficina.Oficina', on_delete=models.CASCADE, related_name='personas')

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.oficina} "