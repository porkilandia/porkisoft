 # -*- coding: UTF-8 -*-
from decimal import Decimal
from math import ceil

from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.template import RequestContext

from Inventario.Forms.forms import *
from Inventario.models import *



# Create your views here.

def home(request):
    productosBajoStock = ProductoBodega.objects.all().filter(pesoProductoStock = 0,unidadesStock = 0).order_by('bodega')
    costosProductos = Producto.objects.all().order_by('nombreProducto')

    return render_to_response('Home.html',{'productosBajoStock':productosBajoStock,
                                           'costosProductos':costosProductos},context_instance = RequestContext(request))

#***************************************PRODUCTOS******************************************
def listaProductos(request):
    productos = Producto.objects.all().order_by('nombreProducto')
    #Creacion de producto en cada bodega con valor inicial

    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save()

            if producto.grupo.id == 5 or producto.grupo.id == 10:# insumos o BasicosProcesados solo se grabaran en la bodega de Taller

                bodegaInicial = ProductoBodega()
                bodega = Bodega.objects.get(pk = 6)

                bodegaInicial.producto = producto
                bodegaInicial.bodega = bodega
                bodegaInicial.pesoProductoStock = 0
                bodegaInicial.unidadesStock = 0
                bodegaInicial.save()

            else:

                for bod in Bodega.objects.all():

                    bodegaInicial = ProductoBodega()
                    bodega = Bodega.objects.get(pk = bod.codigoBodega)

                    bodegaInicial.producto = producto
                    bodegaInicial.bodega = bodega
                    bodegaInicial.pesoProductoStock = 0
                    bodegaInicial.unidadesStock = 0
                    bodegaInicial.save()

            return HttpResponseRedirect('/inventario/listaProd')
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
            return HttpResponseRedirect('/inventario/listaProd')
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
            return HttpResponseRedirect('/inventario/verSubProductos/')
    else:
        formulario =SubProductoForm()

    return render_to_response('Inventario/GestionSubProducto.html',{'formulario':formulario,'subproductos':subproductos },
                              context_instance = RequestContext(request))


def borrarSubproducto(request, idSubproducto):
    subproducto = SubProducto.objects.get(pk=idSubproducto)
    subproducto.delete()

    return  HttpResponseRedirect('/inventario/verSubProductos')

def editarSubproducto(request, idSproducto):
    subproductos = SubProducto.objects.all().order_by('nombreSubProducto')
    sproducto = SubProducto.objects.get(pk=idSproducto)
    if request.method == 'POST':
        formulario = SubProductoForm(request.POST, instance=sproducto)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/verSubProductos')
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
            return HttpResponseRedirect('/inventario/addDSprod/'+ id_subproducto)
    else:
        formulario = DetSubProductoForm(initial={'subproducto':id_subproducto})

    return render_to_response('Inventario/GestionDetalleSubProducto.html',{'Tunds':totalUnd,'TPeso':totalPeso,'formulario':formulario,
                                                         'subrpoductos': subrpoductos,
                                                         'desubproductos': desubproductos},
                                                        context_instance = RequestContext(request))

def borrarDetalleSp(request, idDetalle):
    detsubproducto = DetalleSubProducto.objects.get(pk=idDetalle)
    detsubproducto.delete()
    return  HttpResponseRedirect('/inventario/verSubProductos')

#**************************************BODEGA****************************************************

def GestionBodega(request):
    bodegas = Bodega.objects.all()
    if request.method == 'POST':
        formulario = BodegaForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/bodega')
    else:
        formulario = BodegaForm()

    return render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas },
                              context_instance = RequestContext(request))

def GestionGrupo(request):
    grupos = Grupo.objects.all()
    if request.method == 'POST':
        formulario = GrupoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/grupo')
    else:
        formulario = GrupoForm()

    return render_to_response('Inventario/GestionGrupo.html',{'formulario':formulario,'grupos':grupos },
                              context_instance = RequestContext(request))



def editarBodega(request, idBodega):
    bodegas = Bodega.objects.all()
    bodega = Bodega.objects.get(pk=idBodega)
    if request.method == 'POST':
        formulario = BodegaForm(request.POST, instance=bodega)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/bodega')
    else:
        formulario = BodegaForm(instance=bodega)

    return  render_to_response('Inventario/GestionBodega.html',{'formulario':formulario,'bodegas':bodegas},
                               context_instance = RequestContext(request))

def borrarBodega(request,idbodega ):
    bodega = Bodega.objects.get(pk=idbodega)
    bodega.delete()
    return  HttpResponseRedirect('/inventario/bodega')

def GestionProductoBodega(request,idproducto):
    productoBodegas = ProductoBodega.objects.filter(producto = idproducto)
    producto = Producto.objects.get(pk = idproducto)

    return render_to_response('Inventario/GestionProductoBodega.html',{'productoBodegas':productoBodegas,'producto':producto },
                              context_instance = RequestContext(request))

#*****************************************PROVEEDOR**************************************************

def GestionProvedor(request):
    provedores = Proveedor.objects.all()
    if request.method == 'POST':
        formulario = ProvedorForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/inventario/provedor')
    else:
        formulario = ProvedorForm()

    return render_to_response('Inventario/GestionProvedor.html',{'formulario':formulario,'provedores':provedores },
                              context_instance = RequestContext(request))

#************************************************GANADO*******************************************************

