from datetime import *

from django import forms
from django.forms import ModelForm

from Fabricacion.models import *
from Inventario.models import *
from  Nomina.models import *


class ProvedorForm(ModelForm):
    class Meta:
        model= Proveedor

class ProductoForm(ModelForm):
    class Meta:
        model = Producto

class SubProductoForm(ModelForm):
    class Meta:
        model = SubProducto

class DetSubProductoForm(ModelForm):

    class Meta:
        model = DetalleSubProducto

class BodegaForm(ModelForm):
    class Meta:
        model = Bodega

class ProductoBodegaForm(ModelForm):
    class Meta:
        model = ProductoBodega

class GanadoForm(ModelForm):
    class Meta:
        model = Ganado

class CompraForm(ModelForm):
    class Meta:
        model = Compra

class DetalleCompraForm(ModelForm):
    class Meta:
        model = DetalleCompra

class DesposteForm(ModelForm):
    class Meta:
        model = PlanillaDesposte

class CanalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CanalForm,self).__init__(*args, **kwargs)

        if (PlanillaDesposte.objects.all()):
            self.fields['planilla'].queryset = PlanillaDesposte.objects.filter(fechaDesposte = datetime.today())

    class Meta:
        model=Canal

class DetalleDesposteForm(ModelForm):
    class Meta:
        model = DetallePlanilla

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado

class CargoForm(ModelForm):
    class Meta:
        model = Cargo

class TrasladoForm(ModelForm):
    bodegaDestino = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=True)
    class Meta:
        model = Traslado

class DetalleTrasladoForm(ModelForm):
    class Meta:
        model = DetalleTraslado
