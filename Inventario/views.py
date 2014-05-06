from decimal import Decimal

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext

from Inventario.Forms.forms import *
from Inventario.models import *






# Create your views here.

def home(request):
    return render_to_response('Home.html',{},context_instance = RequestContext(request))

#***************************************PRODUCTOS******************************************

def listaProductos(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    #Creacion de producto en cada bodega con valor inicial


    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            producto = Producto.objects.get(nombreProducto = request.POST.get('nombreProducto'))

            for bod in Bodega.objects.all():

                bodegaInicial = ProductoBodega()
                bodega = Bodega.objects.get(pk = bod.codigoBodega)

                bodegaInicial.producto = producto
                bodegaInicial.bodega = bodega
                bodegaInicial.pesoProductoStock = 0
                bodegaInicial.unidadesStock = 0
                bodegaInicial.save()


            return HttpResponseRedirect('/listaProd')
    else:
        formulario =ProductoForm()

    return render_to_response('Inventario/GestionProducto.html',{'formulario':formulario,'productos':productos },
                              context_instance = RequestContext(request))

def borrar_producto(request, id_producto):
    producto = Producto.objects.get(pk=id_producto)
    producto.delete()
    return  HttpResponseRedirect('/listaProd')

def editar_producto(request, id_producto):
    productos = Producto.objects.all().order_by('nombreProducto')
    producto = Producto.objects.get(pk=id_producto)
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/listaProd')
    else:
        formulario = ProductoForm(instance=producto)
    return  render_to_response('Inventario/GestionProducto.html',{'formulario':formulario,'productos':productos },
                               context_instance = RequestContext(request))

#******************************************************************************************
#***********************************SUBPRODUCTOS*******************************************

def listaSubProductos(request):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    if request.method == 'POST':

        formulario = SubProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/verSubProductos/')
    else:
        formulario =SubProductoForm()

    return render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos },
                              context_instance = RequestContext(request))


def borrarSubproducto(request, idSubproducto):
    subproducto = SubProducto.objects.get(pk=idSubproducto)
    subproducto.delete()

    return  HttpResponseRedirect('/verSubProductos')

def editarSubproducto(request, idSproducto):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    sproducto = SubProducto.objects.get(pk=idSproducto)
    if request.method == 'POST':
        formulario = SubProductoForm(request.POST, instance=sproducto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/verSubProductos')
    else:
        formulario = SubProductoForm(instance=sproducto)

    return  render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos},
                               context_instance = RequestContext(request))

def AgregarDetSubProducto(request,id_subproducto):

    subrpoductos = SubProducto.objects.get(pk = id_subproducto)
    desubproductos = DetalleSubProducto.objects.filter(subproducto = id_subproducto)

    detSubp = DetalleSubProducto.objects.all()
    totalPeso = 0
    totalUnd = 0

    for dts in detSubp: # clacular los totales de la lista de detalles de subproducto
        totalPeso += dts.pesoUnitProducto
        totalUnd += dts.unidades

    if request.method == 'POST':
        formulario = DetSubProductoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/addDSprod/'+ id_subproducto)
    else:
        formulario = DetSubProductoForm(initial={'subproducto':id_subproducto})

    return render_to_response('Inventario/GestionDetalleSubProducto.html',{'Tunds':totalUnd,'TPeso':totalPeso,'formulario':formulario,
                                                         'subrpoductos': subrpoductos,
                                                         'desubproductos': desubproductos},
                                                        context_instance = RequestContext(request))

def borrarDetalleSp(request, idDetalle):
    detsubproducto = DetalleSubProducto.objects.get(pk=idDetalle)
    detsubproducto.delete()
    return  HttpResponseRedirect('/verSubProductos')

#**************************************BODEGA****************************************************

def GestionBodega(request):
    bodegas = Bodega.objects.all()
    if request.method == 'POST':
        formulario = BodegaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/bodega')
    else:
        formulario = BodegaForm()

    return render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas },
                              context_instance = RequestContext(request))