def GestionGanado(request,idcompra):

    ganados = Ganado.objects.order_by('-codigoGanado')
    compra = Compra.objects.get(pk = idcompra)
    detallecompra = DetalleCompra()

    if request.method == 'POST':
        formulario = GanadoForm(request.POST)
        if formulario.is_valid():
            ganado = formulario.save()

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

            compra.vrCompra = totalCompra
            compra.save()

            return HttpResponseRedirect('/inventario/ganado/'+idcompra)
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

            return HttpResponseRedirect('/inventario/compra')
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
        formulario = DetalleCompraForm(idcompra,request.POST)
        if formulario.is_valid():
            detalleCompra = formulario.save()

            productoBodega = ProductoBodega.objects.get(bodega = 6,producto = detalleCompra.producto.codigoProducto)
            producto = Producto.objects.get(pk = detalleCompra.producto.codigoProducto)

            # Si el producto es un insumo

            if detalleCompra.producto.grupo.id == 5 :

                productoBodega.pesoProductoStock += detalleCompra.pesoProducto
                productoBodega.save()

                producto.costoProducto = detalleCompra.vrCompraProducto
                producto.save()

            # Si el producto es una verdura
            elif detalleCompra.producto.grupo.id == 6:

                productoBodega.pesoProductoStock += 0
                productoBodega.save()

            #Si el producto es para compra venta

            elif detalleCompra.producto.grupo.id == 7:

                productoBodegaCV = ProductoBodega.objects.get(bodega = 5,producto = detalleCompra.producto.codigoProducto)
                productoBodegaCV.pesoProductoStock += detalleCompra.pesoProducto
                productoBodegaCV.save()

            #Si el producto es Basico Procesado
            elif detalleCompra.producto.grupo.id == 10:

                producto.costoProducto = detalleCompra.vrCompraProducto
                producto.save()
                productoBodegaBP = ProductoBodega.objects.get(bodega = 6,producto = detalleCompra.producto.codigoProducto)
                productoBodegaBP.pesoProductoStock += detalleCompra.pesoProducto
                productoBodegaBP.save()

            detcompras = DetalleCompra.objects.filter(compra = idcompra)
            totalCompra  = 0
            for dcmp in detcompras: # clacular los totales de la lista de detalles de subproducto
                totalCompra += dcmp.subtotal

            compra.vrCompra = totalCompra
            compra.save()


            return HttpResponseRedirect('/inventario/detcompra/'+ idcompra)
    else:
        formulario = DetalleCompraForm(idcompra,initial={'compra':idcompra })

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
            return HttpResponseRedirect('/inventario/desposte')
    else:
        formulario =DesposteForm()

    return render_to_response('Inventario/GestionDesposte.html',{'formulario':formulario,'despostes':despostes},
                              context_instance = RequestContext(request))


