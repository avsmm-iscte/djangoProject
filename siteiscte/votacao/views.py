from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Questao, Opcao, Aluno
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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


def creator(request):
    if request.method == 'POST':
        try:
            questao_texto = request.POST.get("texto")
        except KeyError:
             return render(request, 'votacao/Creator.html')
        if questao_texto:
            questao = Questao(questao_texto = questao_texto, pub_data = timezone.now())
            questao.save()
            return HttpResponseRedirect(reverse('votacao:detalhe', args=(questao.id,)))
        else:
            return HttpResponseRedirect(reverse('votacao:Creator'))
    else:
        return render(request, 'votacao/Creator.html')



#optimizar esta parte
def criaropcao(request,questao_id):
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
        return render(request, 'votacao/criaropcao.html',{'questao_id': questao_id})



#parte do login
def registo(request):
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            mail = request.POST.get('mail')
            word = request.POST.get('word')
            curso = request.POST.get('curso')
        except KeyError:
            return render(request, 'votacao/registo.html' )

        if nome and mail and word and curso:
            user = User.objects.create_user(nome, mail, word)
            user.save()
            aluno = Aluno.objects.create(user=user, curso=curso)
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

def eliminarquestao(request):
    questoes = Questao.objects.all()
    return render(request, 'votacao/eliminarquestao.html', {'questoes': questoes})

#nao utilizado, nem o path nem o template, usados so para testes
def eliminar(request):
    try:
        questao_seleccionada = Questao.objects.get(pk=request.POST['questao'])
    except (KeyError, Questao.DoesNotExist):
        # Apresenta de novo o form para votar
        questoes = Questao.objects.all()
        return render(request, 'votacao/eliminarQuestao.html', {'questoes': questoes,  'error_message': "Não escolheu uma opção", })
    else:
        questao_seleccionada.delete()
        # Retorne sempre HttpResponseRedirect depois de
        # tratar os dados POST de um form
        # pois isso impede os dados de serem tratados
        # repetidamente se o utilizador
        # voltar para a página web anterior.
    return HttpResponseRedirect(reverse('votacao:index'))
