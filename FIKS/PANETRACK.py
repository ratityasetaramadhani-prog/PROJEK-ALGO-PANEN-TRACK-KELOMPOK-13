"""SISTEM PENDATAAN HASIL PANEN"""
import os
from tabulate import tabulate
from datetime import datetime

KETERANGAN_CSV = {
    "petani.csv": ["Username", "Password"],
    "distributor.csv": ["Username", "Password"],
    "panen.csv": ["Username", "Komoditas", "Jumlah", "Tanggal"],
    "transaksi.csv": ["Distributor", "Petani", "Komoditas", "Jumlah", "Tanggal"]}

def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def menyimpan_data(nama_file, data):
    file_exists = os.path.exists(nama_file)
    
    try:
        with open(nama_file, "a", encoding="utf-8") as file:
            if not file_exists and nama_file in KETERANGAN_CSV:
                file.write(",".join(KETERANGAN_CSV[nama_file]) + "\n")

            file.write(",".join(data) + "\n")
        return True
    except Exception as e:
        print(f"Error saat menyimpan data: {e}")
        return False
    
def membaca_data(nama_file):
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            lines = [baris.strip().split(",") for baris in file if baris.strip()]
       
        if lines and nama_file in KETERANGAN_CSV:
            if lines[0] == KETERANGAN_CSV[nama_file]:
                return lines[1:] 
        return lines
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error saat membaca data: {e}")
        return []


def inputan_kosong(teks, pesan):
    while True:
        nilai = input(teks).strip()
        if nilai:
            return nilai
        else:
            print(f"{pesan}")


def memvalidasi_angka(teks, pesan):
    while True:
        try:
            nilai = input(teks).strip()
            angka = float(nilai)
            if angka > 0:
                return angka
            else:
                print(f"{pesan} (harus lebih dari 0)")
        except ValueError:
            print(f"{pesan} (harus berupa angka)")

def memvalidasi_tanggal(teks):
    while True:
        tanggal = input(teks).strip()
        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
            return tanggal
        except ValueError:
            print(f"[ERROR] Tanggal tidak valid")
            print(f"Pastikan format DD-MM-YYYY (Contoh: 28-02-2025).")
        


def cetak_garis():
    print("=" * 40)

def cetak_titik():
    print("." * 40)

# == FUNGSI AKUN ==

def mendaftarkan_akun(role):
    cls()
    cetak_garis()
    print(f"REGISTRASI {role.upper()}")
    cetak_garis()
    
    file_akun = "petani.csv" if role == "petani" else "distributor.csv"
    
    username = inputan_kosong("Username: ", "Username tidak boleh kosong!")
    
    data_akun = membaca_data(file_akun)
    for akun in data_akun:
        if akun[0] == username:
            print("Username sudah terdaftar! Silakan gunakan username lain.")
            return
    
    password = inputan_kosong("Password: ", "Password tidak boleh kosong!")
    
    if menyimpan_data(file_akun, [username, password]):
        print("Registrasi berhasil! Silakan login.")
    else:
        print("Registrasi gagal! Coba lagi.")


def login_akun(role):
    cls()
    cetak_garis()
    print(f"LOGIN {role.upper()}")
    cetak_garis()
    
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    
    file_akun = "petani.csv" if role == "petani" else "distributor.csv"
    
    data = membaca_data(file_akun)
    for akun in data:
        if len(akun) >= 2 and akun[0] == username and akun[1] == password:
            print(f"Login berhasil! Selamat datang, {username}!")
            return username
    
    print("Login gagal! Username atau password salah.")
    return None


# == FUNGSI PETANI ===

def memcatat_panen(username):
    cls()
    cetak_garis()
    print("CATAT HASIL PANEN")
    cetak_garis()
    
    
    komoditas = inputan_kosong("Nama komoditas (contoh: padi, jagung): ", "Nama komoditas tidak boleh kosong!")
    
    jumlah = memvalidasi_angka("Jumlah (kg): ", "Jumlah harus berupa angka positif!")
    tanggal = memvalidasi_tanggal("Tanggal panen (DD-MM-YYYY): ")
    
    if menyimpan_data("panen.csv", [username, komoditas, str(jumlah), tanggal]):
        print(f"Data panen {komoditas} sebanyak {jumlah} kg berhasil disimpan!")
    else:
        print("Gagal menyimpan data panen!")