#******************************************************CANAL***********************************************************
def GestionCanal(request,idrecepcion):

    canales = Canal.objects.filter(recepcion = idrecepcion)#para renderizar las listas
    recepcion = PlanillaRecepcion.objects.get(pk = idrecepcion)
    compra = Compra.objects.get(pk = recepcion.compra.codigoCompra)
    sacrificio = Sacrificio.objects.get(recepcion = idrecepcion)
    cantidad = canales.count() +1

    if request.method == 'POST':
        formulario = CanalForm(request.POST)


        if formulario.is_valid():

            planilla = PlanillaDesposte.objects.get(pk = request.POST.get('planilla'))
            canalesPlanilla = Canal.objects.filter(planilla = planilla.codigoPlanilla)# Canales por planilla
            pesoCanales = 0
            pesoPie = 0
            vrFactura = 0

            for canale in canalesPlanilla:
                    pesoCanales += canale.pesoPorkilandia

            canal = Canal()
            canal.recepcion = recepcion
            canal.planilla = planilla
            canal.pesoFrigovito = request.POST.get('pesoFrigovito')
            canal.pesoPorkilandia = request.POST.get('pesoPorkilandia')
            canal.difPesos = request.POST.get('difPesos')
            canal.genero = request.POST.get('genero')

            if compra.tipo == 'reses':

                vrKiloCanal = ((compra.vrCompra + sacrificio.vrDeguello + sacrificio.vrTransporte) -
                          (sacrificio.piel + sacrificio.vrMenudo))/ (pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))

                vrArrobaCanal = vrKiloCanal * Decimal(12.5)

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal


            elif compra.tipo == 'cerdos':

                menudo = 7000 * cantidad
                flete = 500000
                transporte = 3500 * cantidad
                deguello = 37000 * cantidad

                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1000


                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))

                vrFactura = (pesoCanales + pesoPorkilandia) * 6950 #--> 6050 es el valor establecido por granjas el paraiso
                pesoPie = Decimal(ceil(pesoCanales + Decimal(request.POST.get('pesoPorkilandia')))) / (Decimal(0.82))
                #KiloPie = vrFactPie / pesoPie
                vrFactPie = (vrFactura - deguello - flete) + menudo
                costoCanales = (vrFactPie + deguello + flete + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

                encargado = Empleado.objects.get(pk = compra.encargado.codigoEmpleado)
                provedor = Proveedor.objects.get(pk = compra.proveedor.codigoProveedor)


            else:
                menudo = 12000 * cantidad
                transporte = 7000* cantidad
                deguello = 48200 * cantidad
                pesoPorkilandia = Decimal(request.POST.get('pesoPorkilandia'))
                cantidadCanalCerdasGrandes = Canal.objects.filter(recepcion = idrecepcion,pesoPorkilandia__gte = 170)# busca registros que el peso sea mayor o igual a 150
                cantidadCanalCerdasChicas = Canal.objects.filter(recepcion = idrecepcion,pesoPorkilandia__lte = 169)# busca registros que el peso sea menor o igual a 150

                incrementoCG = 35 * cantidadCanalCerdasGrandes.count()
                incrementoCP = 32 * cantidadCanalCerdasChicas.count()

                if pesoPorkilandia >= 170:
                    incrementoCG += 35
                else:
                    incrementoCP += 32


                if pesoCanales == 0:#para cuando se ingresa la primera vez
                    pesoCanales = 1000



                pesoPie = pesoCanales + pesoPorkilandia + incrementoCG + incrementoCP
                vrFactura = pesoPie * 4400 #--> 4400 es el valor establecido por granjas el paraiso
                costoCanales = (vrFactura + deguello + transporte) - menudo
                vrKiloCanal = ceil(costoCanales / (pesoCanales + pesoPorkilandia))
                vrArrobaCanal = vrKiloCanal * 12.5

                canal.vrKiloCanal = vrKiloCanal
                canal.vrArrobaCanal= vrArrobaCanal

            #se graba el valor de la factura
            compra.vrCompra = vrFactura
            compra.save()
            # se guarda el canal
            canal.save()

            # Se guarda informacion adicional en el modelo recepcion

            PesoTotalCanales = 0
            TotalPesoPie = 0
            canal = Canal.objects.filter(recepcion = idrecepcion)
            detCompra = DetalleCompra.objects.filter(compra = compra.codigoCompra)


            if recepcion.tipoGanado == 'Mayor':
                for det in detCompra:
                    ganado = Ganado.objects.get(pk = det.ganado.codigoGanado)
                    TotalPesoPie += ganado.pesoEnPie
            else:
                TotalPesoPie = pesoPie


            for cnl in canal:
                PesoTotalCanales += cnl.pesoPorkilandia

            recepcion.difPieCanal = ceil(((Decimal(TotalPesoPie) - PesoTotalCanales)*100)/Decimal(TotalPesoPie))
            recepcion.save()


            return HttpResponseRedirect('/inventario/canal/'+ idrecepcion)
    else:
        formulario = CanalForm(initial={'recepcion':idrecepcion})

    return render_to_response('Inventario/GestionCanal.html',{'formulario':formulario,'canales':canales,'recepcion':recepcion},
                              context_instance = RequestContext(request))


def MarcarCanalDesposte(request, idcanal):

    canal = Canal.objects.get(pk=idcanal)
    recepcion = PlanillaRecepcion.objects.get(pk = canal.recepcion.codigoRecepcion)
    canales = Canal.objects.filter(recepcion = recepcion.codigoRecepcion)

    if request.method == 'POST':
        formulario = CanalForm(request.POST,instance=canal)
        if formulario.is_valid():

            formulario.save()
            return HttpResponseRedirect('/inventario/canal/'+ str(recepcion.codigoRecepcion))
    else:
        formulario = CanalForm(initial={'estado':True},instance=canal)

    return render_to_response('Inventario/GestionCanal.html',{'formulario':formulario,'canales':canales,'recepcion':recepcion},
                              context_instance = RequestContext(request))


#***********************************************PLANILLA DESPOSTE*******************************************************
def GestionCanalDetalleDesposte(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)
    canalesMachos = Canal.objects.filter(planilla = idplanilla).filter(estado = True).filter(genero = 'Macho')

    for cnl in canales:
        recepcion = PlanillaRecepcion.objects.get(pk = cnl.recepcion.codigoRecepcion)


    totalCanales = Canal.objects.filter(planilla = idplanilla)

    totalResesMachos = canalesMachos.count()
    totalReses = canales.count()
    totalDesposte = 0
    totalCanal = 0
    sacrificio = Sacrificio()

    #proceso para guardar todos los productos despostados en la tabla producto.


    for detplanilla in detalleDespostes:
        totalDesposte += detplanilla.PesoProducto

    for canal in canales :
        totalCanal += canal.pesoPorkilandia
        sacrificio = Sacrificio.objects.get( recepcion = canal.recepcion.codigoRecepcion)
    totalCanal *= 1000

    cola = (sacrificio.cola / totalCanales.count()) * totalReses
    rinon = (sacrificio.rinones / totalCanales.count()) * totalReses
    creadilla = (sacrificio.creadillas / totalCanales.count())* totalResesMachos
    recorte = (sacrificio.recortes /totalCanales.count()) * totalReses
    ubre = (sacrificio.ubre / totalCanales.count()) * totalReses


    if request.method == 'POST':
        formulario = DetalleDesposteForm(request.POST)

        if formulario.is_valid():

            PesoProducto = 0

            producto = Producto.objects.get(pk = request.POST.get('producto'))


            # se debe conservar el mismo IDProducto para que no se ocacionen errores

            if (producto.codigoProducto == 32):
                PesoProducto = cola

            if (producto.codigoProducto == 33):
                PesoProducto = rinon

            if (producto.codigoProducto == 34):
                PesoProducto = creadilla

            if (producto.codigoProducto == 36):
                PesoProducto = ubre


            detalleDesposte = DetallePlanilla()
            detalleDesposte.planilla = desposte
            detalleDesposte.producto = producto

            if producto.grupo.id == 4 :
                detalleDesposte.PesoProducto = PesoProducto
            else:
                 detalleDesposte.PesoProducto = request.POST.get('PesoProducto')

            # si el producto es recorte, se sumara al existente con el nuevo valor calculado

            if producto.codigoProducto == 23:
                detalleDesposte.PesoProducto = Decimal(request.POST.get('PesoProducto')) + recorte

            detalleDesposte.save()

            bodegaProducto = ProductoBodega.objects.get(bodega = 5,producto = producto.codigoProducto )

            if producto.grupo.id == 4 :
                bodegaProducto.pesoProductoStock = bodegaProducto.pesoProductoStock
            else:
                bodegaProducto.pesoProductoStock += int(request.POST.get('PesoProducto'))

            bodegaProducto.unidadesStock = 0

            bodegaProducto.save()

            desposte = PlanillaDesposte.objects.get(pk = idplanilla)
            canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
            detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)

            totalDesposte = 0
            totalCanal = 0
            Desecho = 0

            for detplanilla in detalleDespostes:
                producto = Producto.objects.get(pk = detplanilla.producto.codigoProducto)

                if producto.grupo.id == 3:
                    Desecho += detplanilla.PesoProducto

                totalDesposte += detplanilla.PesoProducto

            for canal in canales :
                totalCanal += canal.pesoPorkilandia

            totalCanal *= 1000

            difCanalDesposte = (totalCanal - totalDesposte)/totalReses

            desposte.resesADespostar = totalReses
            desposte.totalDespostado = totalDesposte - Desecho
            desposte.totalCanal = totalCanal
            desposte.difCanalADespostado = difCanalDesposte
            desposte.save()

            return HttpResponseRedirect('/inventario/detalleDesposte/'+ idplanilla)
    else:
        formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    return render_to_response('Inventario/GestionCanalDetalleDesposte.html',{'idplanilla':idplanilla,'formulario':formulario,'desposte':desposte
                                                                            ,'canales':canales,'detalleDespostes':detalleDespostes,
                                                                             'totalCanal':totalCanal,'totalDesposte':totalDesposte},
                              context_instance = RequestContext(request))


