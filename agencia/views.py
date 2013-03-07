# coding=utf-8
# Create your views here.

from django.shortcuts import render
from trabajo.models import Trabajo, ItemPortfolio
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy

def index(request):
  trabajos = Trabajo.objects.filter(estado='AT').order_by('-fecha_ingreso')[:3]
  portfolio = ItemPortfolio.objects.order_by('-fecha')[:3]
  return render(request,'agencia/index.html', { 'trabajos': trabajos, 'portfolio': portfolio})

def contacto(request):
  return render(request,'agencia/contacto.html')