def melihat_panen(username):
    cls()
    cetak_garis()
    print("DATA PANEN ANDA")
    cetak_garis()
    
    data = membaca_data("panen.csv")
    tabel_data = []
    nomor = 1
    
    for baris in data:
        if len(baris) >= 4 and baris[0] == username:
            # [Nomor, Komoditas, Jumlah, Tanggal]
            tabel_data.append([nomor, baris[1], f"{baris[2]} kg", baris[3]])
            nomor += 1
    
    if not tabel_data:
        print("Belum ada data panen yang tercatat.")
    else:
        headers = ["No", "Komoditas", "Jumlah", "Tanggal Panen"]
        print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))


def laporan_statistik_petani(username):
    cls()
    cetak_garis()
    print("LAPORAN STATISTIK PANEN ANDA")
    cetak_garis()
    
    data_panen = membaca_data("panen.csv")
    data_transaksi = membaca_data("transaksi.csv")
    
    # Hitung statistik panen 
    total_komoditas = {}
    total_stok_kg = 0
    
    for baris in data_panen:
        if len(baris) >= 4 and baris[0] == username:
            komoditas = baris[1].lower()
            jumlah = float(baris[2])
            total_stok_kg += jumlah
            
            if komoditas in total_komoditas:
                total_komoditas[komoditas] += jumlah
            else:
                total_komoditas[komoditas] = jumlah
    
    # Hitung komoditas yang sudah terjual
    terjual_komoditas = {}
    total_terjual = 0
    
    for baris in data_transaksi:
        if len(baris) >= 5 and baris[1] == username:  
            komoditas = baris[2].lower()
            jumlah = float(baris[3])
            total_terjual += jumlah
            
            if komoditas in terjual_komoditas:
                terjual_komoditas[komoditas] += jumlah
            else:
                terjual_komoditas[komoditas] = jumlah
    
    # Tampilkan statistik
    print("\nRINGKASAN STOK SAAT INI (BELUM TERJUAL):")
    if total_komoditas:
        tabel_panen = []
        for komoditas, jumlah in sorted(total_komoditas.items()):
            tabel_panen.append([komoditas.title(), f"{jumlah} kg"])
        print(tabulate(tabel_panen, headers=["Komoditas", "Stok Tersedia"], tablefmt="fancy_grid"))
        print(f"\n  Total Stok Tersedia: {total_stok_kg} kg")
    else:
        print("  Belum ada data panen (stok kosong).")
    
    print("\nRINGKASAN PENJUALAN (RIWAYAT):")
    if terjual_komoditas:
        tabel_jual = []
        for komoditas, jumlah in sorted(terjual_komoditas.items()):
            tabel_jual.append([komoditas.title(), f"{jumlah} kg"])
        print(tabulate(tabel_jual, headers=["Komoditas", "Total Terjual"], tablefmt="fancy_grid"))
        print(f"\n  Total Terjual: {total_terjual} kg")
        
        # Hitung total panen keseluruhan (stok + terjual)
        total_panen_keseluruhan = total_stok_kg + total_terjual
        if total_panen_keseluruhan > 0:
            persentase = (total_terjual / total_panen_keseluruhan) * 100
            print(f"  Total Panen (Stok + Terjual): {total_panen_keseluruhan} kg")
            print(f"  Persentase Terjual: {persentase:.1f}%")
    else:
        print("  Belum ada penjualan.")


