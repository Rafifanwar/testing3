from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import CustomUser,JawabanUser, HasilCF
from adm.models import Kriteria
from django.contrib.auth.decorators import login_required
from .utils import hitung_cf  # Fungsi hitung_cf
from django.utils import timezone 


def user_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("user_id"):  # jika session user_id tidak ada (expired/hilang)
            return redirect("login_user")  # ganti sesuai dengan nama url login user kamu
        return view_func(request, *args, **kwargs)
    return wrapper

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username)
            if check_password(password, user.password):
                # Simpan data user ke session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                request.session['nama_lengkap'] = user.nama_lengkap
                request.session['usia'] = user.usia 

               
                return redirect('kuisioner')  # Ganti dengan halaman dashboard user
            else:
                return render(request, 'user/login_user.html', {
                'status': 'error',
                'message': 'Gagal login coba lagi.'
                })
        except CustomUser.DoesNotExist:
           return render(request, 'user/login_user.html', {
                'status': 'error',
                'message': 'Username tidak ada.'
                })
    return render(request, 'user/login_user.html')

def daftar_user(request):
    if request.method == 'POST':
        nama_lengkap = request.POST['nama_lengkap']
        username = request.POST['username']
        no_hp = request.POST['no_hp']
        usia = request.POST['usia']
        password = request.POST['password']

        # Cek apakah username sudah terdaftar
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'user/daftar_user.html', {
                'status': 'error',
                'message': 'Username sudah digunakan.'
            })
        # Simpan data user ke database
        user = CustomUser(nama_lengkap=nama_lengkap, username=username, no_hp=no_hp, usia=usia, password=password)
        user.save()
        
        return render(request, 'user/daftar_user.html', {
            'status': 'success',
            'message': 'Pendaftaran berhasil! Halaman akan diarahkan ke halaman login.'
        })
        
       
        return redirect('login_user')

    return render(request, 'user/daftar_user.html')

def logout_user(request):
    request.session.flush()
    messages.success(request, 'Logout berhasil!')
    return redirect('login_user')

@user_required
def kuisioner(request):
    user_id = request.session.get('user_id')

    if not user_id:
        
        return redirect('login_user')

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        
        return redirect('login_user')

    if request.method == 'POST':
        # Hapus jawaban dan hasil CF sebelumnya
        JawabanUser.objects.filter(user=user).delete()
        HasilCF.objects.filter(user=user).delete()

        # Simpan jawaban kuisioner baru
        for kriteria in Kriteria.objects.all():
            nilai = float(request.POST.get(f'jawaban_{kriteria.id}', 0))
            JawabanUser.objects.create(user=user, kriteria=kriteria, nilai=nilai)

        # Hitung CF
        hasil_cf = hitung_cf(user)

        # Simpan hasil baru
        HasilCF.objects.create(
            user=user,
            persen_robotik=hasil_cf['robotik'],
            persen_coding=hasil_cf['coding'],
            tanggal=timezone.now()
        )

        messages.success(request, "Jawaban berhasil dikirim dan diperbarui!")
        return redirect('hasil_cf')

    kriteria_list = Kriteria.objects.all()
    return render(request, 'user/kuisioner.html', {'kriteria_list': kriteria_list})

@user_required
def hasil_cf(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login_user')
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        
        return redirect('login_user')

    user = CustomUser.objects.get(id=user_id)
    hasil = HasilCF.objects.filter(user=user).order_by('-tanggal')  # Ambil semua hasil, terbaru duluan

    # Pastikan selalu mengembalikan HttpResponse, bahkan jika hasil kosong
    return render(request, 'user/hasil_cf.html', {'hasil':hasil})