from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import ServicoForm, UtilizadorForm, UserForm, PasswordForm, RegisterForm, MarcacaoForm, VeiculoForm, \
    MarcacaoEditForm, MarcacaoEditFormClient, OrcamentoForm, OrcamentoEditForm, OrcamentoEditFormClient, ContatoForm
from .models import Servico, Utilizador, Veiculo, Marcacao, Orcamento
from django import template

from .templatetags.custom_tags import is_administrador

register = template.Library()


def is_superuser(user):
    return user.is_superuser


def home_view(request):
    return render(request, 'automecom/home.html')


def listar_orcamentos(request):

    utilizador = Utilizador.objects.get(user=request.user)

    # Se o usuário for administrador, mostra todos os pedidos
    if is_administrador(request.user):
        orcamentos = Orcamento.objects.all()
    # Se for um cliente autenticado, mostra apenas os pedidos dele
    elif request.user.is_authenticated:
        orcamentos = Orcamento.objects.filter(user=request.user)
        print(f"Orçamentos do cliente {request.user.username}: {orcamentos}")  # Debug

    else:
        orcamentos = None  # Define como None para evitar erros
        messages.error(request, "Você precisa fazer login para acessar esta página.")
        return redirect('automecom:login')  # Substitua pelo nome correto da view de login

    return render(request, 'automecom/orcamentos.html', {
        'orcamentos': orcamentos
    })

def pedido_orcamento(request):
    # Criar instâncias dos formulários
    form = OrcamentoForm(request.POST or None)
    veiculo_form = VeiculoForm(request.POST or None)

    # Se o usuário estiver logado, não exigir os campos de nome e email

    if request.user.is_authenticated:
        form.fields['nome'].required = False
        form.fields['email'].required = False
        form.fields['telefone'].required = False
    else:
        form.fields['nome'].required = True
        form.fields['email'].required = True
        form.fields['telefone'].required = True


    if request.method == 'POST':
        if form.is_valid() and veiculo_form.is_valid():
            # Salvar o orçamento
            orcamento = form.save(commit=False)
            orcamento.veiculo = veiculo_form.save()  # Associar o veículo ao orçamento

            if request.user.is_authenticated:
                orcamento.user = request.user

            orcamento.save()
            form.save_m2m()
            messages.success(request, "Pedido enviado com sucesso!")  # Mensagem de sucesso
            return redirect('automecom:orcamentos')  # Redireciona após o envio

    return render(request, 'automecom/orcamento.html', {
        'form': form,
        'veiculo_form': veiculo_form
    })

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
    form = ContatoForm(request.POST)
    if request.method == "POST":
        if request.user.is_authenticated:

            primeiro_nome = request.user.first_name
            ultimo_nome = request.user.last_name
            email = request.user.email
            telemovel = request.POST.get("telemovel", "")
            mensagem = request.POST.get("mensagem", "")
            print(primeiro_nome)
            print(email)
            print(mensagem)

            # Verificação de campos obrigatórios
            if not mensagem.strip():
                messages.error(request, "Por favor preencha todos os campos obrigatórios.")
                return redirect("automecom:Contacto")  # ou render(request, "...", {...}) se quiseres manter os dados

            # Corpo do e-mail
            corpo_email = f"""
               Nome: {primeiro_nome + " " + ultimo_nome}
               E-mail: {email}
               Telefone: {telemovel}

               Mensagem:
               {mensagem}
               """

            # Enviar e-mail
            send_mail(
                subject=f"Nova mensagem de {primeiro_nome} {ultimo_nome}",
                message=corpo_email,
                from_email="envioemailautomecom@gmail.com",
                recipient_list=["beatrizmneves@gmail.com"],
            )

            print("a bia vai passar")
            messages.success(request, "Sua mensagem foi enviada com sucesso!")
        else:
            primeiro_nome = request.POST.get("primeiro_nome", "")
            ultimo_nome = request.POST.get("ultimo_nome", "")
            email = request.POST.get("email", "")
            telemovel = request.POST.get("telemovel", "")
            mensagem = request.POST.get("mensagem", "")
            print(primeiro_nome)
            print(email)
            print(mensagem)

            # Verificação de campos obrigatórios
            if not mensagem.strip():
                messages.error(request, "Por favor preencha todos os campos obrigatórios.")
                return redirect("automecom:Contacto")  # ou render(request, "...", {...}) se quiseres manter os dados

            # Corpo do e-mail
            corpo_email = f"""
               Nome: {primeiro_nome + " " + ultimo_nome}
               E-mail: {email}
               Telefone: {telemovel}

               Mensagem:
               {mensagem}
               """

            # Enviar e-mail
            send_mail(
                subject=f"Nova mensagem de {primeiro_nome} {ultimo_nome}",
                message=corpo_email,
                from_email="envioemailautomecom@gmail.com",
                recipient_list=["beatrizmneves@gmail.com"],
            )

            print("a bia vai passar")
            messages.success(request, "Sua mensagem foi enviada com sucesso!")


        # return redirect("automeom:contactos")  # para limpar o formulário após envio

    return render(request, "automecom/contactos.html", {'form': form})


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
    # Obter o utilizador logado
    utilizador = Utilizador.objects.get(user=request.user)

    filtro = request.GET.get('filtro', 'todos')  # Padrão é 'todos'


    if is_administrador(request.user):
        marcacoes = Marcacao.objects.all().order_by('data', 'hora')
    else:
        marcacoes = Marcacao.objects.filter(utilizador=utilizador).order_by('data', 'hora')
    if filtro != 'todos':
        marcacoes = marcacoes.filter(estado=filtro)

        # Passar as marcações e outros dados necessários para o contexto
    context = {
        "marcacoes": marcacoes,
        "filtro": filtro,  # Passando o filtro para o template
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
            user.username = user.username
            utilizador = Utilizador()
            utilizador.nome = user.username
            utilizador.user = user
            user.telefone = form.cleaned_data['telefone']

            user.save()
            utilizador.save()
            login(request, user)
            return redirect('automecom:Home')
        else:
            return render(request, 'automecom/register.html', {'form': form})


def perfil_view(request):

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('automecom:login'))

        # Verifica se o Utilizador existe, e se não, cria um novo ou apenas prossegue
        post, created = Utilizador.objects.get_or_create(user=request.user)

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
                    imagem=request.POST['imagem'],
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
                    imagem=request.POST['imagem'],
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