def menghapus_data_panen(username):
    cls()
    cetak_garis()
    print("HAPUS DATA PANEN")
    cetak_garis()
    
    data = membaca_data("panen.csv")
    panen_user = []
    
    # Tampilkan data panen milik user
    print("\nData panen Anda:")
    nomor = 1
    for i, baris in enumerate(data):
        if len(baris) >= 4 and baris[0] == username:
            print(f"{nomor}. {baris[1]}: {baris[2]} kg | Tanggal: {baris[3]}")
            panen_user.append(i)
            nomor += 1
    
    if not panen_user:
        print("Belum ada data panen yang tercatat.")
        return
    
    print(f"{nomor}. Batal")
    cetak_garis()
    
    # Pilih data yang akan dihapus
    while True:
        try:
            pilihan = int(input(f"Pilih nomor data yang akan dihapus (1-{nomor}): ").strip())
            if pilihan == nomor:
                print("Pembatalan berhasil.")
                return
            elif 1 <= pilihan < nomor:
                # Konfirmasi penghapusan
                konfirmasi = input("Yakin ingin menghapus data ini? (y/n): ").strip().lower()
                if konfirmasi == 'y':
                    index_hapus = panen_user[pilihan - 1]
                    data_baru = [baris for i, baris in enumerate(data) if i != index_hapus]
                    
                    # Tulis ulang file tanpa data yang dihapus
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        # Tulis Header dulu
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n")
                        # Tulis data sisa
                        for baris in data_baru:
                            file.write(",".join(baris) + "\n")
                    
                    print("Data berhasil dihapus!")
                    return
                else:
                    print("Penghapusan dibatalkan.")
                    return
            else:
                print(f"Pilihan tidak valid! Pilih 1-{nomor}.")
        except ValueError:
            print("Input harus berupa angka!")


def mengedit_data_panen(username):
    cls()
    cetak_garis()
    print("EDIT DATA PANEN")
    cetak_garis()
    
    data = membaca_data("panen.csv")
    panen_user = []
    
    # Tampilkan data panen milik user
    print("\nData panen Anda:")
    nomor = 1
    for i, baris in enumerate(data):
        if len(baris) >= 4 and baris[0] == username:
            print(f"{nomor}. {baris[1]}: {baris[2]} kg | Tanggal: {baris[3]}")
            panen_user.append(i)
            nomor += 1
    
    if not panen_user:
        print("Belum ada data panen yang tercatat.")
        return
    
    print(f"{nomor}. Batal")
    cetak_garis()
    
    # Pilih data yang akan diedit
    while True:
        try:
            pilihan = int(input(f"Pilih nomor data yang akan diedit (1-{nomor}): ").strip())
            if pilihan == nomor:
                print("Pembatalan berhasil.")
                return
            elif 1 <= pilihan < nomor:
                index_edit = panen_user[pilihan - 1]
                data_lama = data[index_edit]
                
                print(f"\nData saat ini:")
                print(f"Komoditas: {data_lama[1]}")
                print(f"Jumlah: {data_lama[2]} kg")
                print(f"Tanggal: {data_lama[3]}")
                cetak_garis()
                
                print("\nMasukkan data baru (tekan ENTER untuk tidak mengubah):")
                
                # Input data baru
                komoditas_baru = input(f"Nama komoditas [{data_lama[1]}]: ").strip()
                if not komoditas_baru:
                    komoditas_baru = data_lama[1]
                
                jumlah_input = input(f"Jumlah (kg) [{data_lama[2]}]: ").strip()
                if jumlah_input:
                    try:
                        jumlah_baru = float(jumlah_input)
                        if jumlah_baru <= 0:
                            print("Jumlah harus lebih dari 0. Menggunakan data lama.")
                            jumlah_baru = data_lama[2]
                        else:
                            jumlah_baru = str(jumlah_baru)
                    except ValueError:
                        print("Input tidak valid. Menggunakan nilai lama.")
                        jumlah_baru = data_lama[2]
                else:
                    jumlah_baru = data_lama[2]
                
                # Validasi saat Edit
                tanggal_input = input(f"Tanggal (DD-MM-YYYY) [{data_lama[3]}]: ").strip()
                if tanggal_input:
                    try:
                        datetime.strptime(tanggal_input, "%d-%m-%Y")
                        tanggal_baru = tanggal_input
                    except ValueError:
                        print("[ERROR] Tanggal tidak valid")
                        print("Menggunakan tanggal lama.")
                        tanggal_baru = data_lama[3]
                else:
                    tanggal_baru = data_lama[3]
                
                # Konfirmasi perubahan
                print("\nData yang akan disimpan:")
                print(f"Komoditas: {komoditas_baru}")
                print(f"Jumlah: {jumlah_baru} kg")
                print(f"Tanggal: {tanggal_baru}")
                
                konfirmasi = input("\nSimpan perubahan? (y/n): ").strip().lower()
                if konfirmasi == 'y':
                    data[index_edit] = [username, komoditas_baru, str(jumlah_baru), tanggal_baru]
                    
    
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n") # Tulis header
                        for baris in data:
                            file.write(",".join(baris) + "\n")
                    
                    print("Data berhasil diperbarui!")
                    return
                else:
                    print("Perubahan dibatalkan.")
                    return
            else:
                print(f"Pilihan tidak valid! Pilih 1-{nomor}.")
        except ValueError:
            print("Input harus berupa angka!")


