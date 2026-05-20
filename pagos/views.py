import random
from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.common.options import WebpayOptions
from transbank.common.integration_commerce_codes import IntegrationCommerceCodes
from transbank.common.integration_api_keys import IntegrationApiKeys
from transbank.common.integration_type import IntegrationType

def obtener_transaccion():
    # Cargamos las credenciales oficiales de Transbank para el entorno de pruebas
    opciones = WebpayOptions(
        IntegrationCommerceCodes.WEBPAY_PLUS,
        IntegrationApiKeys.WEBPAY,
        IntegrationType.TEST
    )
    return Transaction(opciones)

def resumen_pago(request):
    # Pantalla que muestra el plan y el boton de pago
    return render(request, 'pagos/resumen.html')

def iniciar_pago(request):
    # Generamos orden de compra y sesion unicas
    orden_compra = str(random.randrange(1000000, 9999999))
    sesion_id = str(random.randrange(1000000, 9999999))
    monto = 15000 
    
    # URL a la que Transbank enviara la respuesta
    url_retorno = request.build_absolute_uri('/pagos/retorno/')

    # Inicializamos la transaccion con nuestras opciones de prueba
    tx = obtener_transaccion()
    respuesta = tx.create(buy_order=orden_compra, session_id=sesion_id, amount=monto, return_url=url_retorno)

    # Enviamos los datos al formulario invisible que redirige a Webpay
    return render(request, 'pagos/redireccion.html', {
        'token': respuesta['token'],
        'url': respuesta['url']
    })

def retorno_pago(request):
    # Recibimos el token que envia Transbank
    token = request.GET.get('token_ws')

    if not token:
        # Si el usuario cerro la pestana antes de pagar
        return render(request, 'pagos/error.html', {'mensaje': 'El pago fue cancelado o interrumpido.'})

    # Confirmamos la transaccion con Transbank
    tx = obtener_transaccion()
    respuesta = tx.commit(token)

    # Validamos si el pago fue aprobado
    if respuesta['status'] == 'AUTHORIZED':
        # Guardamos el ticket de autorizacion en la sesion
        request.session['pago_exitoso'] = True
        # Redirigimos al registro de clientes
        return redirect('registro')
    else:
        # Pago rechazado
        return render(request, 'pagos/error.html', {'mensaje': 'Tu pago fue rechazado por el banco. Verifica tus fondos e intenta nuevamente.'})