#**************************************************COSTO DESPOSTE*******************************************************
def CostoDesposte(request, idplanilla):

    desposte = PlanillaDesposte.objects.get(pk = idplanilla)
    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)
    planilla = PlanillaDesposte.objects.get(pk= idplanilla)

    formulario = DetalleDesposteForm(initial={'planilla':idplanilla})

    totalReses = canales.count()


    detalleDespostes = DetallePlanilla.objects.filter(planilla = idplanilla)
    totalDesposte = 0
    totalCanal = 0
    kiloCanal = 0


    for canal in canales :
        totalCanal += canal.pesoPorkilandia

    canales = Canal.objects.filter(planilla = idplanilla) #para conocer el verdadero valor del kilo en canal
    for cnl in canales:
        kiloCanal = cnl.vrKiloCanal

    costoProduccionTotal = 0


    #realizo los calculos generales de costo
    costoCanal = ceil(totalCanal * kiloCanal) #Hace referencia al costo del canal de reces despostadas
    totalMOD = totalReses * 12839 # MOD en desposte
    totalCIF = totalReses * 30173 # CIF en desposte
    costoTotalDesposte = ceil(costoCanal + 100  + totalMOD + totalCIF)
    costoKiloDespostado = ceil((Decimal(costoTotalDesposte) / planilla.totalDespostado)*1000)
    kilosPorArroba = 12.5
    costoArrobaDespostada = ceil(costoKiloDespostado * kilosPorArroba)


    for detalleplanilla in detalleDespostes:
        prodActual= Producto.objects.get(pk = detalleplanilla.producto.codigoProducto)
        costoKiloProducto = round(Decimal(costoArrobaDespostada) * prodActual.porcentajeCalidad)/ 100
        costoProduccionProducto = ceil(Decimal(costoKiloProducto) * (detalleplanilla.PesoProducto/ 1000))
        costoProduccionTotal += costoProduccionProducto

    #*******************************Prueba de WHILE para crear un bucle de ajuste a la formula*****************

    aumentoInicial = ceil((costoTotalDesposte * 100)/costoProduccionTotal)
    arrobaAjustada = costoArrobaDespostada + aumentoInicial

    while(costoProduccionTotal != costoTotalDesposte): # Mientras que los valores sean diferentes
                                                       # el ciclo seguira iterando hasta igualar los valores
        if costoProduccionTotal > costoTotalDesposte :
            ajuste = ceil((costoTotalDesposte * 100)/costoProduccionTotal)
            arrobaAjustada -= ceil(ajuste)
            costoProduccionTotal = 0
        else:
            ajuste = ceil((costoTotalDesposte * 100)/costoProduccionTotal)
            arrobaAjustada += ceil(ajuste)
            costoProduccionTotal = 0


        for detplan in detalleDespostes:
            prodActual= Producto.objects.get(pk = detplan.producto.codigoProducto)
            costoKiloProducto = round(Decimal(arrobaAjustada) * prodActual.porcentajeCalidad)/ 100
            costoProduccionProducto = ceil(Decimal(costoKiloProducto) * (detplan.PesoProducto/ 1000))
            costoProduccionTotal += costoProduccionProducto

        if (((costoProduccionTotal - costoTotalDesposte) >= -600) and ((costoProduccionTotal - costoTotalDesposte) <= 600)):
            break #Si la diferencia entre los valores llega a un valor por encima o pro debajo de 600 pesos el ciclo se detiene
        #*******************************************************************************************************

    for detplanilla in detalleDespostes:

        #tomo el producto el cual voy a costear
        producto = Producto.objects.get(pk = detplanilla.producto.codigoProducto)

        costoKiloProducto = round(Decimal(arrobaAjustada) * producto.porcentajeCalidad)/ 100 # aplicamos el nuevo valor de la arroba para
                                                                                           #recalcular el kilo de  ese producto

        # se graba el costo del producto
        producto.costoProducto = costoKiloProducto
        producto.save()


    canales = Canal.objects.filter(planilla = idplanilla).filter(estado = True)

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
            return HttpResponseRedirect('/inventario/empleado')
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
            return HttpResponseRedirect('/inventario/cargo')
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
            return HttpResponseRedirect('/inventario/traslado')
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



            pesoActualizado = bodegaActual.pesoProductoStock - int(request.POST.get('pesoTraslado'))
            unidadesActualizadas = bodegaActual.unidadesStock - int(request.POST.get('unidadesTraslado'))

            pesoDestinoActualizado = bodegaDestino.pesoProductoStock + int(request.POST.get('pesoTraslado'))
            unidadesDestinoActualizadas = bodegaActual.unidadesStock + int(request.POST.get('unidadesTraslado'))

            #Se extrae de la bodega actual
            bodegaActual.pesoProductoStock = pesoActualizado
            bodegaActual.pesoProductoKilos = pesoActualizado / 1000
            bodegaActual.unidadesStock = unidadesActualizadas
            bodegaActual.save()

            #Se graba en la bodega destino
            bodegaDestino.pesoProductoStock = pesoDestinoActualizado
            bodegaDestino.pesoProductoKilos = pesoDestinoActualizado / 1000
            bodegaDestino.unidadesStock= unidadesDestinoActualizadas
            bodegaDestino.save()

            return HttpResponseRedirect('/inventario/dettraslado/'+ idtraslado)
    else:
        formulario = DetalleTrasladoForm(initial={'traslado':idtraslado})


    return render_to_response('Inventario/GestionDetalleTraslado.html',{'formulario':formulario,
                                                         'traslado': traslado,
                                                         'detraslados': detraslados},
                                                        context_instance = RequestContext(request))


#***************************************************SACRIFICIOS*********************************************************
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
            sacrificio.ubre = request.POST.get('ubre')
            sacrificio.desecho= request.POST.get('desecho')

            sacrificio.save()

            prodLimpieza = ['Cola','Riñones','Creadillas','Recortes x 800 grs','Ubre' ]
            item = ['cola','rinones','creadillas','recortes','ubre' ]
            cont = 0

            for productos  in prodLimpieza:

                producto = Producto.objects.get(nombreProducto = productos )
                existencia = ProductoBodega.objects.get(producto = producto.codigoProducto , bodega = 5)

                existencia.producto = producto
                existencia.pesoProductoStock = existencia.pesoProductoStock + Decimal(request.POST.get(item[cont]))
                existencia.save()

                cont +=1


            return HttpResponseRedirect('/inventario/sacrificio/'+idrecepcion)

    else:
        formSacrificio = SacrificioForm(initial={'recepcion':idrecepcion})


    return render_to_response('Inventario/GestionSacrificio.html',{'formSacrificio':formSacrificio,
                                                                   'sacrificios':sacrificios},
                              context_instance = RequestContext(request))


