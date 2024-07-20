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
import requests
import random

# Create your views here.
# views in django - request handlers (actions, in other frameworks)

def get_random_country():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return random.choice(data)
    return None

def home(request):
    if request.method == 'POST':
        guesses = request.session['guesses'] + 1
        request.session['guesses'] = guesses
        user_input = request.POST.get('country_name', '').strip()
        print("user input: " + user_input)
        correct_country_name = request.session.get('correct_country_name')

        if user_input.lower() == correct_country_name.lower():
            points = 100 - guesses * 10 if guesses * 10 < 100 else 10
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.points += points

            country = Country.objects.get(name=correct_country_name)

            user_profile.countries_guessed.add(country)
            user_profile.save()

            return HttpResponse("Você acertou!")
        else:
            country_info = request.session.get('country_info')
            print(guesses)
            return render(request, "home.html", {'country_info': country_info, 'guesses': guesses})

    if request.user.is_authenticated:
        country = get_random_country()

        if country:
            country_info = {
                'name': country.get('name', {}).get('common'),
                'hemisphere': 'Northern' if country.get('latlng', [])[0] > 0 else 'Southern',
                'continent': country.get('continents', [])[0] if country.get('continents') else None,
                'language': list(country.get('languages', {}).values())[0] if country.get('languages') else None,
                'currency': list(country.get('currencies', {}).keys())[0] if country.get('currencies') else None,
                'area': country.get('area'),
                'population': country.get('population'),
                'capital': country.get('capital')[0]
            }

            request.session['country_info'] = country_info
            request.session['correct_country_name'] = country_info['name']
            guesses = 0
            request.session['guesses'] = 0

            # Certifique-se de que o país esteja na base de dados
            Country.objects.get_or_create(name=country_info['name'])

            return render(request, "home.html", {'country_info': country_info, 'guesses': guesses})

        else:
            return HttpResponse("Erro ao obter informações do país")

    return render(request, "home.html")
    
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')
    template_name = 'registration/change_password.html'

def scoreboard(request):
    top_users = UserProfile.objects.order_by('-points')[:10]
    return render(request, 'scoreboard.html', {'top_users': top_users})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)  # Faz logout do usuário após a exclusão do perfil
        return redirect('home')  # Substitua 'home' pelo nome da URL para a página inicial ou outra página desejada
    return render(request, 'registration/delete_profile.html')