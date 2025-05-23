# Generated by Django 5.2 on 2025-05-21 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Membro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('sobrenome', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
