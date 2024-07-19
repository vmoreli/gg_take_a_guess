# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# modelo de perfil de usuário OneToOne com o modelo de usuário padrão
# alterações no modelo do usuário são feitas aqui (como adição do campo 'pontos')
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # OneToOne com usuário padrão
    points = models.IntegerField(default=0) # campo: pontos!

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