#*******************************************RECEPCION DE GANADO*********************************************************
def GestionPlanillaRecepcion(request , idcompra):

    recepciones = PlanillaRecepcion.objects.filter(compra = idcompra)
    detCompra = DetalleCompra.objects.filter(compra = idcompra)


    if request.method == 'POST':
        formulario = PlanillaRecepcionForm(request.POST)
        if formulario.is_valid():
            Recepcion = formulario.save()

            Recepcion.tipoGanado = request.POST.get('tipoGanado')
            Recepcion.cantCabezas = detCompra.count()
            Recepcion.transporte = request.POST.get('transporte')
            Recepcion.save()

            return HttpResponseRedirect('/inventario/recepcion/'+ idcompra)
    else:
        formulario = PlanillaRecepcionForm(initial={'compra':idcompra})

    return render_to_response('Inventario/GestionPlanillaRecepcion.html',{'formulario':formulario,'recepciones':recepciones },
                              context_instance = RequestContext(request))

def GestionEnsalinado(request,idproducto):
    ensalinados = Ensalinado.objects.all()
    bodegaProducto = ProductoBodega.objects.get(bodega = 6 , producto = idproducto)
    producto = Producto.objects.get(pk =  idproducto)
    sal = Producto.objects.get(pk = 94)
    papaina = Producto.objects.get(pk = 95)

    if request.method == 'POST':
        formulario = EnsalinadoForm(request.POST)

        if formulario.is_valid():
            ensalinado = formulario.save()

            costoSal = (ensalinado.pesoSal/ 1000) * sal.costoProducto
            costoPapaina = (ensalinado.pesoPapaina / 1000) * papaina.costoProducto
            costoProductoEnsalinado = (ensalinado.pesoProducto / 1000) * producto.costoProducto
            costoInsumos = costoSal + costoPapaina + costoProductoEnsalinado
            cif = 30 * (ensalinado.pesoProductoDespues / 1000)
            mod = 20 * (ensalinado.pesoProductoDespues / 1000)
            costoTotal = cif + mod + costoInsumos
            costoKilo = ceil(costoTotal / (ensalinado.pesoProductoDespues /1000))

            ensalinado.pesoProductoDespues /= 1000
            ensalinado.pesoProductoAntes /= 1000
            ensalinado.pesoProducto /= 1000
            ensalinado.costoTotal = costoTotal
            ensalinado.costoKilo = costoKilo
            ensalinado.save()

            # se guarda en el Producto el Costo del Kilo
            piernaEnsalinada = Producto.objects.get(nombreProducto = 'Pierna Ensalinada')
            piernaEnsalinada.costoProducto = costoKilo
            piernaEnsalinada.save()

            #Se guarda la cantidad final en la bodega de taller
            bodegaEnsalinado = ProductoBodega.objects.get(bodega = 6,producto = piernaEnsalinada.codigoProducto)
            bodegaEnsalinado.pesoProductoStock += ensalinado.pesoProductoDespues * 1000
            bodegaEnsalinado.save()

            #se resta la cantidad de Carne que se utilizo para el ensalinado
            bodegaProductoAntes = ProductoBodega.objects.get(bodega = 6, producto = producto.codigoProducto)
            bodegaProductoAntes.pesoProductoStock -= ensalinado.pesoProductoAntes * 1000
            bodegaProductoAntes.save()


            #Se guarda la cantidad a restar para la sal
            salBodega = ProductoBodega.objects.get(bodega = 6 , producto = 94)
            salBodega.pesoProductoStock -= ensalinado.pesoSal
            salBodega.save()

            #Se guarda la cantidad a restar para la Papaina

            PapainaBodega = ProductoBodega.objects.get(bodega = 6 , producto = 95)
            PapainaBodega.pesoProductoStock -= ensalinado.pesoPapaina
            PapainaBodega.save()

            return HttpResponseRedirect('/inventario/ensalinados/'+ idproducto)
    else:
        formulario = EnsalinadoForm(initial={'producto':idproducto, 'pesoProducto':bodegaProducto.pesoProductoStock})

    return render_to_response('Inventario/GestionEnsalinados.html',{'formulario':formulario,'ensalinados':ensalinados },
                              context_instance = RequestContext(request))

def GestionVerduras(request,idDetcompra):
    detalleCompra = DetalleCompra.objects.get(pk = idDetcompra)
    verduras = LimpiezaVerduras.objects.filter(compra = detalleCompra.id )
    compra = Compra.objects.get(pk = detalleCompra.compra.codigoCompra)
    producto = Producto.objects.get(pk = detalleCompra.producto.codigoProducto)
    detalles = DetalleCompra.objects.filter(compra = compra.codigoCompra)

    pesoDetalle = 0

    for detalle in detalles:
        pesoDetalle += detalle.pesoProducto

    if request.method == 'POST':

        formulario = LimpiezaVerdurasForm(request.POST)
        if formulario.is_valid():
            verdura = formulario.save()

            #Calculo del costo de la verdura limpia

            vrCompra = detalleCompra.subtotal
            porcentajeTransporte = ((detalleCompra.pesoProducto * 100) /pesoDetalle)/100
            transporte = compra.vrTransporte * porcentajeTransporte
            mod = verdura.mod * verdura.pesoProducto
            cif = verdura.cif * verdura.pesoProducto
            costo = vrCompra + cif + mod + transporte
            costoKilo = costo / (verdura.pesoProducto / 1000 )

            #Se guarda el costo de la verdura limpia
            verdura.vrKilo = costoKilo
            verdura.save()

            #guardamos el producto en Bodega

            bodegaProducto = ProductoBodega.objects.get(bodega = 6 , producto = producto.codigoProducto )
            bodegaProducto.pesoProductoStock += verdura.pesoProducto
            bodegaProducto.pesoProductoKilos = bodegaProducto.pesoProductoStock / 1000
            bodegaProducto.save()

            #guardamos el costo del producto

            producto.costoProducto = costoKilo
            producto.save()

            # se cambia el estado a verdadero para producto Limpio!!!
            detalleCompra.estado = True
            detalleCompra.save()


            return HttpResponseRedirect('/inventario/verduras/'+ idDetcompra)
    else:
        formulario = LimpiezaVerdurasForm(initial={'compra':idDetcompra,'producto': detalleCompra.producto.codigoProducto})

    return render_to_response('Inventario/GestionVerduras.html',{'formulario':formulario,'verduras':verduras,
                                                                 'compra':detalleCompra.compra.codigoCompra },
                              context_instance = RequestContext(request))

