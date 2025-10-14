"""
Controller Supervisor FINAL untuk mendeteksi tumbukan BB-8.
- Fitur 1: Deteksi tumbukan via analisis kecepatan (jawaban soal 1).
- Fitur 2: Respawn di lokasi acak (jawaban soal 2).
- Fitur 3: Merekam posisi ke file CSV (Jawaban Soal No. 3).
"""

from controller import Supervisor
import numpy as np
import random

# Inisialisasi dasar
TIME_STEP = 32
robot = Supervisor()

# Dapatkan 'handle' untuk node BB-8
bb8_node = robot.getFromDef('BB-8')

if bb8_node is None:
    print("Error: Node dengan DEF 'BB-8' tidak ditemukan.")
    exit()

# --- Fitur Respawn Acak (Jawaban Soal No. 2) ---
translation_field = bb8_node.getField('translation')
posisi_x_acak = random.uniform(-4.5, 4.5)
posisi_z_acak = random.uniform(-4.5, 4.5)
posisi_y_awal = bb8_node.getPosition()[1]
posisi_baru = [posisi_x_acak, posisi_y_awal, posisi_z_acak]
translation_field.setSFVec3f(posisi_baru)
print(f"=====================================================")
print(f"Simulasi di-reset. BB-8 dimunculkan di lokasi acak.")
print(f"=====================================================")

# ==================================================================
# === JAWABAN SOAL NOMOR 3 DIMULAI DI SINI ===
# ==================================================================
# LANGKAH 1: Buka file untuk ditulis.
# File akan dibuat di dalam folder controller-mu.
try:
    file_rekaman = open("rekaman_posisi_bb8.csv", "w")
    # LANGKAH 2: Tulis baris header (judul kolom)
    file_rekaman.write("WaktuSimulasi,PosisiX,PosisiY,PosisiZ\n")
    print("Mulai merekam posisi ke file 'rekaman_posisi_bb8.csv'...")
except IOError as e:
    print(f"Error saat membuka file: {e}")
    file_rekaman = None # Tandai bahwa file gagal dibuka
# ==================================================================

# Siapkan variabel untuk deteksi tumbukan
kecepatan_sebelumnya = np.array([0.0, 0.0, 0.0])
jumlah_tumbukan = 0
sedang_tertabrak = False
AMBANG_BATAS_TUMBUKAN = 0.3

print("Supervisor siap mendeteksi tumbukan.")
print("Gunakan tombol panah untuk menggerakkan BB-8.")

# Loop utama simulasi
try:
    while robot.step(TIME_STEP) != -1:
        # --- Kode deteksi tumbukan ---
        kecepatan_sekarang = np.array(bb8_node.getVelocity()[0:3])
        perubahan_kecepatan = np.linalg.norm(kecepatan_sekarang - kecepatan_sebelumnya)

        if perubahan_kecepatan > AMBANG_BATAS_TUMBUKAN and not sedang_tertabrak:
            jumlah_tumbukan += 1
            sedang_tertabrak = True
            print(f"Tumbukan terdeteksi! Total: {jumlah_tumbukan}")
        elif perubahan_kecepatan < 0.1 and sedang_tertabrak:
            sedang_tertabrak = False

        kecepatan_sebelumnya = kecepatan_sekarang
        
        # ==================================================================
        # === JAWABAN SOAL NOMOR 3 (LANJUTAN DI DALAM LOOP) ===
        # ==================================================================
        if file_rekaman: # Pastikan file berhasil dibuka
            # LANGKAH 3: Dapatkan data saat ini
            waktu_simulasi = robot.getTime()
            posisi_robot = bb8_node.getPosition() # [x, y, z]

            # LANGKAH 4: Format data menjadi string CSV
            baris_data = f"{waktu_simulasi},{posisi_robot[0]},{posisi_robot[1]},{posisi_robot[2]}\n"

            # LANGKAH 5: Tulis baris data ke file
            file_rekaman.write(baris_data)
        # ==================================================================

finally:
    # ==================================================================
    # === JAWABAN SOAL NOMOR 3 (BAGIAN AKHIR) ===
    # ==================================================================
    # LANGKAH 6: Tutup file saat simulasi berhenti
    if file_rekaman:
        file_rekaman.close()
        print("Perekaman selesai. File 'rekaman_posisi_bb8.csv' telah disimpan.")
    # ==================================================================