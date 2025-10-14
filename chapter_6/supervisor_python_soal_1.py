from controller import Supervisor

# Inisialisasi Supervisor dan timestep
supervisor = Supervisor()
timestep = int(supervisor.getBasicTimeStep())

# Cek jumlah perangkat yang terdeteksi oleh supervisor
device_count = supervisor.getNumberOfDevices()
print(f"Jumlah perangkat yang terdeteksi: {device_count}")

# Print nama perangkat yang terdeteksi
for i in range(device_count):
    device = supervisor.getDeviceByIndex(i)
    print(f"Perangkat ke-{i}: {device.getName()}")

# Mencoba mendapatkan perangkat 'bumper'
bumper = supervisor.getDevice('sensor')

if bumper is None:
    print("ERROR: Sensor 'bumper' tidak ditemukan pada robot.")
    exit()

bumper.enable(timestep)

# Variabel untuk menghitung jumlah tabrakan
collision_count = 0

print("Program pelacakan tabrakan dimulai...")

# Simulasi utama
while supervisor.step(timestep) != -1:
    # Periksa apakah bumper (touch sensor) terpicu
    if bumper.getValue() > 0:
        collision_count += 1
        print(f"Tabrakan ke-{collision_count} terdeteksi!")

    # Tampilkan jumlah tabrakan setiap 1000 langkah simulasi
    if supervisor.getTime() % 1000 < timestep:
        print(f"Jumlah tabrakan sejauh ini: {collision_count}")

print("Simulasi selesai.")
