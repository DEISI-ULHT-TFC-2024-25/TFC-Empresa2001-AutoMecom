# Generated by Django 5.1.3 on 2025-04-21 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automecom', '0008_orcamento_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='arquivo_pdf',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
