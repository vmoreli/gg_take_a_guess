from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# views in django - request handlers (actions, in other frameworks)
def home(request):
    return render(request, "home.html")