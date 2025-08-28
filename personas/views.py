from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Persona
from django.db.models import Q  
# Import login mixin if needed
from django.contrib.auth.mixins import LoginRequiredMixin


class PersonaListView(ListView):
    model = Persona
    template_name = 'persona/lista.html'
    context_object_name = 'personas'
    paginate_by = 10  # Número de personas por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Lista de Personas"
        context['search_action'] = 'persona:buscar'
        context['home_url'] = 'persona:lista'
        return context

class PersonaSearchView(ListView):
    model = Persona
    template_name = 'persona/buscar.html'
    context_object_name = 'personas'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Persona.objects.filter(
                Q(nombre__icontains=query)     
            )
        return Persona.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        personas = context['personas']
        if personas.count() == 1:
            persona = personas.first()
            # Agrega la URL de detalle de la primera persona encontrada
            context['detalle_url'] = reverse_lazy('persona:detalle', kwargs={'pk': persona.pk})
        context['titulo'] = "Busqueda de Personas"
        context['home_url'] = 'persona:lista'
        context['search_query'] = self.request.GET.get('q', '')
        return context

class PersonaDetailView(DetailView):
    model = Persona
    template_name = 'persona/detalle.html'
    context_object_name = 'persona'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle de Personas"
        context['home_url'] = 'persona:lista'
        return context
class PersonaCreateView(LoginRequiredMixin, CreateView):
    model = Persona
    template_name = 'persona/crear.html'
    fields = ['nombre', 'apellido', 'edad', 'oficina']
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Persona"
        return context

class PersonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Persona
    template_name = 'persona/crear.html'
    fields = ['nombre', 'apellido', 'edad', 'oficina']
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Persona"
        return context
    
class PersonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Persona
    template_name = 'persona/eliminar.html'
    context_object_name = 'persona'
    success_url = reverse_lazy('persona:lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Borrar Persona"
        context['confirm_message'] = "¿Estás seguro de que quieres eliminar esta persona?"  
        context['cancel_url'] = reverse_lazy('persona:lista')
        return context