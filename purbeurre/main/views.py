from django.shortcuts import render
from django.http import HttpResponse



def homepage(request):
    test = '5'
    return render(request = request,
                  template_name='main/homepage.html',
                  context = {"tutorials":test})