def GestionCondimento(request):
    condimentos  = Condimento.objects.all()

    if request.method == 'POST':

        formulario = CondimentoForm(request.POST)
        if formulario.is_valid():
            condimento = formulario.save()

            #Guardamos el condimento producido en Bodega
            bodega = ProductoBodega.objects.get(bodega = 6, producto__nombreProducto = 'Condimento Natural')
            bodega.pesoProductoStock += condimento.pesoCondimento
            bodega.save()

            #guardamos el peso de producto en Kg ya que al ingresar este se especifica en gramos
            condimento.pesoCondimento = (condimento.pesoCondimento / 1000)
            condimento.save()

            return HttpResponseRedirect('/inventario/condimento/')
    else:
        formulario = CondimentoForm()

    return render_to_response('Inventario/GestionCondimento.html',{'formulario':formulario,'condimentos':condimentos },
                              context_instance = RequestContext(request))

def GestionDetalleCondimento(request,idcondimento):
    condimento = Condimento.objects.get(pk = idcondimento)
    detalleCondimentos = DetalleCondimento.objects.filter(condimento = idcondimento)

    if request.method == 'POST':

        formulario = DetalleCondimentoForm(request.POST)
        if formulario.is_valid():
            detalle = formulario.save()

            producto = Producto.objects.get(pk = detalle.producto.codigoProducto)
            costoProducto = producto.costoProducto
            costoTotalVerduras =(condimento.cantFormulas * costoProducto )* (detalle.pesoProducto/1000)

            # Se resta la cantidad de producrto utilizado en las formulas de condimento y se graba el registro
            bodega = ProductoBodega.objects.get(bodega = 6, producto = detalle.producto.codigoProducto)
            bodega.pesoProductoStock -= (detalle.pesoProducto * condimento.cantFormulas)
            bodega.save()

            detalle.costoProducto = costoProducto
            detalle.costoTotalProducto = costoTotalVerduras
            detalle.pesoProducto /= 1000

            detalle.save()



            return HttpResponseRedirect('/inventario/detallecondimento/'+ idcondimento)
    else:
        formulario = DetalleCondimentoForm(initial={'condimento':idcondimento})

    return render_to_response('Inventario/GestionDetalleCondimento.html',{'formulario':formulario,
                                                                   'condimento': condimento,'idcondimento':idcondimento,
                                                                   'detalleCondimentos':detalleCondimentos },
                              context_instance = RequestContext(request))

def CostoCondimento(request,idcondimento):

    condimento = Condimento.objects.get(pk = idcondimento)
    detalleCondimentos = DetalleCondimento.objects.filter(condimento = idcondimento)
    formulario = DetalleCondimentoForm(initial={'condimento':idcondimento})

    pesoCondProcesado = condimento.pesoCondimento
    costoVerduras = 0

    for costo in detalleCondimentos:
        costoVerduras += costo.costoTotalProducto

    mod = 54 * pesoCondProcesado
    cif = 60 * pesoCondProcesado
    costoCondProsecesado = costoVerduras + cif + mod
    costoLitroCond = ceil(costoCondProsecesado/ pesoCondProcesado)

    #Se graban todos los calculos realizados

    condimento.costoLitroCondimento = costoLitroCond
    condimento.costoCondimento = ceil(costoCondProsecesado)

    condimento.save()

    producto = Producto.objects.get(nombreProducto = 'Condimento Natural')
    producto.costoProducto = costoLitroCond
    producto.save()



    return render_to_response('Inventario/GestionDetalleCondimento.html',{'formulario':formulario,
                                                                   'condimento': condimento,'idcondimento':idcondimento,
                                                                   'detalleCondimentos':detalleCondimentos },
                              context_instance = RequestContext(request))


def GestionCondTajado(request, idprodbod):
    condTajados  = CondimentadoTajado.objects.all()
    prodBod = ProductoBodega.objects.get(pk = idprodbod )
    producto = Producto.objects.get(pk = prodBod.producto.codigoProducto)
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if request.method == 'POST':

        formulario = CondTajadoForm(request.POST)
        if formulario.is_valid():
            proceso = formulario.save()

            mod = Decimal(0.139) * prodBod.pesoProductoStock
            cif = Decimal(0.143) * prodBod.pesoProductoStock
            costoTotalACondimentar = producto.costoProducto + mod + cif

            costoFilete = costoTotalACondimentar * Decimal(0.973)
            costoRecortes = costoTotalACondimentar * Decimal(0.007)#Pendiente guardar en inventario
            costoProcesos = costoTotalACondimentar * Decimal(0.02)#Pendiente guardar en inventario

            costoKiloFilete = costoFilete / proceso.filete
            costoTotalFilete = proceso.filete * costoKiloFilete
            costoTotalCondimento = proceso.condimento * condimento.costoProducto
            costoFileteCondimentado = costoTotalFilete +  costoTotalCondimento
            pesoFileteCondimentado = proceso.filete + proceso.condimento
            costoKiloFileteCondimentado = costoFileteCondimentado / pesoFileteCondimentado


            #Promediamos el costo del filete y lo guardamos
            filete = Producto.objects.get(nombreProducto = 'Filete Condimentado')
            if filete.costoProducto == 0:
                filete.costoProducto = costoKiloFileteCondimentado
            else:
                costoKiloFiletePromedio = (costoKiloFileteCondimentado + filete.costoProducto)/2
                filete.costoProducto = costoKiloFiletePromedio

            filete.save()

            # Guardamos el la cantidad de producto condimentado en la bodega de la planta de procesos
            bodegaFilete = ProductoBodega.objects.get(bodega = 6 , producto = filete.codigoProducto)
            bodegaFilete.pesoProductoStock += pesoFileteCondimentado
            bodegaFilete.save()

            #Restamos la cantidad utilizada a la cantidad ensalinada
            prodBod.pesoProductoStock -= proceso.pesoProductoEnsalinado
            prodBod.save()


            return HttpResponseRedirect('/inventario/condtaj/'+ idprodbod)
    else:
        formulario = CondTajadoForm(initial={'producto':producto.codigoProducto,'pesoProductoEnsalinado':prodBod.pesoProductoStock})

    return render_to_response('Inventario/GestionCondTajado.html',{'formulario':formulario,'condTajados':condTajados },
                              context_instance = RequestContext(request))

