"""perimapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('clientes/', views.listaDeClientes, name='clientes'),
    path('clientes/adicionar/', views.ClienteCreate.as_view(), name='create_cliente'),
    path('clientes/delete/<int:pk>/', views.ClienteDelete.as_view(), name='delete_cliente'),
    path('clientes/update/<int:pk>/', views.ClienteUpdate.as_view(),name='update_cliente'),

    path('entregas/', views.EntregaList.as_view(), name='entregas'),
    path('entregas/adicionar', views.CreateEntrega.as_view(), name='create_entrega'),
    path('entregas/delete/<int:pk>/', views.EntregaDelete.as_view(), name='delete_entrega'),
    path('entregas/update/<int:pk>/', views.EntregaUpdate.as_view(), name='update_entrega'),

    path('ajax/load-enderecos/', views.carregarEnderecosByCliente, name='ajax_load_enderecos'),
    path('accounts/', include('django.contrib.auth.urls'))
]