from audioop import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Cliente, Endereco, Entrega

from .forms import (ClienteForm, EntregaForm, EnderecoFormSet, ItemEntregaFormset)
from django.contrib import messages



# Create your views here.

######### CLIENTES #########
@login_required
def listaDeClientes(request):

    clientes = Cliente.objects.all()

    context = {'clientes': clientes}

    return render(request, 'lista_clientes.html', context)

@method_decorator(login_required, name="dispatch")
class ClienteCreate(CreateView):
    form_class = ClienteForm
    template_name = "formulario_cliente.html"

    def get_context_data(self, **kwargs):
        context = super(ClienteCreate, self).get_context_data(**kwargs)
        context['endereco_formset'] = EnderecoFormSet()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        endereco_formset = EnderecoFormSet(self.request.POST)
        if form.is_valid() and endereco_formset.is_valid():
            return self.form_valid(form, endereco_formset)
        else:
            return self.form_invalid(form, endereco_formset)

    def form_valid(self, form, endereco_formset):
        self.object = form.save(commit=False)
        
        with transaction.atomic():
            self.object.save()

            # saving ProductMeta Instances
            enderecos = endereco_formset.save(commit=False)
            for meta in enderecos:
                meta.cliente = self.object
                meta.save()
        return redirect(to="/clientes")

    def form_invalid(self, form, endereco_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  endereco_formset=endereco_formset
                                  )
        )

@method_decorator(login_required, name="dispatch")
class ClienteDelete(DeleteView):
    model = Cliente
    template_name = "cliente_confirm_delete.html"
    success_url = reverse_lazy('clientes')

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(ClienteDelete, self).form_valid(form)

@method_decorator(login_required, name="dispatch")
class ClienteUpdate(UpdateView):
    model = Cliente
    template_name = "formulario_cliente.html"
    form_class = ClienteForm
    success_url = reverse_lazy('clientes')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['endereco_formset'] = EnderecoFormSet(self.request.POST, instance=self.object) #EnderecoInlineFormSet
        else:
            data['endereco_formset'] = EnderecoFormSet(instance=self.object) #EnderecoInlineFormSet
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        endereco_formset = context['endereco_formset']
        with transaction.atomic():
            self.object = form.save()

            if endereco_formset.is_valid():
                endereco_formset.instance = self.object
                endereco_formset.save()
        
        messages.success(self.request, "The task was updated successfully.")
        return super(ClienteUpdate, self).form_valid(form)


######### ENTREGAS #########
@method_decorator(login_required, name="dispatch")
class EntregaList(ListView):
    model = Entrega
    context_object_name = 'entregas'
    template_name = 'lista_entregas.html'

@method_decorator(login_required, name="dispatch")
class CreateEntrega(CreateView):
    model = Entrega
    form_class = EntregaForm
    template_name = "formulario_entrega.html"
    success_url = reverse_lazy('entregas')

    def get_context_data(self, **kwargs):
        context = super(CreateEntrega, self).get_context_data(**kwargs)
        context['item_formset'] = ItemEntregaFormset()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        item_formset = ItemEntregaFormset(self.request.POST)

        if form.is_valid() and item_formset.is_valid():
            return self.form_valid(form, item_formset)
        else:
            print(form.errors)
            return self.form_invalid(form, item_formset)

    def form_valid(self, form, item_formset):
        self.object = form.save(commit=False)

        with transaction.atomic():
            self.object.quantidade = 0
            self.object.save()

            # saving ProductMeta Instances
            itens = item_formset.save(commit=False)
            for meta in itens:
                meta.entrega = self.object
                meta.save()

                self.object.quantidade += 1
            
            self.object.save()
        
            
        return redirect(to="/entregas")

    def form_invalid(self, form, item_formset):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  item_formset=item_formset
                                  )
        )
    

def carregarEnderecosByCliente(request):
    cliente_id = request.GET.get('cliente')
    enderecos = Endereco.objects.filter(cliente_id=cliente_id).order_by('rua')
    return render(request, 'endereco_dropdown_list_options.html', {'enderecos': enderecos})

@method_decorator(login_required, name="dispatch")
class EntregaUpdate(UpdateView):
    model = Entrega
    template_name = "formulario_entrega.html"
    form_class = EntregaForm
    success_url = reverse_lazy('entregas')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['item_formset'] = ItemEntregaFormset(self.request.POST, instance=self.object) #EnderecoInlineFormSet
        else:
            data['item_formset'] = ItemEntregaFormset(instance=self.object) #EnderecoInlineFormSet
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        with transaction.atomic():
            self.object.quantidade = 0
            self.object = form.save()

            if item_formset.is_valid():
                item_formset.instance = self.object
                item_saved = item_formset.save()
            
            for item in item_formset:
                if not item.cleaned_data.get('DELETE', False):
                    self.object.quantidade += 1

            self.object.save()
        
        messages.success(self.request, "The task was updated successfully.")
        return super(EntregaUpdate, self).form_valid(form)

@method_decorator(login_required, name="dispatch")
class EntregaDelete(DeleteView):
    model = Entrega
    template_name = "entrega_confirm_delete.html"
    success_url = reverse_lazy('entregas')

    def form_valid(self, form):
        messages.success(self.request, "The task was deleted successfully.")
        return super(EntregaDelete, self).form_valid(form)


# def adicionarCliente(request):
#     if request.method == 'GET':
#         form = FormularioCriarCliente()
#         context = {'form': form}
#         return render(request, 'formulario_cliente.html', context)
#     else:
#         form = FormularioCriarCliente(request.POST)
#         if form.is_valid():
#             print("FORMULARIO VALIDO!!!!")
#             cliente = form.save(commit=False)
#             endereco_form = FormularioCriarEnderecoForm(request.POST, instance=cliente.endereco)
#             if endereco_form.is_valid():
#                 endereco = endereco_form.save()
#                 cliente.endereco = endereco
#                 cliente.save()
#                 # redirecionar para outra página
#         else:
#             return render(request, 'formulario_cliente.html', {'form': form})
