from django.contrib import admin

from .models import Cliente, Endereco, Entrega, ItemEntrega

# Register your models here.

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Entrega)
admin.site.register(ItemEntrega)