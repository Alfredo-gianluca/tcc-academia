from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

def membros(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

# Create your views here.
