from django.db import models
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class AdminUser(models.Model):
    nama_lengkap = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Hanya hash password saat pertama kali dibuat
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.username

class Kelas (models.Model):
    nama_kelas =  models.CharField(max_length=255)
    
    def __str__(self):
        return self.nama_kelas

class Kriteria(models.Model):
    KATEGORI_CHOICES = [
        ('robotik', 'Robotik'),
        ('coding', 'Coding'),
    ]

    nama_kriteria = models.CharField(max_length=255)
    pertanyaan = models.TextField()
    kategori = models.CharField(max_length=10, choices=KATEGORI_CHOICES)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True, blank=True)
    mb = models.DecimalField(max_digits=5, decimal_places=1)  # Measure of Belief
    md = models.DecimalField(max_digits=5, decimal_places=1)  # Measure of Disbelief
    cfrule = models.DecimalField(max_digits=5, decimal_places=1, editable=False)  # Otomatis, tidak perlu diisi manual

    def save(self, *args, **kwargs):
        self.cfrule = Decimal(self.mb) - Decimal(self.md)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pertanyaan