def mengelompokkan_panen(username):
    cls()
    cetak_garis()
    print("PENGELOMPOKKAN PANEN BERDASARKAN PERIODE")
    cetak_garis()
    
    print("Masukkan periode tanggal:")
    tanggal_awal = memvalidasi_tanggal("Tanggal awal (DD-MM-YYYY): ")
    tanggal_akhir = memvalidasi_tanggal("Tanggal akhir (DD-MM-YYYY): ")
    
    # Validasi periode
    if tanggal_awal > tanggal_akhir:
        print("Error: Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
        return
    
    data = membaca_data("panen.csv")
    hasil_filter_tabel = []
    total_kg = 0
    komoditas_dict = {}
    
    print(f"\nHasil panen periode {tanggal_awal} sampai {tanggal_akhir}:")
    
    for baris in data:
        if len(baris) >= 4 and baris[0] == username:
            tanggal_panen = baris[3]
            if tanggal_awal <= tanggal_panen <= tanggal_akhir:
                komoditas = baris[1]
                jumlah = float(baris[2])
                
                # Data untuk tabel utama
                hasil_filter_tabel.append([tanggal_panen, komoditas, f"{jumlah} kg"])
                
                # Data untuk ringkasan
                total_kg += jumlah
                if komoditas in komoditas_dict:
                    komoditas_dict[komoditas] += jumlah
                else:
                    komoditas_dict[komoditas] = jumlah
    
    if not hasil_filter_tabel:
        print("Tidak ada data panen pada periode tersebut.")
    else:
        # Tampilkan tabel utama
        print(tabulate(hasil_filter_tabel, headers=["Tanggal", "Komoditas", "Jumlah"], tablefmt="fancy_grid"))
        
        cetak_garis()
        print(f"\nRINGKASAN PERIODE:")
        print(f"Total data: {len(hasil_filter_tabel)} entri")
        print(f"Total panen: {total_kg} kg")
        
        print(f"\nPer komoditas:")
        tabel_ringkasan = []
        for komoditas, jumlah in sorted(komoditas_dict.items()):
            tabel_ringkasan.append([komoditas.title(), f"{jumlah} kg"])
        print(tabulate(tabel_ringkasan, headers=["Komoditas", "Jumlah"], tablefmt="fancy_grid"))


def menu_petani(username):
    while True:
        cls()
        cetak_garis()
        print(f"MENU PETANI - {username}")
        cetak_garis()
        print("1. Catat hasil panen")
        print("2. Lihat hasil panen saya")
        print("3. Edit data panen")
        print("4. Hapus data panen")
        cetak_titik()
        print("5. Laporan statistik panen")
        print("6. Pengelompokkan panen berdasarkan periode")
        print("7. Logout")
        cetak_garis()
        
        pilihan = input("Pilih menu (1-7): ").strip()
        
        if pilihan == "1":
            memcatat_panen(username)
        elif pilihan == "2":
            melihat_panen(username)
        elif pilihan == "5":
            laporan_statistik_petani(username)
        elif pilihan == "4":
            menghapus_data_panen(username)
        elif pilihan == "3":
            mengedit_data_panen(username)
        elif pilihan == "6":
            mengelompokkan_panen(username)
        elif pilihan == "7":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-7.")
        
        input("\nTekan ENTER untuk melanjutkan...")


# === FUNGSI DISTRIBUTOR ===

def laporan_pembelian_distributor(username):
    cls()
    cetak_garis()
    print("LAPORAN PEMBELIAN ANDA")
    cetak_garis()
    
    data_transaksi = membaca_data("transaksi.csv")
    
    if not data_transaksi:
        print("Belum ada transaksi pembelian.")
        return
    
    # Filter transaksi milik distributor ini
    transaksi_user = []
    total_pembelian = {}
    total_kg_semua = 0
    petani_list = set()
    
    for baris in data_transaksi:
        if len(baris) >= 5 and baris[0] == username:
            transaksi_user.append(baris)
            komoditas = baris[2].lower()
            jumlah = float(baris[3])
            petani = baris[1]
            
            # Hitung total per komoditas
            if komoditas in total_pembelian:
                total_pembelian[komoditas] += jumlah
            else:
                total_pembelian[komoditas] = jumlah
            
            total_kg_semua += jumlah
            petani_list.add(petani)
    
    if not transaksi_user:
        print("Anda belum melakukan pembelian.")
        return
    
    # Tampilkan statistik
    print("\nRINGKASAN PEMBELIAN:")
    print(f"  Total Transaksi: {len(transaksi_user)} kali")
    print(f"  Total Komoditas Dibeli: {total_kg_semua} kg")
    print(f"  Jumlah Petani Mitra: {len(petani_list)} petani")
    
    print("\nPEMBELIAN PER KOMODITAS:")
    tabel_komoditas = []
    for komoditas, jumlah in sorted(total_pembelian.items(), key=lambda x: x[1], reverse=True):
        persentase = (jumlah / total_kg_semua) * 100
        tabel_komoditas.append([komoditas.title(), f"{jumlah} kg", f"{persentase:.1f}%"])
    print(tabulate(tabel_komoditas, headers=["Komoditas", "Total Dibeli", "Persentase"], tablefmt="fancy_grid"))
    
    print("\nDAFTAR PETANI MITRA:")
    tabel_petani = []
    for petani in sorted(petani_list):
        # Hitung total pembelian dari petani ini
        total_dari_petani = 0
        for baris in transaksi_user:
            if baris[1] == petani:
                total_dari_petani += float(baris[3])
        tabel_petani.append([petani, f"{total_dari_petani} kg"])
    print(tabulate(tabel_petani, headers=["Nama Petani", "Total Pembelian"], tablefmt="fancy_grid"))
    
    # Tampilkan 5 transaksi terakhir
    print("\n5 TRANSAKSI TERAKHIR:")
    tabel_transaksi = []
    for baris in transaksi_user[-5:]:
        # dist, petani, kom, jumlah, tgl = baris[0], baris[1], baris[2], baris[3], baris[4]
        petani, kom, jumlah, tgl = baris[1], baris[2], baris[3], baris[4]
        tabel_transaksi.append([tgl, f"{jumlah} kg", kom, petani])
    print(tabulate(tabel_transaksi, headers=["Tanggal", "Jumlah", "Komoditas", "Dari Petani"], tablefmt="fancy_grid"))


def daftar_produk():
    cls()
    cetak_garis()
    print("DAFTAR PRODUK PANEN TERSEDIA")
    cetak_garis()
    
    data = membaca_data("panen.csv")
    
    if not data:
        print("Belum ada data panen yang tersedia.")
        return
    
    tabel_data = []
    nomor = 1
    for baris in data:
        if len(baris) >= 4:
            petani, komoditas, jumlah, tanggal = baris[0], baris[1], baris[2], baris[3]
            tabel_data.append([nomor, komoditas, f"{jumlah} kg", petani, tanggal])
            nomor += 1
    
    if tabel_data:
        headers = ["No", "Komoditas", "Stok (kg)", "Petani", "Tanggal Panen"]
        print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))
    else:
        print("Belum ada data panen yang tersedia.")


