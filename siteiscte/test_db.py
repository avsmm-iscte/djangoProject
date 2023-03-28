from votacao.models import Questao, Opcao

count = 0
for i in Questao.objects.all():
    for j in i.opcao_set.all():
        count += j.votos
print(count)

for questao in Questao.objects.all():
    votos = 0
    votomax = ""
    for opcao in questao.opcao_set.all():
        if opcao.votos >= votos:
            votomax = opcao.opcao_texto
            votos = opcao.votos
    print("Questao: " + questao.questao_texto + " Opcao com mais votos: " + votomax)