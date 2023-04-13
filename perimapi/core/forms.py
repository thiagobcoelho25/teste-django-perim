from django import forms
from django.forms import inlineformset_factory, modelformset_factory, ModelForm, Select

from .models import Cliente, Endereco, Entrega, ItemEntrega

class EnderecoForm(ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'cidade', 'estado']


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['rua'].error_messages['required'] = 'A rua é obrigatória.'
    #     self.fields['rua'].error_messages['min_length'] = 'A rua deve ter no mínimo 5 caracteres.'
    #     self.fields['rua'].error_messages['max_length'] = 'A rua deve ter no máximo 100 caracteres.'

    #     self.fields['numero'].error_messages['required'] = 'O numero é obrigatório.'

    #     self.fields['cidade'].error_messages['required'] = 'A cidade é obrigatório.'
    #     self.fields['cidade'].error_messages['min_length'] = 'A cidade deve ter no mínimo 3 caracteres.'
    #     self.fields['cidade'].error_messages['max_length'] = 'A cidade deve ter no máximo 100 caracteres.'

    #     self.fields['estado'].error_messages['required'] = 'O estado é obrigatório.'
    #     self.fields['estado'].error_messages['min_length'] = 'O estado deve ter no mínimo 2 caracteres.'
    #     self.fields['estado'].error_messages['max_length'] = 'O estado deve ter no máximo 100 caracteres.'


class ClienteForm(ModelForm):
    model = Cliente

    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'telefone']
    # endereco = EnderecoForm()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['nome'].error_messages['required'] = 'O nome do cliente é obrigatório.'
    #     self.fields['nome'].error_messages['min_length'] = 'O nome do cliente deve ter no mínimo 3 caracteres.'
    #     self.fields['nome'].error_messages['max_length'] = 'O nome do cliente deve ter no máximo 50 caracteres.'

    #     self.fields['cpf'].error_messages['required'] = 'O cpf é obrigatório.'
    #     self.fields['cpf'].error_messages['min_length'] = 'O cpf deve ter no mínimo 11 caracteres.'
    #     self.fields['cpf'].error_messages['max_length'] = 'O cpf deve ter no máximo 11 caracteres.'

    #     self.fields['telefone'].error_messages['required'] = 'O telefone é obrigatório.'
    #     self.fields['telefone'].error_messages['min_length'] = 'O telefone deve ter no mínimo 3 caracteres.'
    #     self.fields['telefone'].error_messages['max_length'] = 'O telefone deve ter no máximo 20 caracteres.'

class EntregaForm(ModelForm):
    class Meta:
        model = Entrega
        fields = ('cliente', 'endereco', 'nome_do_embalador', 'numero_nfce', 'data_compra', 'data_entrega', 'hora_entrega', 'quantidade')
    
    # data_compra = forms.DateField(
    #     widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker', 'placeholder': 'EX: 02/02/2023'}),
    #     input_formats=('%d/%m/%Y')
    #     )

    # data_entrega = forms.DateField(
    #     widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'datepicker', 'placeholder': 'EX: 02/02/2023'}),
    #     input_formats=('%d/%m/%Y')
    #     )
    
        widgets = {
                'data_compra': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'EX: 02/02/2023'}, format='%d/%m/%Y'),
                'data_entrega': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'EX: 02/02/2023'}, format='%d/%m/%Y'),
                }

    hora_entrega = forms.TimeField(required=True,
        widget=forms.TimeInput(format=('%H:%M'), attrs={'type': 'time','placeholder': 'EX: 23:54'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['endereco'].queryset = Endereco.objects.none()
        self.fields['endereco'].label_from_instance = lambda obj: obj.rua
        self.fields['cliente'].label_from_instance = lambda obj: f"{obj.id} - {obj.nome}"
        self.fields['quantidade'].widget.attrs['readonly'] = True
        self.fields['quantidade'].required = False

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['endereco'].queryset = Endereco.objects.filter(cliente_id=cliente_id).order_by('rua')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['endereco'].queryset = self.instance.cliente.enderecos.order_by('rua')



EnderecoFormSet = inlineformset_factory(
    Cliente, Endereco, form=EnderecoForm,
    extra=0, can_delete=True, can_delete_extra=True
)

class ItemEntregaForm(ModelForm):
    class Meta:
        model = ItemEntrega
        fields = ('tipo_volume_extra',)
    

ItemEntregaFormset = inlineformset_factory(Entrega, ItemEntrega, form=ItemEntregaForm, extra=0, can_delete=True, can_delete_extra=True)
# ItemEntregaFormset = modelformset_factory(ItemEntrega, fields=('produto', 'quantidade'), extra=0)