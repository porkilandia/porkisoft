$(document).on('ready', inicio);
 function inicio()
 {


     $('#id_precioTotal').on('focus',calculoGanado);
     $('#id_difPesos').on('focus',calculoCanal);
     $('#id_subtotal').on('focus', calculoCompra);
     $('#id_pesoProductoAntes').on('focus', calculoEnsalinado);
     $('#nuevo').on('click',nuevoRegistro);
     $('#cerrar').on('click',cerrarVentana);
     $('#editaFila').on('click',editaFilas);


     $('#tablacostos').dataTable();
     $('#tablastock').dataTable();
     $('#tablaTraslados').dataTable();
     $('#tablaCompras').dataTable();
     $('#tablaProductos').dataTable();
     $('#ListaSubp').dataTable();
     $('#tablabodegas').dataTable();
     $('#tablaproveedor').dataTable();
     $('#despostes').dataTable();
 }
function calculoGanado(){


         var pesoEnPie = $('#id_pesoEnPie').val();
         var vrKiloEnPie = $('#id_precioKiloEnPie').val();
         var total = pesoEnPie * vrKiloEnPie;
            $('#id_precioTotal').val(total);



}
function calculoCanal(){

         var pesoPorkilandia = $('#id_pesoPorkilandia').val();
         var pesoFrigovito = $('#id_pesoFrigovito').val();
         var totalCanal =  pesoFrigovito - pesoPorkilandia;

         $('#id_difPesos').val(totalCanal.toFixed(2));
}

function calculoCompra()
{
    var unidades = $('#id_unidades').val();
    var pesoProducto = $('#id_pesoProducto').val();
    var vrUnitario = $('#id_vrCompraProducto').val();

    if (unidades !=0){

        var totalUnidades = unidades * vrUnitario;
        $('#id_subtotal').val(totalUnidades);
    }
    if (pesoProducto != 0){

        var totalPeso = (pesoProducto/ 1000) * vrUnitario;
        $('#id_subtotal').val(totalPeso);
    }

}

function calculoEnsalinado()
{
    var pesoProducto = $('#id_pesoProducto').val();
    var pesoSal = $('#id_pesoSal').val();
    var pesoPapaina = $('#id_pesoPapaina').val();
    var pesoAntes = parseFloat(pesoProducto) + parseFloat(pesoSal) + parseFloat(pesoPapaina);

    $('#id_pesoProductoAntes').val(pesoAntes);

}

function nuevoRegistro()
     {
         $('fieldset').fadeIn();
         return false
     }

function cerrarVentana()
{
    $('fieldset').fadeOut();
}

function editaFilas()
{
    $('#tablaproveedor td').attr('contenteditable','true');

}
function eliminarFilas()
{
    /**
         * Funcion para eliminar la ultima columna de la tabla.
         * Si unicamente queda una columna, esta no sera eliminada
         */
    // Obtenemos el total de columnas (tr) del id "tabla"
            var trs=$('tr', $("#tablaproveedor")).length;
            if(trs>1)
            {
                // Eliminamos la ultima columna
                $("#tablaproveedor td:last").remove();
            }
}

