from django.urls import path
from . import views

urlpatterns = [

    path('login_user/', views.login_user, name='login_user'),
    path('daftar_user/', views.daftar_user, name='daftar_user'),
    path('kuisioner/', views.kuisioner, name='kuisioner'),
    path('hasil_cf/', views.hasil_cf, name='hasil_cf'),
    path('logout_user/', views.logout_user, name='logout_user'),
]