#*********************************************************** MIGA*******************************************************

def GestionMiga(request):
    migas  = Miga.objects.all()

    if request.method == 'POST':

        formulario = MigaForm(request.POST)
        if formulario.is_valid():
            miga = formulario.save()

            #Guardamos la cantidad de producto procesado en la bodega de planta de procesos
            bodegaMiga = ProductoBodega.objects.get(bodega = 6, producto__nombreProducto = 'Miga' )
            bodegaMiga.pesoProductoStock += miga.PesoFormulaMiga
            bodegaMiga.save()

            miga.PesoFormulaMiga /= 1000
            miga.save()

            return HttpResponseRedirect('/inventario/miga')
    else:
        formulario = MigaForm()

    return render_to_response('Inventario/GestionMiga.html',{'formulario':formulario,'migas':migas },
                              context_instance = RequestContext(request))

def GestionDetalleMiga(request,idmiga):
    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)

    if request.method == 'POST':

        formulario = DetalleMigaForm(request.POST)
        if formulario.is_valid():
            detalle =  formulario.save()

            producto = Producto.objects.get(pk = detalle.producto.codigoProducto)
            costoProducto = producto.costoProducto
            costoTotalmiga = (miga.cantidadFormulas * costoProducto )* (detalle.PesoProducto/1000)

            # Se resta la cantidad de producrto utilizado en las formulas de condimento y se graba el registro
            bodega = ProductoBodega.objects.get(bodega = 6, producto = detalle.producto.codigoProducto)
            bodega.pesoProductoStock -= (detalle.PesoProducto * miga.cantidadFormulas)
            bodega.save()

            detalle.costoProducto = costoProducto
            detalle.costoTotalProducto = costoTotalmiga
            detalle.PesoProducto /= 1000
            detalle.save()


            return HttpResponseRedirect('/inventario/detallemiga/'+ idmiga)
    else:
        formulario = DetalleMigaForm(initial={'miga':idmiga})

    return render_to_response('Inventario/GestionDetalleMiga.html',{'formulario':formulario,'miga':miga,
                                                                           'detallesMiga':detallesMiga,'idmiga':idmiga },
                              context_instance = RequestContext(request))

def CostoMiga(request,idmiga):

    miga = Miga.objects.get(pk = idmiga)
    detallesMiga = DetalleMiga.objects.filter(miga = idmiga)
    formulario = DetalleMigaForm(initial={'miga':idmiga})

    pesoMigaProcesada = miga.PesoFormulaMiga
    costoInsumos = 0

    for costo in detallesMiga:
        costoInsumos += costo.costoTotalProducto

    mod = 38 * pesoMigaProcesada
    cif = 57 * pesoMigaProcesada
    costomigaProsecesada = costoInsumos + cif + mod
    costoKiloMiga = ceil(costomigaProsecesada/ pesoMigaProcesada)

    #Se graban todos los calculos realizados

    miga.costoKiloMigaProcesada = costoKiloMiga
    miga.costoFormulaMiga = ceil(costomigaProsecesada)
    miga.save()

    producto = Producto.objects.get(nombreProducto = 'Miga')
    producto.costoProducto = costoKiloMiga
    producto.save()

    return render_to_response('Inventario/GestionDetalleMiga.html',{'formulario':formulario,
                                                                   'miga': miga,'idmiga':idmiga,
                                                                   'detallesMiga':detallesMiga },
                              context_instance = RequestContext(request))

def GestionApanado(request,idprodbod):

    bodegaFilete = ProductoBodega.objects.get(pk = idprodbod)
    apanados = Apanado.objects.filter(producto = bodegaFilete.producto.codigoProducto )
    miga = Producto.objects.get(nombreProducto = 'Miga')
    Huevos = Producto.objects.get(nombreProducto = 'Huevos')
    filete = Producto.objects.get(nombreProducto = 'Filete Condimentado')
    fileteApanado =  Producto.objects.get(nombreProducto = 'Filete Apanado')
    bodegaHuevos = ProductoBodega.objects.get(bodega = 6, producto = Huevos.codigoProducto)
    bodegaMiga = ProductoBodega.objects.get(bodega = 6 , producto = miga.codigoProducto)
    bodegaFileteApanado = ProductoBodega.objects.get(bodega = 5 , producto = fileteApanado.codigoProducto)

    if request.method == 'POST':
        formulario = ApanadoForm(request.POST)
        if formulario.is_valid():
            apanado = formulario.save()

            CostoTotalMiga = miga.costoProducto * apanado.miga
            CostoTotalHuevos = Huevos.costoProducto * apanado.huevos
            CostoTotalFilete = filete.costoProducto * apanado.pesoFilete

            CostoFiletePorApanar = CostoTotalMiga + CostoTotalFilete + CostoTotalHuevos

            mod = Decimal(0.096) * apanado.totalApanado
            cif= Decimal(0.134) * apanado.totalApanado

            costoFileteApanado = CostoFiletePorApanar + mod + cif
            costoKiloApanado = costoFileteApanado / apanado.totalApanado

            #Guardamoslos calculos realizados
            apanado.costoKiloApanado = costoKiloApanado
            apanado.save()

            #Restamos la cantidad de productos usados en el proseso

            bodegaFilete.pesoProductoStock -= apanado.pesoFilete
            bodegaFilete.save()

            bodegaHuevos.unidadesStock -= apanado.huevos
            bodegaHuevos.save()

            bodegaMiga.pesoProductoStock -= apanado.miga
            bodegaMiga.save()

            #Guardamos el costo del Kilo del Filete Apanado
            fileteApanado.costoProducto = costoKiloApanado
            fileteApanado.save()

            #Guardamos la cantidad de filete apanado
            bodegaFileteApanado.pesoProductoStock = apanado.totalApanado
            bodegaFileteApanado.save()

            return HttpResponseRedirect('/inventario/apanado/'+idprodbod)
    else:
        #Se Setea el valor inicial del formulario con las cantidades existentes
        formulario = ApanadoForm(initial={'producto':bodegaFilete.producto.codigoProducto,
                                          'pesoFilete':bodegaFilete.pesoProductoStock,
                                          'huevos':bodegaHuevos.unidadesStock,
                                          'miga':bodegaMiga.pesoProductoStock})

    return render_to_response('Inventario/GestionApanado.html',{'formulario':formulario, 'apanados': apanados},
                              context_instance = RequestContext(request))

