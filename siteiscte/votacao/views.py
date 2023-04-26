from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from .models import Questao, Opcao, Aluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import * #(2)
from .models import Questao, Opcao


def index(request):
    latest_question_list = Questao.objects.order_by('-pub_data')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'votacao/index.html', context)


def detalhe(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/detalhe.html', {'questao': questao})


@login_required(login_url='votacao:loginpage')
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])

    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'votacao/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção",
        })
    else:
        if 'eliminaropcao' in request.POST:
            opcao_seleccionada.delete()
            return render(request, 'votacao/detalhe.html', {'questao': questao, })

        if request.user.aluno.nr_votos < 20:
            opcao_seleccionada.votos += 1
            request.user.aluno.add_voto()
            opcao_seleccionada.save()
        else:
            return render(request, 'votacao/detalhe.html', {
                'questao': questao,
                'error_message': "Limite de votos atingido",
            })
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior

    return HttpResponseRedirect(reverse('votacao:resultados', args=(questao.id,)))


def resultados(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    return render(request, 'votacao/resultados.html', {'questao': questao})

@permission_required('auth.superuser', login_url=reverse_lazy('votacao:index'))
def creator(request):
    if request.method == 'POST':
        try:
            questao_texto = request.POST.get("texto")
        except KeyError:
            return render(request, 'votacao/Creator.html')
        if questao_texto:
            questao = Questao(questao_texto=questao_texto, pub_data=timezone.now())
            questao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:Creator'))
    else:
        return render(request, 'votacao/Creator.html')


# optimizar esta parte
def criaropcao(request, questao_id):
    if request.method == 'POST':
        try:
            nome = request.POST.get('novaopcao')
        except KeyError:
            return render(request, 'votacao/criaropcao.html')
        if nome:
            q = Opcao(questao=Questao.objects.all().get(pk=questao_id), opcao_texto=nome)
            q.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao_id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:criaropcao'))
    else:
        return render(request, 'votacao/criaropcao.html', {'questao_id': questao_id})


# parte do login
def registo(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            mail = request.POST.get('mail')
            word = request.POST.get('word')
            curso = request.POST.get('curso')
        except KeyError:
            return render(request, 'votacao/registo.html')

        if nome and mail and word and curso:
            user = User.objects.create_user(nome, mail, word)
            user.save()
            aluno = Aluno.objects.create(user=user, curso=curso, image="")
            aluno.save()
            return HttpResponseRedirect(reverse('votacao:loginpage'))
        else:
            return HttpResponseRedirect(reverse('votacao:registo'))

    else:
        return render(request, 'votacao/registo.html')


def loginpage(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            word = request.POST.get('word')
        except KeyError:
            return render(request, 'votacao/loginpage.html')

        if nome and word:
            user = authenticate(username=nome, password=word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('votacao:index'))
            else:
                return HttpResponseRedirect(reverse('votacao:registo'))
    else:
        return render(request, 'votacao/loginpage.html')


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('votacao:index'))


def personal(request):
    return render(request, 'votacao/personal.html')

@permission_required('auth.superuser', login_url=reverse_lazy('votacao:index'))
def eliminarquestao(request):
    questoes = Questao.objects.all()
    return render(request, 'votacao/eliminarquestao.html', {'questoes': questoes})


def eliminar(request):
    try:
        questao_seleccionada = Questao.objects.get(pk=request.POST['questao'])
    except (KeyError, Questao.DoesNotExist):
        # Apresenta de novo o form para votar
        questoes = Questao.objects.all()
        return render(request, 'votacao/eliminarQuestao.html',
                      {'questoes': questoes, 'error_message': "Não escolheu uma opção", })
    else:
        questao_seleccionada.delete()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:index'))

def fazer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        request.user.aluno.add_image("/votacao/static/votacao/images/" + filename)
        print(request.user.aluno.image)
        uploaded_file_url = fs.url(filename)
        return render(request, 'votacao/fazer_upload.html',
                      {'uploaded_file_url': uploaded_file_url})
    return render(request, 'votacao/fazer_upload.html')



@api_view(['GET', 'POST']) #(3)
def questoes_lista(request):
 if request.method == 'GET': #(4)
    questoes = Questao.objects.all()
    serializerQ = QuestaoSerializer(questoes, context={'request': request}, many=True)
    return Response(serializerQ.data)
 elif request.method == 'POST': #(4)
    serializer = QuestaoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT', 'DELETE']) #(3) e (5)
def questoes_edita(request, pk):
 try:
    questao = Questao.objects.get(pk=pk)
 except Questao.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
 if request.method == 'PUT':
    serializer = QuestaoSerializer(questao,data=request.data,context={'request': request})
    if serializer.is_valid():
          serializer.save()
          return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 elif request.method == 'DELETE':
    questao.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def opcoes_lista(request):
    if request.method == 'GET':
        opcoes = Opcao.objects.all()
        serializerO = OpcaoSerializer(opcoes, context={'request':request}, many=True)
        return Response(serializerO.data)
    elif request.method == 'POST':
        serializer = OpcaoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT', 'DELETE'])
def opcoes_edita(request, pk):
 try:
    opcao = Opcao.objects.get(pk=pk)
 except Opcao.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
 if request.method == 'PUT':
    serializer = OpcaoSerializer(opcao, data=request.data,context={'request': request})
    if serializer.is_valid():
        opcao.votos = opcao.votos + 1
        opcao.save()
        #serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 elif request.method == 'DELETE':
     opcao.delete()
     return Response(status=status.HTTP_204_NO_CONTENT)