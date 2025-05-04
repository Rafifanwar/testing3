from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('login/', views.login_admin, name='login_admin'),
    path('daftar_admin/', views.daftar_admin, name='daftar_admin'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
    path('data_user/', views.data_user, name='data_user'),
    path('ubah_user/<int:id>/', views.ubah_user, name='ubah_user'),
    path('hapus_user/<int:id>/', views.hapus_user, name='hapus_user'),
    path('data_kelas/', views.data_kelas, name='data_kelas'),
    path('hapus_kelas/<int:id>/', views.hapus_kelas, name='hapus_kelas'),
    path('tambah_kelas/', views.tambah_kelas, name='tambah_kelas'),
    path('ubah_kelas/<int:id>/', views.ubah_kelas, name='ubah_kelas'),
    path('data_kriteria/', views.data_kriteria, name='data_kriteria'),
    path('tambah_kriteria/', views.tambah_kriteria, name='tambah_kriteria'),
    path('ubah_kriteria/<int:id>/', views.ubah_kriteria, name='ubah_kriteria'),
    path('hapus_kriteria/<int:id>/', views.hapus_kriteria, name='hapus_kriteria'),
    path('hasil_cf/', views.data_hasil_cf, name='data_hasil_cf'),
    path('hapus_hasil_cf/<int:id>/', views.hapus_hasil_cf, name='hapus_hasil_cf'),
    path('tambah_user/', views.tambah_user, name='tambah_user'),
]