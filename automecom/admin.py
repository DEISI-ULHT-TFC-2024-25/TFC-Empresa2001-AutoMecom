from django.contrib import admin

from automecom.models import Servico, Utilizador, Marcacao, Veiculo, Orcamento, Conselho


# Register your models here.

admin.site.register(Servico)
admin.site.register(Utilizador)
admin.site.register(Marcacao)
admin.site.register(Veiculo)
admin.site.register(Orcamento)
admin.site.register(Conselho)

