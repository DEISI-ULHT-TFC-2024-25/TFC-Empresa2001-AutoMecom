from django import template
from django.contrib.auth.models import AnonymousUser
from ..models import Utilizador

register = template.Library()
@register.filter(name="is_administrador")
def is_administrador(user):
    if isinstance(user, AnonymousUser):
        return False

    try:
        # Tenta obter o objeto Utilizador relacionado ao usuário
        utilizador = Utilizador.objects.get(user=user)
        # Depuração: Verifica se o campo 'administrador' está sendo lido corretamente
        print(f"Usuário {user.username} é administrador: {utilizador.administrador}")
    except Utilizador.DoesNotExist:
        # Se não encontrar, retorna False
        return False

    # Retorna se o campo 'administrador' for True
    return utilizador.administrador
