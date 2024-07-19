from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ChangePasswordView

# URLConf
urlpatterns = [
    path('register/', views.register, name='register'), # URL de página para cadastro
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # URL de logout com redirecionamento
    path('home/', views.home, name='home'), # view da página inicial
    path('scoreboard/', views.scoreboard, name='scoreboard'),  # URL para o scoreboard
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),   # URL para trocar senha
    path('delete-profile/', views.delete_profile, name='delete_profile')  # URL para deletar usuário 
]