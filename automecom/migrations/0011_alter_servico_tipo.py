# Generated by Django 5.1.3 on 2025-04-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automecom', '0010_alter_marcacao_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='tipo',
            field=models.ManyToManyField(blank=True, to='automecom.tiposervico'),
        ),
    ]