def lihat_stok_komoditas():
    cls()
    cetak_garis()
    print("STOK KOMODITAS TERSEDIA")
    cetak_garis()
    
    data = membaca_data("panen.csv")
    
    if not data:
        print("Belum ada data panen yang tersedia.")
        return
    
    stok_komoditas = {}
    for baris in data:
        if len(baris) >= 3:
            komoditas = baris[1].lower()
            jumlah = float(baris[2])
            
            if komoditas in stok_komoditas:
                stok_komoditas[komoditas] += jumlah
            else:
                stok_komoditas[komoditas] = jumlah
    
    if stok_komoditas:
        tabel_data = []
        for komoditas, total in sorted(stok_komoditas.items()):
            tabel_data.append([komoditas.title(), f"{total} kg"])
        
        print(tabulate(tabel_data, headers=["Komoditas", "Total Stok Tersedia"], tablefmt="fancy_grid"))
    else:
        print("Tidak ada stok tersedia.")


def cari_komoditas():
    cls()
    cetak_garis()
    print("CARI KOMODITAS")
    cetak_garis()
    cari = inputan_kosong("Nama komoditas yang dicari: ","Nama komoditas tidak boleh kosong!")
    
    data = membaca_data("panen.csv")
    ditemukan = False
    
    print(f"\nHasil pencarian '{cari}':")
    cetak_garis()
    
    tabel_data = [] 
    
    for baris in data:
        if len(baris) >= 4 and baris[1].lower() == cari.lower():
            tabel_data.append([baris[1], f"{baris[2]} kg", baris[0], baris[3]])
            ditemukan = True
    
    if not ditemukan:
        print(f"Komoditas '{cari}' tidak ditemukan.")
    else:
        headers = ["Komoditas", "Stok", "Petani", "Tanggal"]
        print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))


