from django.urls import path
from . import views
from .views import alterar_estado_marcacao
from django.conf import settings
from django.conf.urls.static import static

app_name = "automecom"
urlpatterns = [
    path('', views.home_view, name="Dashboard"),
    path('home', views.home_view, name="Home"),
    path('servicos', views.servico_view, name="Servico"),
    path('create.html', views.servico_create, name="Create"),
    path('edit/<int:post_id>', views.servico_edit, name='editar'),
    path('delete/<int:post_id>', views.servico_delete, name='apagar'),
    path('conselhos', views.conselho_view, name="Conselho"),
    path('contactos', views.contacto_view, name="Contacto"),
    path('sobre', views.sobre_view, name="Sobre"),
    path('marcacao', views.marcacao_view, name="Marcação"),
    path('login', views.view_login, name="login"),
    path('logout', views.view_logout, name='logout'),
    path('registro', views.register_view, name='register'),
    path('login/registro', views.register_view, name='register'),
    path('perfil', views.perfil_view, name="perfil"),
    path('marcacoes', views.marcacoes_view, name="marcacoes"),
    path('orcamento', views.pedido_orcamento, name='orcamento'),
    path('orcamentos', views.listar_orcamentos, name='orcamentos'),
    # path('marcacao/', views.marcacao_view, name='Marcação'),
    path('editmarc/<int:post_id>', views.marcacao_edit, name='editarmarc'),
    path('editorca/<int:post_id>', views.orcamento_edit, name='editarorca'),
    path('deletemarc/<int:post_id>', views.marcacao_delete, name='apagarmarc'),
    path('marcacao/<int:marcacao_id>/estado/<str:novo_estado>/', alterar_estado_marcacao, name='alterar_estado_marcacao'),
    path('deleteorca/<int:post_id>', views.orcamento_delete, name='apagarorca'),
    path('garantia.html', views.garantia_view, name='garantia'),
    path('privacidade.html', views.privacidade_view, name='privacidade'),
    path('obras.html', views.obras_view, name='obras'),
    path('servicos/', views.servico_view, name='servicos'),
    path('login/conselhos', views.conselho_view, name="Conselho"),
    path('login/contactos', views.contacto_view, name="Contacto"),
    path('login/sobre', views.sobre_view, name="Sobre"),
    path('login/marcacao', views.marcacao_view, name="Marcação"),
    path('login/home', views.home_view, name="Home"),
    path('login/marcacoes', views.marcacoes_view, name="marcacoes"),
    path('login/servicos', views.servico_view, name='servicos'),
    path('login/obras.html', views.obras_view, name='obras'),
    path('login/logout', views.view_logout, name='logout'),
    path('login/orcamento', views.pedido_orcamento, name='orcamento'),
    path('login/registro', views.register_view, name='register'),
    path('login/orcamentos', views.listar_orcamentos, name='orcamentos'),
    path('login/perfil', views.perfil_view, name="perfil"),
    path('login/privacidade.html', views.privacidade_view, name='privacidade'),
    path('login/garantia.html', views.garantia_view, name='garantia'),

]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
