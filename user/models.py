from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from adm.models import Kriteria
from django.contrib.auth import get_user_model
from .models import *


class CustomUser(models.Model):
    
    MINAT_CHOICES = [
        ('robotika', 'Robotika'),
        ('coding', 'Coding'),
    ]
     
    nama_lengkap = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=255)
    usia = models.PositiveIntegerField(null=True, blank=True)  # Bisa dikosongkan
    date_joined = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # Hash password hanya jika ada perubahan password
        if self.pk:
            original = CustomUser.objects.get(pk=self.pk)
            if original.password != self.password:
                self.password = make_password(self.password)
        else:
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        """Memeriksa apakah password cocok dengan hash yang tersimpan"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class JawabanUser(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    kriteria = models.ForeignKey(Kriteria, on_delete=models.CASCADE)
    nilai = models.DecimalField(max_digits=3, decimal_places=2)  # Simpan nilai CF (0.0 - 1.0)

    def __str__(self):
        return f"{self.user.nama_lengkap} - {self.kriteria.nama_kriteria}: {self.nilai}"

class HasilCF(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    persen_robotik = models.DecimalField(max_digits=5, decimal_places=2)
    persen_coding = models.DecimalField(max_digits=5, decimal_places=2)
    tanggal = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} | Robotik: {self.persen_robotik}% | Coding: {self.persen_coding}%"


