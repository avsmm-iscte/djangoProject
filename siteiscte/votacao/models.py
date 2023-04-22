import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
class Questao(models.Model):
        questao_texto =  models.CharField(max_length=200)
        pub_data = models.DateTimeField('data depublicacao')
        def __str__(self):
            return self.questao_texto
        def foi_publicada_recentemente(self):
            return self.pub_data >= timezone.now() - datetime.timedelta(days=1)

class Opcao(models.Model):
        questao = models.ForeignKey(Questao,on_delete=models.CASCADE)
        opcao_texto = models.CharField(max_length=200)
        votos = models.IntegerField(default=0)
        def __str__(self):
            return self.opcao_texto


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    curso = models.CharField(max_length=100)
    nr_votos = models.IntegerField(default=0)
    image = models.TextField()

    def __str__(self):
        return self.user.username

    def add_voto(self):
        self.nr_votos += 1
        self.save()

    def add_image(self, image):
        self.image = image
        self.save()

    def remove_image(self):
        self.delete()
