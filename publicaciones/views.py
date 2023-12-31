from typing import Any
from django.shortcuts import render, redirect
from .models import Publicacion, Comentario, Categoria
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse
from .forms import PublicarForm, ComentarioForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import ColaboradorMixin, CreadorMixin
# Crea tus vistas aqui.

'''def Publicaciones_view(request):  #definimos el publicaciones_view y le hacemos un request para que solicite el archivo
 #creamos una variable a la que se le asigan un diccionario que se utilizará para traer los datos de la db
 ctx = {
  'publicaciones' : Publicacion.objects.all() #hacemos la solicitud para que la db nos devuelva todo de la tabla publicaciones
 }

 return render(request, 'publicaciones/publicaciones.html', ctx)''' #retornamos la solicitud y le pedimos que haga el render

#view basada en clase, para enlistar las publicaciones
class PublicacionesView(ListView):
    template_name = 'publicaciones/publicaciones.html'
    model = Publicacion 
    context_object_name = 'publicaciones'
    
    
    
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context ['categorias'] = Categoria.objects.all()
         return context
     
     
    def get_queryset(self):
        queryset = super().get_queryset()
        
        
        
        #filtramos las categorias
        
        categoria_seleccionada = self.request.GET.get('categoria')
        
        if categoria_seleccionada:
            queryset = queryset.filter(categoria = categoria_seleccionada)
            
            
     
        #orden
        
        orden = self.request.GET.get('orderby')
        if orden:
            if orden == 'fecha_asc':
                queryset = queryset.order_by('fecha')
            elif orden == 'fecha_desc':
                queryset = queryset.order_by('-fecha')
            elif   orden == 'fecha_asc':
                queryset = queryset.order_by('titulo')
            elif   orden == 'fecha_desc':
                 queryset = queryset.order_by('-titulo')
      
        return queryset
     

# View basada en clase para CREAR una publicacion.
class Publicar(LoginRequiredMixin, ColaboradorMixin, CreateView):
    model = Publicacion
    template_name = 'publicaciones/publicar.html'
    form_class = PublicarForm

    def form_valid(self, form):
        f = form.save(commit=False) # aca le paro el carro al formulario para que no guarde
        f.creador_id = self.request.user.id
        return super().form_valid(f)
    

    def get_success_url(self):
        return reverse('publicaciones')


# # View basada en clase para que modifiquemos una publicacion.
class ModificarPublicacionView(LoginRequiredMixin, CreadorMixin, UpdateView):
    model = Publicacion
    template_name = 'publicaciones/modificar-publicacion.html'
    form_class = PublicarForm
    success_url = '../ver-publicaciones/'


    
    
# View basada en clase para que eliminemos una publicacion.
class EliminarPublicacionView(LoginRequiredMixin, CreadorMixin, DeleteView):
    model=Publicacion
    template_name='publicaciones/eliminar-publicacion.html'
    success_url = '../ver-publicaciones/'
   
#view para ver a detalle una publicacion
class DetallePublicacion(DetailView):
    model=Publicacion
    template_name = 'publicaciones/detalle.html'
    context_object_name = 'publicacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentarioForm()
        return context


    def post(self, request, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('login')

        publicacion = self.get_object()
        form = ComentarioForm(request.POST)

        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.creador_id = self.request.user.id
            comentario.publicacion = publicacion
            comentario.save()
            return super().get(request)
        else:
            return super().get(request)



class BorrarComentarioView(LoginRequiredMixin, CreadorMixin, DeleteView):
    template_name='comentarios/borrar-comentario.html'
    model=Comentario

    def get_success_url(self):
        return reverse('detalle-publicacion', args=[self.object.publicacion.id])
    
class EditarComentarioView(LoginRequiredMixin, CreadorMixin, UpdateView):
    template_name='comentarios/editar-comentario.html'
    model=Comentario
    form_class = ComentarioForm

    def get_success_url(self):
        return reverse('detalle-publicacion', args=[self.object.publicacion.id])