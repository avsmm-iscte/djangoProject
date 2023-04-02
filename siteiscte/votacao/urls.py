from django.urls import path
from . import views

app_name = 'votacao'
# (. significa que importa views da mesma directoria)
urlpatterns = [
    # ex: votacao /
    path("", views.index, name='index'),
    # ex: votacao/1
    path('<int:questao_id>', views.detalhe, name='detalhe'),
    # ex: votacao/3/resultados
    path('<int:questao_id>/resultados', views.resultados, name='resultados'),
    # ex: votacao/5/voto
    path('<int:questao_id>/voto', views.voto, name='voto'),
    # ex: votacao/criarquestao/
    path('creator', views.creator, name='creator'),

    path('<int:questao_id>/criaropcao', views.criaropcao, name="criaropcao"),

    path('registo', views.registo, name='registo'),

    path('loginpage', views.loginpage, name='loginpage'),

    path('logoutview', views.logoutview, name='logoutview'),

    path('personal', views.personal, name='personal'),

    path('eliminarquestao', views.eliminarquestao, name='eliminarquestao'),

    path('eliminar', views.eliminar, name='eliminar'),

    path('fazer_upload', views.fazer_upload, name='fazer_upload'),

    path('', views.index, name='index'),

]
