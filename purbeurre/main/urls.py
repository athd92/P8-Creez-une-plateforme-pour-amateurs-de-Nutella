from django.urls import path
from . import views
from django.views.generic import RedirectView
app_name = 'main'  # here for namespacing of urls.


urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path("logout/", views.logout_request, name="logout"),
    path('login/', views.login_request, name="login"),
    path('aliments/', views.aliments, name="aliments"),
    path('account/', views.account, name="account"),
    path('infos/<int:aliment_id>/', views.infos, name='infos'),
    path('save_aliment/<int:aliment_id>/',
         views.save_aliment,
         name='save_aliment'),
    path('saved/', views.saved, name='saved'),
    path('delete/<int:aliment_id>/', views.delete, name="delete"),
    path('alternative/<int:aliment_id>',
         views.alternative,
         name='alternative'),
]