from django.conf.urls import patterns, url

from Inventario.views import *


urlpatterns = patterns('',
    # Examples:
    url(r'^home/$',home),
    url(r'^listaProd/$', listaProductos),
    url(r'^verSubProductos/$',listaSubProductos),
    url(r'^bodega/$',GestionBodega),
    url(r'^provedor/$',GestionProvedor),
    url(r'^ganado/(?P<idcompra>\d+)',GestionGanado),
    url(r'^compra/$',GestionCompra),

    url(r'^recepcion/(?P<idcompra>\d+)',GestionPlanillaRecepcion),
    url(r'^canal/(?P<idrecepcion>\d+)',GestionCanal),
    url(r'^marcarcanal/(?P<idcanal>\d+)',MarcarCanalDesposte),

    url(r'^sacrificio/(?P<idrecepcion>\d+)',GestionSacrificio),

    url(r'^desposte/$',GestionDesposte),
    url(r'^traslado/$',GestionTraslados),
    url(r'^dettraslado/(?P<idtraslado>\d+)',GestionDetalleTraslado),
    url(r'^cargo/$',GestionCargos),
    url(r'^detalleDesposte/(?P<idplanilla>\d+)',GestionCanalDetalleDesposte),
    url(r'^costoDesposte/(?P<idplanilla>\d+)',CostoDesposte),

    url(r'^ensalinados/(?P<idproducto>\d+)', GestionEnsalinado),
    url(r'^verduras/(?P<idDetcompra>\d+)', GestionVerduras),
    url(r'^condimento/$', GestionCondimento),
    url(r'^detallecondimento/(?P<idcondimento>\d+)', GestionDetalleCondimento),
    url(r'^costoCond/(?P<idcondimento>\d+)',CostoCondimento),


    url(r'^empleado/$',GestionEmpleados),
    url(r'^detcompra/(?P<idcompra>\d+)',GestionDetalleCompra),
    url(r'^productoBodega/(?P<idproducto>\d+)',GestionProductoBodega),
    url(r'^addDSprod/(?P<id_subproducto>\d+)',AgregarDetSubProducto, name='gestionSp'),
    url(r'^borrar/(?P<id_producto>\d+)',borrar_producto),
    url(r'^borrarSP/(?P<idSubproducto>\d+)',borrarSubproducto),
    url(r'^borrardetSP/(?P<idDetalle>\d+)',borrarDetalleSp),
    url(r'^borrarBodega/(?P<idbodega>\d+)',borrarBodega),
    url(r'^editar/(?P<id_producto>\d+)',editar_producto),
    url(r'^editarBodega/(?P<idBodega>\d+)',editarBodega),
    url(r'^editarSP/(?P<idSproducto>\d+)',editarSubproducto),


)