def editarBodega(request, idBodega):
    bodegas = Bodega.objects.all()
    bodega = Bodega.objects.get(pk=idBodega)
    if request.method == 'POST':
        formulario = BodegaForm(request.POST, instance=bodega)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/bodega')
    else:
        formulario = BodegaForm(instance=bodega)

    return  render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas},
                               context_instance = RequestContext(request))

def borrarBodega(request,idbodega ):
    bodega = Bodega.objects.get(pk=idbodega)
    bodega.delete()
    return  HttpResponseRedirect('/bodega')

def GestionProductoBodega(request,idproducto):
    productoBodegas = ProductoBodega.objects.filter(producto = idproducto)

    return render_to_response('Inventario/GestionProductoBodega.html',{'productoBodegas':productoBodegas },
                              context_instance = RequestContext(request))

#*****************************************PROVEEDOR**************************************************

def GestionProvedor(request):
    provedores = Proveedor.objects.all()
    if request.method == 'POST':
        formulario = ProvedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/provedor')
    else:
        formulario = ProvedorForm()

    return render_to_response('Inventario/GestionProvedor.html',{'formulario':formulario,'provedores':provedores },
                              context_instance = RequestContext(request))

#************************************************GANADO*******************************************************

def GestionGanado(request,idcompra):

    ganados = Ganado.objects.order_by('-codigoGanado')
    compra = Compra.objects.get(pk = idcompra)
    detallecompra = DetalleCompra()
    ganado = Ganado()



    if request.method == 'POST':
        formulario = GanadoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            ganado.codigoGanado = ganados[0].codigoGanado
            ganado.genero = request.POST.get('genero')
            ganado.pesoEnPie = request.POST.get('pesoEnPie')
            ganado.precioKiloEnPie = request.POST.get('precioKiloEnPie')
            ganado.precioTotal = request.POST.get('precioTotal')
            ganado.difPieCanal = request.POST.get('difPieCanal')

            detallecompra.compra = compra
            detallecompra.ganado = ganado
            detallecompra.pesoProducto = request.POST.get('pesoEnPie')
            detallecompra.unidades = 1
            detallecompra.vrCompraProducto = ganado.precioTotal
            detallecompra.estado = False
            detallecompra.subtotal = ganado.precioTotal
            detallecompra.save()



            artCompra = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra = 0
            totalPesoFactura = 0

            for dcmp in artCompra:
                totalPesoFactura += dcmp.pesoProducto

            for dcmp in artCompra:
                totalCompra += dcmp.subtotal

            compraTotal = Compra(
                                codigoCompra = compra.codigoCompra,
                                encargado = compra.encargado,
                                proveedor = compra.proveedor,
                                fechaCompra = compra.fechaCompra,
                                vrCompra = totalCompra,
                                tipo = compra.tipo
                                )


            compraTotal.save()


            return HttpResponseRedirect('/ganado/'+idcompra)
    else:
        formulario = GanadoForm()

    return render_to_response('Inventario/GestionGanado.html',{'formulario':formulario,'ganados':ganados,'compra':idcompra },
                              context_instance = RequestContext(request))

#**********************************************COMPRA***********************************************************

def GestionCompra(request):

    compras = Compra.objects.all()

    if request.method == 'POST':
        formulario = CompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            return HttpResponseRedirect('/compra')
    else:
        formulario =CompraForm()

    return render_to_response('Inventario/GestionCompras.html',{'formulario':formulario,'compras':compras },
                              context_instance = RequestContext(request))

