from django.test import TestCase

# Create your tests here.
import random
from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction

def resumen_pago(request):
    # Pantalla antes de saltar a Transbank
    return render(request, 'pagos/resumen.html')

def iniciar_pago(request):
    # Transbank exige una orden de compra y un ID de sesión únicos por cada transacción
    orden_compra = str(random.randrange(1000000, 9999999))
    sesion_id = str(random.randrange(1000000, 9999999))
    monto = 15000  # Monto fijo para pruebas

    # Transbank requiere una URL de retorno para redirigir al usuario después del pago
    url_retorno = request.build_absolute_uri('/pagos/retorno/')

    # Inicializamos la transacción con el SDK oficial (usa credenciales de prueba por defecto)
    tx = Transaction()
    respuesta = tx.create(buy_order=orden_compra, session_id=sesion_id, amount=monto, return_url=url_retorno)

    # Enviamos el token y la URL a una plantilla invisible que hará el redireccionamiento
    return render(request, 'pagos/redireccion.html', {
        'token': respuesta['token'],
        'url': respuesta['url']
    })

def retorno_pago(request):
    # Transbank nos devuelve por la URL el token de la transacción
    token = request.GET.get('token_ws')

    if not token:
        # Si el usuario cerró la pestaña o anuló la compra
        return render(request, 'pagos/error.html', {'mensaje': 'El pago fue cancelado.'})

    # Le confirmamos a Transbank que recibimos al usuario de vuelta
    tx = Transaction()
    respuesta = tx.commit(token)

    # Validamos si la tarjeta fue aprobada
    if respuesta['status'] == 'AUTHORIZED':
        # ¡EL TICKET DORADO! Guardamos en sesión que esta persona sí pagó
        request.session['pago_exitoso'] = True
        # Redirigimos automáticamente al formulario de registro que ya tienes
        return redirect('registro')
    else:
        # Si la tarjeta fue rechazada (sin fondos, etc.)
        return render(request, 'pagos/error.html', {'mensaje': 'Tu pago fue rechazado por el banco.'})