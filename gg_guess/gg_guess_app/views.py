from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Country
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib import messages
import requests
import random

# Create your views here.
# views in django - request handlers (actions, in other frameworks)

# Função que faz o acesso à API e devolve um país aleatório que não esteja nos países já acertados por um usuário
def get_random_country(excluded_countries):
    # excluded countries : lista de países que o usuário já acertou e que, portanto, não devem ser mais selecionados
    url = "https://restcountries.com/v3.1/all"  # url da API p/ pegar todos os países
    response = requests.get(url)    
    if response.status_code == 200: # se o pedido foi bem sucedido
        data = response.json()
        # da lista de todos os países, exclui os que estão em excluded_countries
        available_countries = [country for country in data if country['name']['common'] not in excluded_countries]
        return random.choice(available_countries)   # retorna país aleatório dentre os disponíveis
    return None

# View da home
def home(request):

    # se o método é POST e o usuário está autenticado -> palpite foi feito para o jogo
    if request.method == 'POST' and request.user.is_authenticated:
        # Pega pontos do usuário para imprimir na tela
        profile = UserProfile.objects.get(user=request.user)
        points = profile.points

        # Atualiza número de palpites feitos
        guesses = request.session['guesses'] + 1
        request.session['guesses'] = guesses

        user_input = request.POST.get('country_name', '').strip()   # input do usuário

        correct_country_name = request.session.get('correct_country_name')  # nome do país a ser adivinhado

        if user_input.lower() == correct_country_name.lower():  
            # Usuário fez o palpite correto!

            # Calcula pontos obtidos e atualiza pontos do usuário
            points_got = 100 - guesses * 10 if guesses * 10 < 100 else 10
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.points += points_got

            # Coloca páis acertado na lista do usuário
            country = Country.objects.get(name=correct_country_name)
            user_profile.countries_guessed.add(country)

            # Salva alterações no profile do usuário
            user_profile.save()

            # Mensagem para ser impressa na tela
            messages.success(request, 'Congratulations! You guessed the country correctly!')

            return render(request, "home.html", {'points': points + points_got})
        else:
            # Usuário não fez o palpite correto!

            # Obtém informações do país correto novamente
            country_info = request.session.get('country_info')
    
            return render(request, "home.html", {'country_info': country_info, 'guesses': guesses, 'points': points})

    # Se o método é GET e o usuário está autenticado -> inicia novo jogo
    if request.user.is_authenticated:

        # Obtém pontos do usuário para impressão na tela
        user_profile = UserProfile.objects.get(user=request.user)
        points = user_profile.points

        # Obtem lista de países que o usuário já acertou
        guessed_countries = list(user_profile.countries_guessed.values_list('name', flat=True))

        # Obtem páis aleatório dentre os disponíveis
        country = get_random_country(guessed_countries)

        # Preenche dicionário com as informações do país sorteado
        if country:
            country_info = {
                'name': country.get('name', {}).get('common'),
                'hemisphere': 'Northern' if country.get('latlng', [])[0] > 0 else 'Southern',
                'continent': country.get('continents', [])[0] if country.get('continents') else None,
                'language': list(country.get('languages', {}).values())[0] if country.get('languages') else None,
                'currency': list(country.get('currencies', {}).keys())[0] if country.get('currencies') else None,
                'area': country.get('area'),
                'subregion': country.get('subregion'),
                'capital': country.get('capital')[0]
            }

            # Atualiza info na sessão: informações do país sorteado, 
            request.session['country_info'] = country_info
            request.session['correct_country_name'] = country_info['name']
            guesses = 0
            request.session['guesses'] = guesses

            # Certifique-se de que o país esteja na base de dados
            Country.objects.get_or_create(name=country_info['name'])

            return render(request, "home.html", {'country_info': country_info, 'guesses': guesses, 'points': points})

        else:
            return HttpResponse("Erro ao obter informações do país")

    # Se o método for GET e o usuário não está autenticado
    return render(request, "home.html")
    
    
# View da página de registro
def register(request):

    # Se o método for um POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)   # form pré-definido do Django
        if form.is_valid(): # Validação do form
            form.save() # Salva o form
            username = form.cleaned_data.get('username')    # Pega username digitado
            password = form.cleaned_data.get('password1')   # Pega senha digitada
            user = authenticate(username=username, password=password)   # Realiza autenticação do usuário com os valores passados
            login(request, user)    # Realiza o login do usuário
            return redirect('home') # Redireciona para a home
    else:   # Se o método for um GET
        form = UserCreationForm()   # form pré-definido do Django 
    return render(request, 'registration/register.html', {'form': form}) # Renderiza página com o form para ser preenchido

# Classe de view para mudança de senha, herança com a view pré-definida do Django
class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm # form para preenchimento
    success_url = reverse_lazy('home')  # Se a mudança for pré-definida, redireciona para a home
    template_name = 'registration/change_password.html' # caminho do template

# View do scoreboard
def scoreboard(request):
    top_users = UserProfile.objects.order_by('-points')[:10]    # Pega os 10 usuários com as maiores quantidades de pontos
    return render(request, 'scoreboard.html', {'top_users': top_users})

# View para deletar perfil
@login_required
def delete_profile(request):
    if request.method == 'POST':    # Se o método for post
        user = request.user      
        user.delete()
        logout(request)  # Faz logout do usuário após a exclusão do perfil
        return redirect('home')  # Redireciona para a home
    return render(request, 'registration/delete_profile.html')  # Se o método for GET