def alterar_estado_marcacao(request, marcacao_id, novo_estado):
    if not is_administrador(request.user):
        return HttpResponseForbidden("Acesso negado.")

    print("bia")
    marcacao = get_object_or_404(Marcacao, id=marcacao_id)
    print(marcacao_id)
    if novo_estado == "Aceite":
        print("aceitou")
        marcacao.estado = "Confirmado"
        marcacao.save()
    else:
        print("recusado")
        marcacao.estado = "Recusado"
        marcacao.save()

    return redirect('automecom:marcacoes')


def orcamento_edit(request, post_id):
    post = get_object_or_404(Orcamento, id=post_id)

    # Verifica se o usuário tem permissão para editar
    if not is_administrador(request.user) and post.user != request.user:
        return HttpResponseRedirect(reverse('automecom:Home'))

    # POST: Atualizar os dados
    if request.method == 'POST':
        if is_administrador(request.user):
            form = OrcamentoEditForm(request.POST, request.FILES, instance=post)
        else:
            form = OrcamentoEditFormClient(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('automecom:orcamentos'))
        else:
            # Retornar o formulário com erros se não for válido
            print(form.errors)  # Loga os erros no console
            messages.error(request, "Erro ao salvar o orçamento. Por favor, corrija os erros abaixo.")
            context = {'form': form, 'post_id': post_id}
            return render(request, 'automecom/editorcamento.html', context)

    # GET: Exibir o formulário com os dados atuais
    else:
        if is_administrador(request.user):
            form = OrcamentoEditForm(instance=post)
        else:
            form = OrcamentoEditFormClient(instance=post)
        context = {'form': form, 'post_id': post_id}
        return render(request, 'automecom/editorcamento.html', context)


def marcacao_delete(request, post_id):
    if Marcacao.objects.filter(pk=post_id).exists():
        Marcacao.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:marcacoes'))

def orcamento_delete(request, post_id):
    if Orcamento.objects.filter(pk=post_id).exists():
        Orcamento.objects.get(pk=post_id).delete()
    return HttpResponseRedirect(reverse('automecom:orcamentos'))


from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages



def marcacao(request):
    return render(request, 'automecom/marcacao.html')

