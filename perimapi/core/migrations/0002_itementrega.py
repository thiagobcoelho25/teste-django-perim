# Generated by Django 4.1.7 on 2023-04-12 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemEntrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('produto', models.CharField(max_length=255)),
                ('quantidade', models.PositiveIntegerField()),
                ('entrega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_entrega', to='core.entrega')),
            ],
        ),
    ]