def GestionDetalleCompra(request,idcompra):

    compra = Compra.objects.get(pk = idcompra)
    detcompras = DetalleCompra.objects.filter(compra = idcompra)
    totalCompra  = 0
    for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

    if request.method == 'POST':
        formulario = DetalleCompraForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            detcompras = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra  = 0
            for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

            compraTotal = Compra(
                                codigoCompra = compra.codigoCompra,
                                encargado = compra.encargado,
                                proveedor = compra.proveedor,
                                fechaCompra = compra.fechaCompra,
                                vrCompra = totalCompra )

            compraTotal.save()

            return HttpResponseRedirect('/detcompra/'+ idcompra)
    else:
        formulario = DetalleCompraForm(initial={'compra':idcompra})

    return render_to_response('Inventario/GestionDetalleCompra.html',{'formulario':formulario,
                                                         'compra': compra,
                                                         'detcompras': detcompras, 'totalCompra':totalCompra},
                                                        context_instance = RequestContext(request))

def GestionDesposte(request):
    despostes = PlanillaDesposte.objects.all()

    if request.method == 'POST':

        formulario = DesposteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/desposte/')
    else:
        formulario =DesposteForm()

    return render_to_response('Inventario/GestionDesposte.html',{'formulario':formulario,'despostes':despostes},
                              context_instance = RequestContext(request))

def GestionCanal(request,idrecepcion):

    canal = Canal.objects.filter(recepcion = idrecepcion)#para renderizar las listas
    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    sacrificio = Sacrificio.objects.get(recepcion = idrecepcion)


    if request.method == 'POST':
        formulario = CanalForm(request.POST)


        if formulario.is_valid():

            planilla = PlanillaDesposte.objects.get(pk = request.POST.get('planilla'))
            canalesPlanilla = Canal.objects.filter(planilla = planilla.codigoPlanilla)# Canales por planilla

            pesoCanales = 0

            for canales in canalesPlanilla:
                pesoCanales += canales.pesoPorkilandia


            vrKiloCanal = ((compra.vrCompra + sacrificio.vrDeguello + sacrificio.vrTransporte) -
                          (sacrificio.piel + sacrificio.vrMenudo))/ (pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))

            vrArrobaCanal = vrKiloCanal * Decimal(12.5)

            canal = Canal()
            canal.recepcion = recepcion
            canal.planilla = planilla
            canal.pesoFrigovito = request.POST.get('pesoFrigovito')
            canal.pesoPorkilandia = request.POST.get('pesoPorkilandia')
            canal.difPesos = request.POST.get('difPesos')
            canal.vrKiloCanal = vrKiloCanal
            canal.vrArrobaCanal= vrArrobaCanal

            canal.save()

            PesoTotalCanales = 0
            TotalPesoPie = 0
            canal = Canal.objects.filter(recepcion = idrecepcion)
            detCompra = DetalleCompra.objects.filter(compra = compra.codigoCompra)
            empleado = Empleado.objects.get(pk = recepcion.empleado.codigoEmpleado)
            provedor= Proveedor.objects.get(pk = recepcion.provedor.codigoProveedor)

            for det in detCompra:
                ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
                TotalPesoPie += ganado.pesoEnPie

            for cnl in canal:
                PesoTotalCanales += cnl.pesoPorkilandia

            recepcionUPD = PlanillaRecepcion(
                                            codigoRecepcion = recepcion.codigoRecepcion,
                                            compra = compra,
                                            empleado = empleado,
                                            tipoGanado = recepcion.tipoGanado,
                                            fechaRecepcion = recepcion.fechaRecepcion,
                                            cantCabezas = recepcion.cantCabezas,
                                            provedor = provedor,
                                            transporte = recepcion.transporte,
                                            difPieCanal = ((TotalPesoPie - PesoTotalCanales)*100)/TotalPesoPie
            )

            recepcionUPD.save()




            return HttpResponseRedirect('/canal/'+ idrecepcion)
    else:
        formulario = CanalForm(initial={'recepcion':idrecepcion})

    return render_to_response('Inventario/GestionCanal.html',{'formulario':formulario,'canal':canal,'recepcion':recepcion},
                              context_instance = RequestContext(request))

