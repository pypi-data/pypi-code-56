import stripe # new
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# Proceso para definir la estructura del pago en stripe
def definir_pago(tituloPago,descr,cantidad,logo,url,debug):

    msj = "Pago Definido Correctamente (url): "
    contexto = {}

    try:
        cantidad_final = cantidad * 100

        logo_final = "img/shop.jpg"
        if logo != None:
            logo_final = logo

        contexto = {
            'tituloPago' : tituloPago,
            'descripcion' : descr + "($"+str(cantidad)+".00 MXN)",
            'key' : settings.STRIPE_PUBLISHABLE_KEY,
            'cantidad' : cantidad,
            'cantidad_final' : cantidad_final,
            'logo' : logo_final,
            'msj' : msj,
            'url' : url,
            'debug' : debug
        }
    except Exception as e:
        contexto['msj'] = str(e)

    return contexto

# Proceso para realizar el pago en stripe
def realizar_pago(request,precio,desc):
    
    resultPay = {
        'titulo' : "Pagos",
        'charge' : "",
        'nombre' : "",
        'cantidad' : "",
        'pagado' : False,
        'recibo' : "",
        'error' : "",
    }

    try:
        if request.method == 'POST':
            token = request.POST['stripeToken']
            charge = stripe.Charge.create(
                amount=precio*100,
                currency="mxn",
                description=desc, 
                source=request.POST['stripeToken']
            )

            resultPay['charge'] = charge
            resultPay['nombre'] = charge.source.name
            resultPay['cantidad'] = charge.amount/100
            resultPay['pagado'] = charge.paid
            resultPay['recibo'] = charge.receipt_url
            resultPay['debug'] = settings.DEBUG

    except Exception as e:
        resultPay['error'] = str(e)
    
    return resultPay
