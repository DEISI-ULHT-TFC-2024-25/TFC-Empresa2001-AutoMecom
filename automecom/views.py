from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ServicoForm, UtilizadorForm, UserForm, PasswordForm, RegisterForm, MarcacaoForm, VeiculoForm, \
    MarcacaoEditForm, MarcacaoEditFormClient
from .models import Servico, Utilizador, Veiculo, Marcacao
from django import template

from .templatetags.custom_tags import is_administrador

register = template.Library()


def is_superuser(user):
    return user.is_superuser


def home_view(request):
    return render(request, 'automecom/home.html')


@login_required
def view_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('automecom:Home'))




def view_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('automecom:Home'))
        else:
            return render(request, 'automecom/login.html', {
                'message': 'Credenciais invalidas.'
            })

    return render(request, 'automecom/login.html')


def servico_view(request):
    servicos = Servico.objects.all()
    return render(request, 'automecom/servico.html', {
        'servicos': servicos,
        'administrador': is_administrador(request.user)
    })


def servico_create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))

    if not is_administrador(request.user):
        return HttpResponseRedirect(reverse('automecom:Home'))

    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:Servico'))
    form = ServicoForm()

    context = {'form': form}
    return render(request, 'automecom/create.html', context)


def servico_edit(request, post_id):
    if not is_administrador(request.user):
        return HttpResponseRedirect(reverse('automecom:Home'))

    post = Servico.objects.get(id=post_id)
    if request.method == 'POST':
        form = ServicoForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:Servico'))
    else:
        form = ServicoForm(instance=post)
    context = {'form': form, 'post_id': post_id}
    return render(request, 'automecom/edit.html', context)


@login_required
def servico_delete(request, post_id):
    if Servico.objects.filter(pk=post_id).exists():
        Servico.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:Servico'))


def conselho_view(request):
    return render(request, 'automecom/conselhos.html')


def contacto_view(request):
    return render(request, 'automecom/contactos.html')


def garantia_view(request):
    return render(request, 'automecom/garantia.html')


def privacidade_view(request):
    return render(request, 'automecom/privacidade.html')


from django.core.exceptions import ObjectDoesNotExist

def obras_view(request):
    if not Utilizador.objects.filter(user=request.user).exists():
        # Redirecionar para a página inicial ou outra página
        return HttpResponseRedirect(reverse('automecom:Home'))

    utilizador = Utilizador.objects.get(user=request.user)
    context = {
        "marcacoes": Marcacao.objects.filter(utilizador_id=utilizador),
        "estado": Marcacao.estado,
        "data": Marcacao.data,
        "hora": Marcacao.hora,
    }

    if is_administrador(request.user):
        context = {
            "marcacoes": Marcacao.objects.all(),
            "estado": Marcacao.estado,
            "data": Marcacao.data,
            "hora": Marcacao.hora,
        }

    return render(request, 'automecom/obras.html', context)


def sobre_view(request):
    return render(request, 'automecom/sobre.html')


def marcacoes_view(request):
    try:
        utilizador = Utilizador.objects.get(user=request.user)
    except Utilizador.DoesNotExist:
        utilizador = Utilizador.objects.create(user=request.user)



    context = {
        "marcacoes": Marcacao.objects.filter(utilizador_id=utilizador),
        "estado": Marcacao.estado,
        "descricao": Marcacao.descricao,
        "data": Marcacao.data,
        "hora": Marcacao.hora,
    }

    if is_administrador(request.user):

        context = {
            "marcacoes": Marcacao.objects.all(),
            "estado": Marcacao.estado,
            "descricao": Marcacao.descricao,
            "data": Marcacao.data,
            "hora": Marcacao.hora,
            "fatura": Marcacao.fatura,
        }
    return render(request, 'automecom/marcacoes.html', context)



def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'automecom/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username  # Isso parece redundante
            user.save()


            utilizador = Utilizador(user=user)
            utilizador.save()

            login(request, user)  # Faz o login automaticamente após o registro
            return redirect('automecom:Home')
        else:
            return render(request, 'automecom/register.html', {'form': form})

from django.core.exceptions import ObjectDoesNotExist

def perfil_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))

    try:
        post = Utilizador.objects.get(user=request.user)
    except ObjectDoesNotExist:
        # Você pode redirecionar o usuário ou criar um novo objeto Utilizador
        return HttpResponseRedirect(reverse('automecom:Home'))  # Ou outra página

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=request.user)
        form2 = UtilizadorForm(request.POST, request.FILES, instance=post)
        form3 = PasswordForm(request.user, request.POST)
        if form.is_valid() and form2.is_valid() and form3.is_valid():
            form.save()
            form2.save()
            form3.save()
            return HttpResponseRedirect(reverse('automecom:perfil'))
    else:
        form = UserForm(instance=request.user)
        form2 = UtilizadorForm(instance=post)
        form3 = PasswordForm(request.user)

    context = {'form': form, 'form2': form2, 'form3': form3}
    return render(request, 'automecom/perfil.html', context)


@login_required
def utilizador_delete(request, post_id):
    if Utilizador.objects.filter(pk=post_id).exists():
        logout(request)
        Utilizador.objects.get(pk=post_id).user.delete()
    return HttpResponseRedirect(reverse('automecom:Home'))


