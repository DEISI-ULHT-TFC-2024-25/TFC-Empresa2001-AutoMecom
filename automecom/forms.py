from datetime import datetime, date, timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .models import Servico, Utilizador, Veiculo, Marcacao, TipoServico, Orcamento
from .widget import DatePickerInput, TimePickerInput


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['tipo', 'nome', 'descricao']


class TipoServicoForm(forms.ModelForm):
    class Meta:
        model = TipoServico
        fields = ['nome']


class RegisterForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Número de Telefone'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'telefone', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # Atribuindo placeholders aos campos
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome próprio'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Apelido'
        self.fields['email'].widget.attrs['placeholder'] = 'E-mail'
        self.fields['telefone'].widget.attrs['placeholder'] = 'Número de Telefone'
        self.fields['password1'].widget.attrs['placeholder'] = 'Palavra passe'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

        # Adicionando ajuda aos campos
        self.fields['username'].help_text = '150 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'
        self.fields['password1'].help_text = 'Sua senha deve conter pelo menos 8 caracteres.'
        self.fields['password2'].help_text = 'Digite a mesma senha de antes, para verificação.'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = '50 caracteres ou menos. Somente letras, dígitos e @/./+/-/_.'


class UtilizadorForm(forms.ModelForm):
    class Meta:
        model = Utilizador
        fields = ['user', 'administrador']


class PasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customizando os placeholders
        self.fields['old_password'].widget.attrs['placeholder'] = 'Senha atual'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Repita a nova senha'

        # Customizando os help texts
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].help_text = ''

        # Opcional: alterando as labels
        self.fields['old_password'].label = 'Senha Atual'
        self.fields['new_password1'].label = 'Nova Senha'
        self.fields['new_password2'].label = 'Confirmação da Nova Senha'


class VeiculoForm(forms.ModelForm):
    matricula = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: AB-12-CD'})
    )

    class Meta:
        model = Veiculo
        fields = ['marca', 'modelo', 'ano', 'matricula', 'kms']
        widgets = {
            'marca': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite Marca do veículo', 'style': 'width: 300px;'}),
            'modelo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Digite o modelo do veículo', 'style': 'width: 300px;'}),
            'ano': forms.Select(
                attrs={'class': 'form-control', 'placeholder': 'Selecione o ano do veículo', 'style': 'width: 100px;'},
                choices=[(year, year) for year in range(datetime.now().year, 1980, -1)]),
            'kms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a quilometragem (kms)',
                                          'style': 'width: 100px;'}),
        }


class ContatoForm(forms.Form):
    primeiro_nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Primeiro Nome", "class": "form-control"}),
    )
    ultimo_nome = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Último Nome", "class": "form-control"}),
    )
    telemovel = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "Telemóvel", "class": "form-control"}),
        required=False,  # Caso não seja obrigatório
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "E-mail", "class": "form-control"}),
    )
    mensagem = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Escreva sua mensagem aqui", "class": "form-control"}),
    )


from django import forms
from datetime import datetime, timedelta
from datetime import date
from .models import Servico  # Certifique-se de que o modelo 'Servico' está sendo importado corretamente

class MarcacaoForm(forms.Form):
    nome = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu primeiro nome'})
    )
    apelido = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu sobrenome'})
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu e-mail'})
    )

    servicos = forms.MultipleChoiceField(
        choices=[(servico.id, servico.nome) for servico in Servico.objects.all()],
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
    )

    descricao = forms.CharField(
        label="Descrição",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva a situação'}),
    )

    data = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'min': date.today().isoformat(), 'placeholder': 'Selecione a data'})
    )

    hora = forms.ChoiceField(
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[]  # Inicialmente sem escolhas, será preenchido no __init__
    )

    imagem = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label="Imagem (opcional)"
    )

    def __init__(self, *args, **kwargs):
        super(MarcacaoForm, self).__init__(*args, **kwargs)

        # Gerar horários com incrementos de 10 minutos
        horarios = []
        inicio = datetime.strptime("08:00", "%H:%M")  # Hora inicial (exemplo: 08:00)
        fim = datetime.strptime("18:00", "%H:%M")  # Hora final (exemplo: 18:00)

        while inicio <= fim:
            horarios.append(inicio.strftime("%H:%M"))
            inicio += timedelta(minutes=10)

        # Adicionar os horários gerados ao campo de hora
        self.fields['hora'].choices = [(hora, hora) for hora in horarios]

    def clean_data(self):
        data = self.cleaned_data.get("data")
        if data and data < date.today():
            raise forms.ValidationError("A data não pode ser anterior à data atual.")
        return data

    def clean_hora(self):
        hora = self.cleaned_data['hora']
        data = self.cleaned_data.get('data')
        if data == date.today():
            agora = datetime.now().time()
            if datetime.strptime(hora, "%H:%M").time() <= agora:
                raise forms.ValidationError("A hora não pode estar no passado.")
        return hora


class MarcacaoEditForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'servicos', 'imagem', 'data', 'descricao', 'hora',
                  'orcamento', 'observacoes', 'fatura']

class OrcamentoEditForm(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'servicos', 'data', 'descricao', 'hora',
                  'observacoes']


class MarcacaoEditFormClient(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'imagem', 'servicos', 'data', 'hora', 'descricao']

class OrcamentoEditFormClient(forms.ModelForm):
    class Meta:
        model = Marcacao
        fields = ['nome', 'apelido', 'email', 'servicos', 'data', 'hora', 'descricao']

class OrcamentoForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu primeiro nome'})
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o seu e-mail'})
    )
    telefone = forms.CharField(
      max_length=9,
      min_length=9,
      required=True,
      validators=[RegexValidator(regex=r'^\d{9}$', message="O telefone deve conter exatamente 9 números.")],
      widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 912345678'})
    )

    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.all(),
        required=True,
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'})
    )
    descricao = forms.CharField(
        label="Descrição",
        max_length=500,
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descreva a situação'})
    )
    data = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Selecione a data'})
    )
    hora = forms.TimeField(
        required=True,
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Selecione a hora'})
    )

    class Meta:
        model = Orcamento  # Especifica o modelo associado
        fields = ['nome', 'email', 'descricao', 'data', 'hora', 'servicos','arquivo_pdf']
