from django.shortcuts import render
from django.views.generic import CreateView
from .models import Usuario
from .forms import RegistrarseForm

# Create your views here.
class RegistrarseView(CreateView):
    model=Usuario
    template_name='usuarios/registrarse.html'
    form_class = RegistrarseForm
