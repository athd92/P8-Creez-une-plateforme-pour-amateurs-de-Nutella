from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .forms import UserFormWithEmail
from .models import Aliment
from .form_aliment import FormAliment


def homepage(request):
    test = '5'
    return render(request=request,
                  template_name='main/homepage.html',
                  context={"tutorials": test})


def register(request):
    if request.method == "POST":
        form = UserFormWithEmail(request.POST)
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

            return render(request=request,
                          template_name="main/register.html",
                          context={"form": form})

    form = UserFormWithEmail
    return render(request=request,
                  template_name="main/register.html",
                  context={"form": form})


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
                messages.info(request,
                              f"Bienvenue {username},vous êtes connecté!")
                return redirect('/')
            else:
                messages.error(request,
                               "Identifiant ou mot de passe invalide.")
        else:
            messages.error(request, "Identifiant ou mot de passe invalide.")
    form = AuthenticationForm()
    return render(request=request,
                  template_name="main/login.html",
                  context={"form": form})


def aliments(request):
    
    aliment_list = Aliment.objects.all()
    query = request.GET.get('aliments')
    print(query)
    
    if query:
        
        aliment_list = Aliment.objects.filter(
                                              name__startswith=query,
                                              ).exclude(nutriscore='non disponible').exclude(brands="non disponible")
        aliment_count = aliment_list.count()

    paginator = Paginator(aliment_list, 3) # 6 posts per page
    page = request.GET.get('page')

    try:
        aliments = paginator.page(page)
    except PageNotAnInteger:
        aliments = paginator.page(1)
    except EmptyPage:
        aliments = paginator.page(paginator.num_pages)

    context = {
        'aliments': aliments,
        'count': aliment_count,
    }
    return render(request, "main/aliments.html", context)



    # aliments = Aliment.objects.all()
    # paginator = Paginator(aliments, 6) # Show 25 contacts per page

    # page = request.GET.get('page')
    # aliment = paginator.get_page(page)
    # return render(request, 'main/aliments.html', {'aliments': aliment})


def account(request):

    return render(request, 'main/account.html')

def infos(request, aliment_id):
    
    aliment = Aliment.objects.get(id=aliment_id)
    # name = aliment.name
    date = aliment.date
    date = date[2:12]
    print(f'DATE {date}')
    context = {
        'aliment': aliment,
        'date': date,
    }
    
    return render(request, 'main/infos.html', context)

def favorites(request, aliment_id):
    
    print("ALIMENT ID")
    print(aliment_id)
    context = {
        "aliment_id" : aliment_id
    }
    return render(request, 'main/favorites.html', context)