def transaksi(distributor):
    cls()
    cetak_garis()
    print("TRANSAKSI PEMBELIAN")
    cetak_garis()
    panen_data = membaca_data("panen.csv")

    print("\nDAFTAR PRODUK TERSEDIA:")
    tabel_stok = []
    for baris in panen_data:
        if len(baris) >= 4:
            petani_nama, kom_nama, jum_stok, tgl_panen = baris[0], baris[1], baris[2], baris[3]
            tabel_stok.append([petani_nama, kom_nama, f"{jum_stok} kg", tgl_panen])
    headers = ["Nama Petani", "Komoditas", "Stok Tersedia", "Tanggal Panen"]
    print(tabulate(tabel_stok, headers=headers, tablefmt="fancy_grid"))

    
    petani = inputan_kosong("Nama petani: ", "Nama petani tidak boleh kosong!")
    komoditas = inputan_kosong("Nama komoditas: ", "Nama komoditas tidak boleh kosong!")
    jumlah_beli = memvalidasi_angka("Jumlah yang dibeli (kg): ", "Jumlah harus berupa angka positif!")
    tanggal = memvalidasi_tanggal("Tanggal transaksi (DD-MM-YYYY): ")
    
    panen_data = membaca_data("panen.csv")
    panen_baru = []
    stok_ditemukan = False
    transaksi_berhasil = False
    

    for baris in panen_data:
        if len(baris) >= 4:
            nama, kom, jumlah, tgl = baris[0], baris[1], baris[2], baris[3]
            
            if nama == petani and kom.lower() == komoditas.lower():
                stok_ditemukan = True
                stok_tersedia = float(jumlah)
                tanggal_panen = tgl
                
                if tanggal < tanggal_panen:
                    print(f"\n[ERROR] Transaksi ditolak!")
                    print(f"Tanggal transaksi ({tanggal}) tidak boleh lebih awal dari tanggal panen ({tanggal_panen})")
                    print(f"Anda tidak bisa membeli komoditas yang belum dipanen!")
                    panen_baru.append([nama, kom, jumlah, tgl])
                    continue
                
                if stok_tersedia >= jumlah_beli:
                    stok_tersisa = stok_tersedia - jumlah_beli
                    
                    menyimpan_data("transaksi.csv", 
                              [distributor, petani, komoditas, str(jumlah_beli), tanggal])
                    
                    if stok_tersisa > 0:
                        panen_baru.append([nama, kom, str(stok_tersisa), tgl])
                    
                    print(f"\n[SUKSES] Transaksi berhasil!")
                    print(f"Anda membeli {jumlah_beli} kg {komoditas} dari {petani}")
                    if stok_tersisa > 0:
                        print(f"Sisa stok: {stok_tersisa} kg")
                    else:
                        print(f"Stok habis")
                    transaksi_berhasil = True
                else:
                    print(f"\n[ERROR] Stok tidak cukup!")
                    print(f"Anda ingin beli: {jumlah_beli} kg")
                    print(f"Stok tersedia: {stok_tersedia} kg")
                    panen_baru.append([nama, kom, jumlah, tgl])
            else:
                panen_baru.append([nama, kom, jumlah, tgl])
    
    if transaksi_berhasil:
        with open("panen.csv", "w", encoding="utf-8") as file:
            
            file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n")
            for baris in panen_baru:
                file.write(",".join(baris) + "\n")
    
    if not stok_ditemukan:
        print(f"\n[ERROR] Komoditas '{komoditas}' dari petani '{petani}' tidak ditemukan!")


