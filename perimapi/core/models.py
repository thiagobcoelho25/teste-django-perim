from django.db import models

from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    cargo = models.CharField(max_length=11)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '%d: %s %s' % (self.id, self.nome, self.cargo)


class Cliente(models.Model):
    nome = models.CharField(max_length=50, validators=[MinLengthValidator(3), MaxLengthValidator(50)])
    cpf = models.CharField(max_length=11, validators=[MinLengthValidator(11), MaxLengthValidator(11)])
    telefone = models.CharField(max_length=20, validators=[MinLengthValidator(3), MaxLengthValidator(20)])
    
    def __str__(self):
        return 'id: %d (nome: %s, cpf: %s, telefone: %s)' % (self.id, self.nome, self.cpf, self.telefone)

class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='enderecos', on_delete=models.CASCADE)
    rua = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    numero = models.PositiveIntegerField()
    cidade = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    estado = models.CharField(max_length=100, validators=[MinLengthValidator(3), MaxLengthValidator(100)])
    def __str__(self):
        return 'id: %d: (cliente_cpf: %s, rua: %s)' % (self.id, self.cliente.cpf, self.rua)

class Entrega(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='entregas', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    data_entrega = models.DateField()
    quantidade = models.PositiveIntegerField()
    nome_do_embalador = models.CharField(max_length=50)
    numero_nfce = models.CharField(max_length=100)
    data_compra = models.DateField()
    hora_entrega = models.TimeField()

    def __str__(self):
        return '%d: (rua_entrega: %s, cliente_nome: %s, cliente_cpf: %s)' % (self.id, self.endereco.rua, self.cliente.nome, self.cliente.cpf)
    
class ItemEntrega(models.Model):
    entrega = models.ForeignKey(Entrega, on_delete=models.CASCADE, related_name='itens_entrega')
    tipo_volume_extra = models.CharField(max_length=16, choices=[('bebidas', 'Bebidas'), ('frios_congelados', 'Frios/Congelados'),('vassouras_rodo','Vassouras/Rodo'), ('outros', 'Outros')])

    def __str__(self):
        return '%d: (entrega_id: %d, cliente_nome: %s, produto: %s)' % (self.id, self.entrega.id, self.entrega.cliente.nome, self.tipo_volume_extra)

    