from .models import *
def hitung_cf(user):
    """Menghitung Certainty Factor dengan metode persis seperti Excel"""
    # 1. Ambil semua jawaban user
    jawaban_all = user.jawabanuser_set.all()
    
    # 2. Dapatkan jawaban terbaru (jika ada banyak set jawaban)
    # Asumsikan 10 jawaban (sesuai dengan jumlah kriteria)
    id_jawaban_terbaru = jawaban_all.values('kriteria').annotate(max_id=models.Max('id')).values_list('max_id', flat=True)
    jawaban_list = JawabanUser.objects.filter(id__in=id_jawaban_terbaru)
    
    # 3. Log semua jawaban untuk verifikasi
    print("\n=== DATA JAWABAN PENGGUNA ===")
    for j in jawaban_list:
        print(f"Kriteria {j.kriteria.id}: Kategori={j.kriteria.kategori}, MB={j.kriteria.mb}, MD={j.kriteria.md}, cfrule={j.kriteria.cfrule} Nilai={j.nilai}")
        print(f"\nTotal soal yang dijawab dan dihitung: {len(jawaban_list)}")
    # 4. Pisahkan jawaban robotik dan coding
    # Penting: Urutkan berdasarkan kriteria.id untuk konsistensi
    jawaban_robotik = sorted(
        [j for j in jawaban_list if j.kriteria.kategori == 'robotik'],
        key=lambda x: x.kriteria.id
    )
    
    jawaban_coding = sorted(
        [j for j in jawaban_list if j.kriteria.kategori == 'coding'],
        key=lambda x: x.kriteria.id
    )
    
    # 5. Hitung CF robotik dengan langkah-langkah yang jelas
    cf_robotik = 0
    print("\n=== PERHITUNGAN CF ROBOTIK ===")
    for idx, j in enumerate(jawaban_robotik):
        mb = float(j.kriteria.mb)
        md = float(j.kriteria.md)
        cf=float(j.kriteria.cfrule)
        nilai = float(j.nilai)
        
        # CF individual = MB * nilai - MD * nilai
        cf_individual = (mb-md) * nilai
        
        # Simpan CF lama untuk logging
        cf_old = cf_robotik
        
        # Kombinasi CF dengan rumus: CF(x,y) = CF(x) + CF(y) * (1 - CF(x))
        cf_robotik = cf_robotik + cf_individual * (1 - cf_robotik)
        
        # Log setiap langkah perhitungan
        print(f"Langkah {idx+1} - Kriteria {j.kriteria.id}:")
        print(f"  • MB={mb}, MD={md}, Nilai={nilai}")
        print(f"  • CF individual = ({mb}-{md}) * {nilai}= {cf_individual}")
        print(f"  • CF kombinasi = {cf_old} + {cf_individual} * (1 - {cf_old}) = {cf_robotik}")
   
    # 6. Hitung CF coding dengan langkah yang sama
    cf_coding = 0
    print("\n=== PERHITUNGAN CF CODING ===")
    for idx, j in enumerate(jawaban_coding):
        mb = float(j.kriteria.mb)
        md = float(j.kriteria.md)
        nilai = float(j.nilai)
        
        cf_individual = (mb-md) * nilai
        cf_old = cf_coding
        cf_coding = cf_coding + cf_individual * (1 - cf_coding)
        
        print(f"Langkah {idx+1} - Kriteria {j.kriteria.id}:")
        print(f"  • MB={mb}, MD={md}, Nilai={nilai}")
        print(f"  • CF individual =({mb}-{md}) * {nilai}= {cf_individual}")
        print(f"  • CF kombinasi = {cf_old} + {cf_individual} * (1 - {cf_old}) = {cf_coding}")
    
    # 7. Hitung persentase akhir
    persen_robotik = round(cf_robotik * 100, 2)
    persen_coding = round(cf_coding * 100, 2)
    
    print("\n=== HASIL AKHIR ===")
    print(f"CF Robotik: {cf_robotik} → {persen_robotik}%")
    print(f"CF Coding: {cf_coding} → {persen_coding}%")
    
    return {'robotik': persen_robotik, 'coding': persen_coding}