def marcacao_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('automecom:login'))

    if request.method == 'GET':
        form = MarcacaoForm()
        form2 = VeiculoForm()
        if request.user.is_authenticated:
            del form.fields['nome']
            del form.fields['apelido']
            del form.fields['email']
        return render(request, 'automecom/marcacao.html', {'form': form, 'form2': form2})

    if request.method == 'POST':
        form = MarcacaoForm()
        form2 = VeiculoForm(request.POST)
        if form2.is_valid():
            veiculo = form2.save()
            if request.user.is_authenticated:
                marcacao = Marcacao(
                    nome=request.user.first_name,
                    apelido=request.user.last_name,
                    email=request.user.email,
                    telefone=request.POST['telefone'],
                    veiculo=veiculo,
                    data=request.POST['data'],
                    hora=request.POST['hora'],
                    descricao=request.POST['descricao']
                )
                utilizador = Utilizador.objects.get(user=request.user)
                marcacao.utilizador = utilizador
                marcacao.save()

                # Adicionar os serviços à marcação
                servicos_ids = request.POST.getlist('servicos')  # Obtém os IDs dos serviços
                marcacao.servicos.set(servicos_ids)  # Define os serviços usando o método set()
            else:
                marcacao = Marcacao(
                    nome=request.POST['nome'],
                    apelido=request.POST['apelido'],
                    email=request.POST['email'],
                    telefone=request.POST['telefone'],
                    veiculo=veiculo,
                    data=request.POST['data'],
                    hora=request.POST['hora'],
                    descricao=request.POST['descricao']
                )
                marcacao.save()

                # Adicionar os serviços à marcação
                servicos_ids = request.POST.getlist('servicos')  # Obtém os IDs dos serviços
                marcacao.servicos.set(servicos_ids)  # Define os serviços usando o método set()

            return redirect('automecom:marcacoes')
        else:
            return render(request, 'automecom/marcacao.html', {'form': form, 'form2': form2})


def marcacao_edit(request, post_id):
    post = get_object_or_404(Marcacao, id=post_id)

    # Verifica se o usuário tem permissão para editar
    if not is_administrador(request.user) and post.utilizador.user != request.user:
        return HttpResponseRedirect(reverse('automecom:Home'))

    # POST: Atualizar os dados
    if request.method == 'POST':
        if is_administrador(request.user):
            form = MarcacaoEditForm(request.POST, request.FILES, instance=post)
        else:
            form = MarcacaoEditFormClient(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "A marcação foi alterada com sucesso!")
            return HttpResponseRedirect(reverse('automecom:marcacoes'))
        else:
            # Retornar o formulário com erros se não for válido
            print(form.errors)  # Loga os erros no console
            messages.error(request, "Erro ao salvar a marcação. Por favor, corrija os erros abaixo.")
            context = {'form': form, 'post_id': post_id}
            return render(request, 'automecom/editmarcacao.html', context)

    # GET: Exibir o formulário com os dados atuais
    else:
        if is_administrador(request.user):
            form = MarcacaoEditForm(instance=post)
        else:
            form = MarcacaoEditFormClient(instance=post)
        context = {'form': form, 'post_id': post_id}
        return render(request, 'automecom/editmarcacao.html', context)


def marcacao_delete(request, post_id):
    if Marcacao.objects.filter(pk=post_id).exists():
        Marcacao.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:marcacoes'))


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def enviar_email(request):
    if request.method == 'POST':
        nome = request.POST.get('name')
        email = request.POST.get('email')
        mensagem = request.POST.get('message')

        # Formatar a mensagem do e-mail
        assunto = f"Mensagem de {nome} através do site"
        corpo_mensagem = f"Nome: {nome}\nEmail: {email}\n\nMensagem:\n{mensagem}"

        # Enviar o e-mail
        try:
            send_mail(
                assunto,  # Assunto
                corpo_mensagem,  # Corpo do email
                email,  # De
                ['geral@automecom.com'],  # Para
                fail_silently=False,
            )
            messages.success(request, 'Sua mensagem foi enviada com sucesso!')
        except Exception as e:
            messages.error(request, 'Houve um erro ao enviar sua mensagem. Tente novamente.')

        return redirect('nome_da_pagina_de_contato')  # Redireciona de volta à página de contatos

    return render(request, 'caminho_para_o_template.html')


def marcacao(request):
    return render(request, 'automecom/marcacao.html')


def contact(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            nome = request.user.get_full_name() or request.user.username
            email = request.user.email
        else:
            nome = request.POST.get("Pnome", "") + " " + request.POST.get("Unome", "")  # Nome completo do formulário
            email = request.POST.get("email", "")  # E-mail do formulário
            telemovel = request.POST.get("telemovel", "")  # Telefone do formulário

        mensagem = request.POST.get("mensagem", "")  # Mensagem do formulário

        # Construção do corpo do e-mail
        corpo_email = f"""
        Nome: {nome}
        E-mail: {email}
        Telefone: {telemovel}

        Mensagem:
        {mensagem}
        """

        # Enviar o e-mail usando o e-mail fixo (definido como remetente)
        send_mail(
            subject=f"Nova mensagem de {nome}",
            message=corpo_email,
            from_email="envioemailautomecom@gmail.com",  # E-mail de envio fixo
            recipient_list=["geral@automecom.com"],  # E-mail da empresa que recebe a mensagem
        )

        # Exibir uma mensagem de sucesso
        messages.success(request, "Sua mensagem foi enviada com sucesso!")

    return render(request, "automecom/contact.html")