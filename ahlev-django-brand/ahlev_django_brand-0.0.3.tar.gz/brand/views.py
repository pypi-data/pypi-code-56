from django.shortcuts import render
from django.http import HttpResponse
from .models import Brand

def index(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands
    }
    return render(request, 'brand/index.html', context=context)