def GestionCanalDetalleDesposte(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

    totalReses = canales.count()
    totalDesposte = 0
    totalCanal = 0


    #proceso para guardar todos los productos despostados en la tabla producto.



    for detplanilla in detalleDespostes:
        totalDesposte += detplanilla.PesoProducto
    for canal in canales :
        totalCanal += canal.pesoPorkilandia
    totalCanal *= 1000


    if request.method == 'POST':
        formulario = DetalleDesposteForm(request.POST)

        if formulario.is_valid():
            formulario.save()

            producto = Producto.objects.get(pk = request.POST.get('producto'))
            bodega = Bodega.objects.get(pk = 5)
            bodegaprodID = ProductoBodega.objects.get(bodega = 5,producto = producto.codigoProducto )

            bodegaProducto = ProductoBodega()
            bodegaProducto.id = bodegaprodID.id
            bodegaProducto.producto = producto
            bodegaProducto.bodega = bodega
            bodegaProducto.pesoProductoStock = request.POST.get('PesoProducto')
            bodegaProducto.unidadesStock = 0

            bodegaProducto.save()

            desposte = PlanillaDesposte.objects.get(pk = idplanilla)
            canales = Canal.objects.filter(planilla = idplanilla)
            detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

            totalDesposte = 0
            totalCanal = 0


            for detplanilla in detalleDespostes:
                totalDesposte += detplanilla.PesoProducto

            for canal in canales :
                totalCanal += canal.pesoPorkilandia


            totalCanal *= 1000
            difCanalDesposte = (totalCanal - totalDesposte)/totalReses

            desposte = PlanillaDesposte(
                codigoPlanilla = idplanilla,
                fechaDesposte = desposte.fechaDesposte,
                resesADespostar = totalReses,
                totalDespostado = totalDesposte,
                difCanalADespostado = difCanalDesposte,
                costoProduccionTotal = 0
            )

            desposte.save()

            return HttpResponseRedirect('/detalleDesposte/'+ idplanilla)
    else:
        formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    return render_to_response('Inventario/GestionCanalDetalleDesposte.html',{'idplanilla':idplanilla,'formulario':formulario,'desposte':desposte
                                                                            ,'canales':canales,'detalleDespostes':detalleDespostes,
                                                                             'totalCanal':totalCanal,'totalDesposte':totalDesposte},
                              context_instance = RequestContext(request))


def CostoDesposte(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla)

    formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    totalReses = canales.count()

    canales = Canal.objects.filter(planilla = idplanilla)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)
    totalDesposte = 0
    totalCanal = 0
    kiloCanal = 0
    costoProduccionTotal = 0


    for detplanilla in detalleDespostes:
        totalDesposte += detplanilla.PesoProducto

    for canal in canales :
        totalCanal += canal.pesoPorkilandia
        kiloCanal = canal.vrKiloCanal


    costoCanal = totalCanal * kiloCanal #Hace referencia al costo del canal de reces despostadas
    totalMOD = totalReses * 12839 # MOD en desposte
    totalCIF = totalReses * 30173 # CIF en desposte
    costoTotalDesposte = costoCanal + totalMOD + totalCIF
    costoKiloDespostado = costoTotalDesposte / (totalDesposte/1000)
    kilosPorArroba = Decimal(12.5)
    costoArrobaDespostada = costoKiloDespostado * kilosPorArroba

    for detplanilla in detalleDespostes:

        prodActual= Producto.objects.get(pk = detplanilla.producto.codigoProducto)
        costoKiloProducto = round(costoArrobaDespostada * prodActual.porcentajeCalidad)/ 100
        costoProduccionProducto = Decimal(costoKiloProducto) * (detplanilla.PesoProducto/ 1000)
        costoProduccionTotal += costoProduccionProducto

    ajuste = (costoProduccionTotal - costoTotalDesposte)/ detalleDespostes.count()

    for detplanilla in detalleDespostes:

        prodActual= Producto.objects.get(pk = detplanilla.producto.codigoProducto)
        costoKiloProducto = round((costoArrobaDespostada + ajuste) * prodActual.porcentajeCalidad)/ 100
        grupo = Grupo.objects.get(pk = prodActual.grupo.id)

        productoUPD = Producto()
        productoUPD.codigoProducto = prodActual.codigoProducto
        productoUPD.grupo = grupo
        productoUPD.nombreProducto = prodActual.nombreProducto
        productoUPD.costoProducto = costoKiloProducto
        productoUPD.vrVentaProducto = prodActual.vrVentaProducto
        productoUPD.utilidadProducto = prodActual.utilidadProducto
        productoUPD.rentabilidadProducto = prodActual.rentabilidadProducto
        productoUPD.porcentajeCalidad = prodActual.porcentajeCalidad
        productoUPD.gravado = prodActual.gravado
        productoUPD.excento = prodActual.excento
        productoUPD.excluido = prodActual.excluido
        productoUPD.save()

    return render_to_response('Inventario/GestionCanalDetalleDesposte.html',{'idplanilla':idplanilla,'formulario':formulario,'desposte':desposte
                                                                            ,'canales':canales,'detalleDespostes':detalleDespostes,
                                                                             'totalCanal':totalCanal,'totalDesposte':totalDesposte},
                                                                            context_instance = RequestContext(request))