def GestionarTajadoCondPechugas(request,idprodbod):
    bodegaPechuga = ProductoBodega.objects.get(pk = idprodbod)
    registros = CondimentadoTajadoPechuga.objects.filter(producto = bodegaPechuga.producto.codigoProducto)
    fileteCondimentado = Producto.objects.get(nombreProducto = 'Filete de Pollo Condimentado')
    hueso = Producto.objects.get(nombreProducto = 'Hueso de pollo')
    piel = Producto.objects.get(nombreProducto = 'Piel')
    procesos = Producto.objects.get(nombreProducto = 'Procesos de pollo')
    condimento = Producto.objects.get(nombreProducto = 'Condimento Natural')

    if request.method == 'POST':
        formulario = CondTajPechugasForm(request.POST)
        if formulario.is_valid():
            tajado = formulario.save()

            compra = Compra.objects.get(pk = tajado.compra)
            costoKiloDescongelado = (tajado.PesoDescongelado / 1000) / compra.vrCompra
            costoPechugaAProcesar = costoKiloDescongelado * tajado.PesoDescongelado
            mod = Decimal(0.161) * tajado.PesoDescongelado
            cif = Decimal(0.131) * tajado.PesoDescongelado
            costoTotalPechuga = costoPechugaAProcesar + mod + cif
            totalFileteTajado = tajado.fileteACond + tajado.fileteAApanar

            costoFilete = costoTotalPechuga * Decimal(0.95)
            costoHueso = costoTotalPechuga * hueso.porcentajeCalidad
            costoPiel = costoTotalPechuga * piel.porcentajeCalidad
            costoProcesos = costoTotalPechuga * procesos.porcentajeCalidad
            costoTotalCondimento = tajado.condimento * condimento.costoProducto
            costoTotalCondimentoApanar = tajado.condimentoAP * condimento.costoProducto

            #calculamos el costo por kilo de cada producto obtenido
            costoKiloFilete = costoFilete / totalFileteTajado
            costoKiloHueso = costoHueso / tajado.huesos
            costoKiloPiel = costoPiel / tajado.piel
            costoKiloProcesos = costoProcesos/ tajado.procesos

            #Calculamos el filete que se va a condimentar
            costoFileteACondimentar = costoKiloFilete * tajado.fileteACond
            costoFileteCondimentado = costoFileteACondimentar + costoTotalCondimento
            costoKiloFileteCondimentado = costoFileteCondimentado / tajado.fileteACond

            #Calculamos el Filete que se va a Apanar

            costoFileteAcondApanado = costoFilete * tajado.fileteAApanar
            costoFileteCondimentadoApanar = costoFileteAcondApanado + costoTotalCondimentoApanar
            costoKiloFileteCondApanar = costoFileteCondimentadoApanar / tajado.tajado.fileteAApanar



            #Guardamos los costo del filete condimentado para venta
            fileteCondimentado.costoProducto = costoKiloFileteCondimentado
            fileteCondimentado.save()

            #guardamos la cantidad de filete condimetado para la venta
            bodegaFileteCondimentado = ProductoBodega.objects.get(bodega = 5, producto = fileteCondimentado.codigoProducto )
            bodegaFileteCondimentado.pesoProductoStock = tajado.fileteACond + tajado.condimento
            bodegaFileteCondimentado.save()

            #obtenemos las bodegas de los subproductos
            bodegaHueso = ProductoBodega.objects.get(bodega = 5,producto = hueso.codigoProducto)
            bodegaPiel = ProductoBodega.objects.get(bodega = 5,producto = piel.codigoProducto)
            bodegaProcesos = ProductoBodega.objects.get(bodega = 5,producto = procesos.codigoProducto)

            #guardamos el costo y la cantidad de los  subproductos
            hueso.costoProducto = costoKiloHueso
            bodegaHueso.pesoProductoStock = tajado.huesos
            bodegaHueso.save()
            hueso.save()

            piel.costoProducto = costoKiloPiel
            bodegaPiel.pesoProductoStock = tajado.piel
            bodegaPiel.save()
            piel.save()

            procesos.costoProducto = costoKiloProcesos
            bodegaProcesos.pesoProductoStock = tajado.procesos
            bodegaProcesos.save()
            procesos.save()

            #Restamos la cantidad de pechuga utilizada
            bodegaPechuga.pesoProductoStock -= tajado.PesoDescongelado
            bodegaPechuga.save()

            #restamos la cantidad de condimento utilizada
            bodegaCondimento = ProductoBodega.objects.get(bodega = 6 , producto = condimento.codigoProducto)
            bodegaCondimento.pesoProductoStock -= tajado.condimento + tajado.condimentoAP
            bodegaCondimento.save()

            #pendiente  la vista para el apanado delFilete Condimentado

            return HttpResponseRedirect('/inventario/pechugas/'+idprodbod)
    else:
        formulario = CondTajPechugasForm(initial={'producto':bodegaPechuga.producto.codigoProducto})

    return render_to_response('Inventario/GestionTajaddoCondPechugas.html',{'formulario':formulario,'registros':registros}
                              ,context_instance = RequestContext(request))