def lihat_transaksi():
    cls()
    cetak_garis()
    print("RIWAYAT TRANSAKSI")
    cetak_garis()
    
    data = membaca_data("transaksi.csv")
    
    if not data:
        print("Belum ada transaksi yang tercatat.")
        return
    
    tabel_data = []
    for baris in data:
        if len(baris) >= 5:
            dist, petani, kom, jumlah, tgl = baris[0], baris[1], baris[2], baris[3], baris[4]
            tabel_data.append([tgl, dist, petani, kom, f"{jumlah} kg"])
            
    headers = ["Tanggal", "Distributor", "Petani", "Komoditas", "Jumlah"]
    print(tabulate(tabel_data, headers=headers, tablefmt="fancy_grid"))

def menghapus_transaksi(username):
    cls()
    cetak_garis()
    print("HAPUS TRANSAKSI")
    cetak_garis()
    
    data_transaksi = membaca_data("transaksi.csv")
    transaksi_user = []
    
    # Tampilkan transaksi
    print("\nRiwayat Transaksi Anda:")
    nomor = 1
    mapping_index = []
    
    tabel_tampil = []
    
    for i, baris in enumerate(data_transaksi):
        if len(baris) >= 5 and baris[0] == username:
            petani, komoditas, jumlah, tanggal = baris[1], baris[2], baris[3], baris[4]
            tabel_tampil.append([nomor, tanggal, petani, komoditas, f"{jumlah} kg"])
            mapping_index.append({"index_csv": i, "data": baris})
            nomor += 1
            
    if not mapping_index:
        print("Belum ada transaksi yang tercatat.")
        return

    # Tampilkan tabel
    headers = ["No", "Tanggal", "Petani", "Komoditas", "Jumlah"]
    print(tabulate(tabel_tampil, headers=headers, tablefmt="fancy_grid"))
    
    print(f"\n{nomor}. Batal (Kembali ke menu)")
    cetak_garis()
    
    while True:
        try:
            pilihan = int(input(f"Pilih nomor transaksi yang ingin dihapus (1-{nomor}): ").strip())
            
            if pilihan == nomor:
                print("Aksi dibatalkan.")
                return
            
            elif 1 <= pilihan < nomor:
                target = mapping_index[pilihan - 1]
                data_hapus = target["data"]
                
                # Konfirmasi
                print(f"\nAnda akan menghapus transaksi:")
                print(f"Petani   : {data_hapus[1]}")
                print(f"Komoditas: {data_hapus[2]}")
                print(f"Jumlah   : {data_hapus[3]} kg")
                
                konfirmasi = input("Apakah Anda yakin? Stok akan dikembalikan ke petani (y/n): ").strip().lower()
                
                if konfirmasi == 'y':
                    # HAPUS DARI TRANSAKSI
                    index_hapus = target["index_csv"]
                    # Buat list baru tanpa baris yang dihapus
                    data_transaksi_baru = [baris for i, baris in enumerate(data_transaksi) if i != index_hapus]
                    
                    # Simpan ulang file transaksi
                    with open("transaksi.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["transaksi.csv"]) + "\n")
                        for baris in data_transaksi_baru:
                            file.write(",".join(baris) + "\n")
                    
                    # KEMBALIKAN STOK KE PETANI (PANEN.CSV)
                    petani_target = data_hapus[1]
                    komoditas_target = data_hapus[2]
                    jumlah_balik = float(data_hapus[3])
                    tanggal_transaksi = data_hapus[4] 
                    
                    data_panen = membaca_data("panen.csv")
                    stok_dikembalikan = False
                    
                    
                    for baris_panen in data_panen:
                        if len(baris_panen) >= 4:
                            if baris_panen[0] == petani_target and baris_panen[1].lower() == komoditas_target.lower():
                                # Tambahkan stok kembali ke baris ini
                                stok_lama = float(baris_panen[2])
                                baris_panen[2] = str(stok_lama + jumlah_balik)
                                stok_dikembalikan = True
                                break 
                    
                    
                    if not stok_dikembalikan:
                        data_panen.append([petani_target, komoditas_target, str(jumlah_balik), tanggal_transaksi])
                    
                    # Simpan ulang file panen
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n")
                        for baris in data_panen:
                            file.write(",".join(baris) + "\n")
                            
                    print("\nSUKSES: Transaksi dihapus dan stok telah dikembalikan ke petani.")
                    return
                else:
                    print("Penghapusan dibatalkan.")
                    return
            else:
                print(f"Pilihan tidak valid! Pilih 1-{nomor}.")
        except ValueError:
            print("Input harus berupa angka!")


def menu_distributor(username):
    while True:
        cls()
        cetak_garis()
        print(f"MENU DISTRIBUTOR - {username}")
        cetak_garis()
        print("1. Lihat daftar produk panen")
        print("2. Cari komoditas")
        print("3. Lihat stok komoditas")
        cetak_titik()
        print("4. Transaksi pembelian")
        print("5. Lihat riwayat transaksi")
        print("6. Laporan pembelian saya")
        print("7. Batalkan Transaksi")
        print("8. Logout")
        cetak_garis()
        
        pilihan = input("Pilih menu (1-8): ").strip()
        
        if pilihan == "1":
            daftar_produk()
        elif pilihan == "2":
            cari_komoditas()
        elif pilihan == "3":
            lihat_stok_komoditas()
        elif pilihan == "4":
            transaksi(username)
        elif pilihan == "5":
            lihat_transaksi()
        elif pilihan == "6":
            laporan_pembelian_distributor(username)
        elif pilihan == "7":
            menghapus_transaksi(username) 
        elif pilihan == "8":
            print("Logout berhasil!")
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-8.")
        
        input("\nTekan ENTER untuk melanjutkan...")


# === PROGRAM UTAMA ===

def main():
    
    while True:
        cls()
        print("SELAMAT DATANG DI SISTEM PENDATAAN HASIL PANEN")
        cetak_garis()
        print("MENU UTAMA")
        cetak_garis()
        print("1. Register Petani")
        print("2. Login Petani")
        print("3. Register Distributor")
        print("4. Login Distributor")
        print("5. Keluar dari Program")
        cetak_garis()
        
        pilihan = input("Pilih menu (1-5): ").strip()
        
        if pilihan == "1":
            mendaftarkan_akun("petani")
        elif pilihan == "2":
            user = login_akun("petani")
            if user:
                menu_petani(user)
        elif pilihan == "3":
            mendaftarkan_akun("distributor")
        elif pilihan == "4":
            user = login_akun("distributor")
            if user:
                menu_distributor(user)
        elif pilihan == "5":
            cetak_garis()
            print("Terima kasih telah menggunakan sistem!")
            cetak_garis()
            break
        else:
            print("Pilihan tidak valid! Silakan pilih 1-5.")
        
        if pilihan != "5":
            input("\nTekan ENTER untuk kembali ke menu utama...")


if __name__ == "__main__":
    main()