#**************************************************** EMPLEADOS ************************************************

def GestionEmpleados(request):

    empleados = Empleado.objects.all()

    if request.method == 'POST':

        formulario = EmpleadoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/empleado/')
    else:
        formulario =EmpleadoForm()

    return render_to_response('Inventario/GestionEmpleados.html',{'formulario':formulario,'empleados':empleados },
                              context_instance = RequestContext(request))

def GestionCargos(request):

    cargos = Cargo.objects.all()

    if request.method == 'POST':

        formulario = CargoForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/cargo/')
    else:
        formulario = CargoForm()

    return render_to_response('Inventario/Cargo.html',{'formulario':formulario,'cargos':cargos },
                              context_instance = RequestContext(request))

#********************************************TRASLADOS******************************************************
def GestionTraslados(request):
    traslados = Traslado.objects.all()
    if request.method == 'POST':

        formulario = TrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/traslado/')
    else:
        formulario =TrasladoForm()

    return render_to_response('Inventario/GestionTraslado.html',{'formulario':formulario,'traslados':traslados },
                              context_instance = RequestContext(request))


def GestionDetalleTraslado(request,idtraslado):

    traslado = Traslado.objects.get(pk = idtraslado)
    detraslados = DetalleTraslado.objects.filter(traslado = idtraslado)


    if request.method == 'POST':
        formulario = DetalleTrasladoForm(request.POST)
        if formulario.is_valid():
            formulario.save()

            bodegaActual = ProductoBodega.objects.get(bodega = traslado.bodegaActual.codigoBodega,
                                                      producto = request.POST.get('producto'))
            destino = Bodega.objects.get(nombreBodega = traslado.bodegaDestino)
            bodegaDestino = ProductoBodega.objects.get(bodega = destino.codigoBodega,
                                                       producto = request.POST.get('producto'))


            producto = Producto.objects.get(pk = request.POST.get('producto'))
            #subproducto = SubProducto.objects.get(pk = request.POST.get('subproducto'))

            pesoActualizado = bodegaActual.pesoProductoStock - int(request.POST.get('pesoPiezasTraslado'))
            unidadesActualizadas = bodegaActual.unidadesStock - int(request.POST.get('unidadesTraslado'))

            pesoDestinoActualizado = bodegaDestino.pesoProductoStock + int(request.POST.get('pesoPiezasTraslado'))
            unidadesDestinoActualizadas = bodegaActual.unidadesStock + int(request.POST.get('unidadesTraslado'))

            bodegaactual = ProductoBodega()
            bodegaactual.bodega = Bodega.objects.get(pk = bodegaActual.bodega.codigoBodega)
            bodegaactual.id = bodegaActual.id
            bodegaactual.producto = producto
            bodegaactual.pesoProductoStock = pesoActualizado
            bodegaactual.pesoProductoKilos = pesoActualizado / 1000
            bodegaactual.unidadesStock = unidadesActualizadas

            bodegaactual.save()

            bodegadestino = ProductoBodega()
            bodegadestino.id = bodegaDestino.id
            bodegadestino.bodega = Bodega.objects.get(pk = bodegaDestino.bodega.codigoBodega)
            bodegadestino.producto = producto
            bodegadestino.pesoProductoKilos = pesoDestinoActualizado / 1000
            bodegadestino.pesoProductoStock = pesoDestinoActualizado
            bodegadestino.unidadesStock = unidadesDestinoActualizadas


            bodegadestino.save()

            return HttpResponseRedirect('/dettraslado/'+ idtraslado)
    else:
        formulario = DetalleTrasladoForm(initial={'traslado':idtraslado})


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'formulario':formulario,
                                                         'traslado': traslado,
                                                         'detraslados': detraslados},
                                                        context_instance = RequestContext(request))


