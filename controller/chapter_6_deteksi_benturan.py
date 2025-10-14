from controller import Supervisor
import numpy as np  # Library canggih untuk perhitungan matematika/vektor

# Inisialisasi dasar
TIME_STEP = 32
robot = Supervisor()

# 1. Dapatkan 'handle' untuk node BB-8 secara keseluruhan. Ini sudah cukup!
bb8_node = robot.getFromDef('BB-8')

if bb8_node is None:
    print("Error: Node dengan DEF 'BB-8' tidak ditemukan.")
    exit()

# 2. Siapkan variabel yang dibutuhkan
#    Variabel untuk menyimpan data kecepatan dari langkah simulasi sebelumnya.
kecepatan_sebelumnya = np.array([0.0, 0.0, 0.0])
jumlah_tumbukan = 0
#    'Flag' untuk mencegah satu tabrakan dihitung berkali-kali.
sedang_tertabrak = False

# 3. Tentukan Ambang Batas (Threshold)
#    Seberapa besar "guncangan" atau perubahan kecepatan yang kita anggap sebagai tabrakan.
#    Kamu bisa coba naikkan atau turunkan nilai ini jika deteksinya terlalu sensitif/kurang sensitif.
AMBANG_BATAS_TUMBUKAN = 0.2

print("Supervisor siap mendeteksi tumbukan via analisis kecepatan.")
print("Coba dorong BB-8 dengan keras ke dinding!")

# Loop utama simulasi
while robot.step(TIME_STEP) != -1:
    # 4. Dapatkan kecepatan linear saat ini [vx, vy, vz]
    #    getVelocity() mengembalikan [vx, vy, vz, ang_vx, ang_vy, ang_vz]
    #    Kita hanya butuh 3 komponen pertama (kecepatan linear).
    kecepatan_sekarang = np.array(bb8_node.getVelocity()[0:3])

    # 5. Hitung besarnya perubahan kecepatan
    #    np.linalg.norm menghitung panjang vektor, cara mudah untuk tahu "besarnya" guncangan.
    perubahan_kecepatan = np.linalg.norm(kecepatan_sekarang - kecepatan_sebelumnya)

    # 6. Logika Deteksi Tumbukan
    #    Jika besarnya perubahan kecepatan MELEBIHI ambang batas DAN kita TIDAK sedang tertabrak...
    #    ...maka ini adalah tumbukan baru!
    if perubahan_kecepatan > AMBANG_BATAS_TUMBUKAN and not sedang_tertabrak:
        jumlah_tumbukan += 1
        sedang_tertabrak = True  # Naikkan bendera
        print(f"Tumbukan terdeteksi! (Guncangan: {perubahan_kecepatan:.2f}) Total: {jumlah_tumbukan}")
    
    # Jika guncangan sudah reda, turunkan bendera agar siap mendeteksi lagi
    elif perubahan_kecepatan < 0.1 and sedang_tertabrak:
        sedang_tertabrak = False
        print("Robot sudah stabil, siap mendeteksi tumbukan berikutnya.")

    # 7. Update data untuk iterasi selanjutnya
    #    Kecepatan "sekarang" akan menjadi kecepatan "sebelumnya" di langkah berikutnya.
    kecepatan_sebelumnya = kecepatan_sekarang
