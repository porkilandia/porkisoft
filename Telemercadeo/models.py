from django.db import models

# Create your models here.
class Cliente (models.Model):
    codigoCliente  = models.AutoField(primary_key=True, verbose_name='Codigo Cliente')
    nombreCliente = models.CharField(max_length=50)
    telefonoCliente = models.CharField(max_length=10,verbose_name='Telefono')
    direccionCliente = models.CharField(max_length=50,verbose_name='Direccion')

    def __unicode__(self):
        return self.nombreCliente