def GestionSacrificio(request,idrecepcion):

    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    sacrificios = Sacrificio.objects.all()
    detCompra = DetalleCompra.objects.filter(compra = recepcion.compra.codigoCompra)

    totalPieles = 0

    for det in detCompra:
        ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
        totalPieles += ganado.piel


    if request.method == 'POST':
        formSacrificio = SacrificioForm(request.POST)

        if formSacrificio.is_valid():

            cantCabezas = recepcion.cantCabezas

            menudo = cantCabezas * 90000
            deguello = cantCabezas * 82800
            transporte = cantCabezas * 8000

            sacrificio = Sacrificio()

            sacrificio.recepcion = recepcion
            sacrificio.piel = totalPieles
            sacrificio.vrMenudo = menudo
            sacrificio.vrDeguello = deguello
            sacrificio.vrTransporte = transporte
            sacrificio.cola = request.POST.get('cola')
            sacrificio.rinones = request.POST.get('rinones')
            sacrificio.creadillas = request.POST.get('creadillas')
            sacrificio.recortes = request.POST.get('recortes')
            sacrificio.desecho= request.POST.get('desecho')

            sacrificio.save()

            return HttpResponseRedirect('/sacrificio/'+idrecepcion)

    else:
        formSacrificio = SacrificioForm(initial={'recepcion':idrecepcion})


    return render_to_response('Inventario/GestionSacrificio.html',{'formSacrificio':formSacrificio,
                                                                   'sacrificios':sacrificios},
                              context_instance = RequestContext(request))


#*******************************************Recepcion de ganado*******************************************

def GestionPlanillaRecepcion(request , idcompra):

    recepciones = PlanillaRecepcion.objects.filter(compra = idcompra)
    detCompra = DetalleCompra.objects.filter(compra = idcompra)


    if request.method == 'POST':
        formulario = PlanillaRecepcionForm(request.POST)
        if formulario.is_valid():

            compra = Compra.objects.get(pk = idcompra)
            empleado = Empleado.objects.get(pk = request.POST.get('empleado'))
            provedor = Proveedor.objects.get(pk = request.POST.get('provedor'))

            Recepcion = PlanillaRecepcion()
            Recepcion.compra =compra
            Recepcion.empleado = empleado
            Recepcion.tipoGanado = request.POST.get('tipoGanado')
            Recepcion.cantCabezas = detCompra.count()
            Recepcion.provedor= provedor
            Recepcion.transporte = request.POST.get('transporte')
            Recepcion.save()

            return HttpResponseRedirect('/recepcion'+ idcompra)
    else:
        formulario = PlanillaRecepcionForm(initial={'compra':idcompra})

    return render_to_response('Inventario/GestionPlanillaRecepcion.html',{'formulario':formulario,'recepciones':recepciones },
                              context_instance = RequestContext(request))


