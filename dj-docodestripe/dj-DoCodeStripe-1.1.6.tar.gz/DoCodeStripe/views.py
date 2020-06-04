from django.shortcuts import render
# payments/views.py
#import stripe # new

from django.conf import settings

# Libreria para realizar pagos
import DoCodeStripe.procesos.pago as _pago

# class HomePageView(TemplateView):
#     template_name = 'home.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['key'] = settings.STRIPE_PUBLISHABLE_KEY
#         context['titulo'] = "Pagos Django"
#         context['descripcion'] = "Informacion adicional ($15.00 MXN)"
#         context['cantidad'] = 1500
#         context['imagen'] = "img/docode.png"
#         return context


def homePagosStripe_dc(request):
    contexto = {
        'titulo' : "Pagos Django",
        'descripcion' : "descripcion y precio ($15.00 MXN)",
        'key' : settings.STRIPE_PUBLISHABLE_KEY,
        'cantidad' : 1500,
        'imagen' : "img/docode.png",
    }
    return render(request, 'home.html', context=contexto)


def chargeStripe_dc(request): # new
    # realizar_pago(request,precio,descripcion)
    result = _pago.realizar_pago(request,15,"Plataforma-DoCode")

    if result['pagado']:
        return render(request, 'charge.html', context=result)
