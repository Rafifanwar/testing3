from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import AdminUser,Kelas,Kriteria
from django.contrib.auth.hashers import check_password
from user.models import CustomUser, HasilCF
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from user.models import HasilCF
from django.contrib.auth.hashers import make_password
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get("admin_id"):  # Jika bukan admin
            return redirect("login_admin")  # Redirect ke login jika session habis
            #return render(request, "adm/403.html", status=403)  
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def dashboard_admin(request):
        # Menghitung total data
    total_siswa = CustomUser.objects.count()
    total_kelas = Kelas.objects.count()
    total_hasil_cf = HasilCF.objects.count()

    context = {
        'total_siswa': total_siswa,
        'total_kelas': total_kelas,
        'total_hasil_cf': total_hasil_cf,
    }

    return render(request, "adm/dashboard_admin.html",context)

def login_admin(request):
    error = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            admin_user = AdminUser.objects.get(username=username)
            if check_password(password, admin_user.password):
                request.session['admin_id'] = admin_user.id
                request.session['admin_username'] = admin_user.username
                return redirect('dashboard_admin')
            else:
                return render(request, 'adm/login_admin.html', {
                'status': 'error',
                'message': 'Gagal login coba lagi.'
            })
        except AdminUser.DoesNotExist:
            return render(request, 'adm/login_admin.html', {
                'status': 'error',
                'message': 'Username tidak ada.'
            })

    return render(request, "adm/login_admin.html")

def daftar_admin(request):
    if request.method == 'POST':
        nama_lengkap = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if AdminUser.objects.filter(username=username).exists():
            return render(request, 'adm/daftar_admin.html', {
                'status': 'error',
                'message': 'Username sudah digunakan.'
            })

        if AdminUser.objects.filter(email=email).exists():
            return render(request, 'adm/daftar_admin.html', {
                'status': 'error',
                'message': 'Email sudah digunakan.'
            })

        admin_user = AdminUser(
            nama_lengkap=nama_lengkap,
            username=username,
            email=email,
            password=password
        )
        admin_user.save()

        return render(request, 'adm/daftar_admin.html', {
            'status': 'success',
            'message': 'Pendaftaran berhasil! Halaman akan diarahkan ke halaman login.'
        })

    return render(request, 'adm/daftar_admin.html')

def logout_admin(request):
    request.session.flush()

    return redirect('login_admin')

@admin_required
def data_user(request):
    users = CustomUser.objects.all()  # Mengambil semua data user dari database
    return render(request, 'adm/data_user.html', {'users': users})

def ubah_user(request, id):
    user = get_object_or_404(CustomUser, id=id)

    if request.method == "POST":
        user.nama_lengkap = request.POST.get('nama_lengkap', user.nama_lengkap)
        user.username = request.POST.get('username', user.username)
        user.no_hp = request.POST.get('no_hp', user.no_hp)
        user.usia = request.POST.get('usia', user.usia)
        user.save()
      
        return redirect("data_user")

    return redirect("data_user")

@admin_required
def tambah_user(request):
    if request.method == "POST":
        nama_lengkap = request.POST.get("nama_lengkap")
        username = request.POST.get("username")
        no_hp = request.POST.get("no_hp")
        usia = request.POST.get("usia")
        password = request.POST.get("password")  # Tambahkan input password

        # Validasi apakah username sudah digunakan
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('data_user')
        
        # Validasi apakah semua field terisi
        if not all([nama_lengkap, username, no_hp, usia, password]):
            messages.error(request, "Semua field wajib diisi.")
            return redirect('data_user')

        # Simpan user baru dengan password yang di-hash
        user = CustomUser(
            nama_lengkap=nama_lengkap,
            username=username,
            no_hp=no_hp,
            usia=usia,
            password=make_password(password)  # Hash password
        )
        user.save()
        messages.success(request, "User berhasil ditambahkan.")
        return redirect('data_user')

    return redirect('data_user')

# Menghapus user
def hapus_user(request, id):
    user = get_object_or_404(CustomUser, id=id)  # Cari user berdasarkan ID
    user.delete()  # Hapus user dari database
 
    return redirect('data_user')


@admin_required
def data_kelas(request):
    kelas = Kelas.objects.all()  # Mengambil semua data user dari database
    return render(request, 'adm/data_kelas.html', {'kelas': kelas})

def hapus_kelas(request, id):
    kelas = get_object_or_404(Kelas, id=id)  # Cari kelas berdasarkan ID
    kelas.delete()  # Hapus kelas dari database
  
    return redirect('data_kelas')

# View untuk menambah kelas
def tambah_kelas(request):
    if request.method == "POST":
        nama_kelas = request.POST.get("nama_kelas")
        if nama_kelas:
            Kelas.objects.create(nama_kelas=nama_kelas)
    return redirect("data_kelas")

def ubah_kelas(request, id):
    kelas = get_object_or_404(Kelas, id=id)

    if request.method == "POST":
        nama_kelas = request.POST.get("nama_kelas", kelas.nama_kelas)
        kelas.nama_kelas = nama_kelas
        kelas.save()
        return redirect("data_kelas")

    return render(request, "adm/data_kelas.html", {"kelas": kelas})

@admin_required
def data_kriteria(request):
    kriteria = Kriteria.objects.all()
    kelas_list = Kelas.objects.all()  # Ambil semua data kelas dari model Kelas
    return render(request, 'adm/data_kriteria.html', {'kriteria': kriteria, 'kelas_list': kelas_list})

def tambah_kriteria(request):
    if request.method == "POST":
        nama_kriteria = request.POST.get("nama_kriteria")
        pertanyaan = request.POST.get("pertanyaan")
        kategori = request.POST.get("kategori")
        mb = request.POST.get("mb")
        md = request.POST.get("md")

        if not all([nama_kriteria, pertanyaan, kategori, mb, md]):
            return redirect("data_kriteria")

        try:
            mb = float(mb)
            md = float(md)
        except ValueError:
            return redirect("data_kriteria")

        cfrule = mb - md

        Kriteria.objects.create(
            nama_kriteria=nama_kriteria,
            pertanyaan=pertanyaan,
            kategori=kategori,
            mb=mb,
            md=md,
            cfrule=cfrule
        )

        return redirect("data_kriteria")

    return render(request, "adm/data_kriteria.html")


def ubah_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)

    if request.method == "POST":
        kriteria.nama_kriteria = request.POST.get("nama_kriteria", kriteria.nama_kriteria)
        kriteria.pertanyaan = request.POST.get("pertanyaan", kriteria.pertanyaan)
        kriteria.kategori = request.POST.get("kategori", kriteria.kategori)
        kriteria.mb = request.POST.get("mb", kriteria.mb)
        kriteria.md = request.POST.get("md", kriteria.md)
        kriteria.cfrule = request.POST.get("cfrule", kriteria.cfrule)
        kriteria.save()
        return redirect("data_kriteria")

    return redirect("data_kriteria")

def hapus_kriteria(request, id):
    kriteria = get_object_or_404(Kriteria, id=id)
    kriteria.delete()
  
    return redirect("data_kriteria")


@admin_required
def data_hasil_cf(request):
    """
    View untuk menampilkan daftar hasil Certainty Factor (CF).
    """
    hasil_cf = HasilCF.objects.select_related('user').all()
    return render(request, 'adm/riwayat_rekomendasi.html', {'hasil_cf': hasil_cf})

def hapus_hasil_cf(request,id):
    hasil_cf = get_object_or_404(HasilCF, id=id)
    hasil_cf.delete()
 
    return redirect("data_hasil_cf")
