from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages



def homepage(request):
    test = '5'
    return render(request = request,
                  template_name='main/homepage.html',
                  context = {"tutorials":test})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,
                             f'Bienvenue {username}, votre profile est créé!')
            login(request, user)
            
            return redirect("main:homepage")
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

            return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                template_name = "main/register.html",
                context={"form":form})


def logout_request(request):
    logout(request)
    messages.info(request, 'Vous êtes déconnecté')
    return redirect("main:homepage")


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Bienvenue {username}, vous êtes connecté!")
                return redirect('/')
            else:
                messages.error(request, "Identifiant ou mot de passe invalide.")
        else:
            messages.error(request, "Identifiant ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request = request,
                    template_name = "main/login.html",
                    context={"form":form})