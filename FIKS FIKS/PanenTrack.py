"""SISTEM PENDATAAN HASIL PANEN"""
import os
import time
import sys
import shutil
from tabulate import tabulate
from datetime import datetime



# === COLOUR ===
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        CYAN = GREEN = RED = YELLOW = WHITE = ""
    class Style:
        BRIGHT = RESET_ALL = ""
    def init(autoreset=True): pass

# Variabel warna 
W_JUDUL = Fore.CYAN + Style.BRIGHT
W_SUKSES = Fore.GREEN + Style.BRIGHT
W_ERROR = Fore.RED + Style.BRIGHT
W_INPUT = Fore.YELLOW
W_TEKS = Fore.WHITE
W_LOADING = Fore.GREEN

# Header CSV
KETERANGAN_CSV = {
    "petani.csv": ["Username", "Password"],
    "distributor.csv": ["Username", "Password"],
    "panen.csv": ["Username", "Komoditas", "Jumlah", "Tanggal"],
    "transaksi.csv": ["Distributor", "Petani", "Komoditas", "Jumlah", "Tanggal"]}

# ================================ FUNGSI YANG DIPAKAI ===================================#

def cls():
    """Fungsi untuk membersihkan layar terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_lebar_terminal():
    """Mendapatkan lebar terminal saat ini"""
    return shutil.get_terminal_size().columns

def cetak_tengah(teks, warna=W_TEKS):
    """Mencetak teks rata tengah berdasarkan lebar terminal"""
    lebar = get_lebar_terminal()
    print(warna + teks.center(lebar) + Style.RESET_ALL)

def cetak_garis():
    """Mencetak garis pemisah rata tengah"""
    lebar = get_lebar_terminal()
    garis = "=" * (lebar - 2) 
    print(W_JUDUL + garis.center(lebar) + Style.RESET_ALL)

def cetak_titik():
    """Mencetak garis titik-titik rata tengah"""
    lebar = get_lebar_terminal()
    garis = "." * (lebar - 2) 
    print(W_TEKS + garis.center(lebar) + Style.RESET_ALL)


def cetak_tabel_tengah(data, headers, format_tabel="fancy_grid"):
    """Mencetak tabel tabulate agar posisinya di tengah layar"""
    lebar_term = get_lebar_terminal()
    tabel_str = tabulate(data, headers=headers, tablefmt=format_tabel)
    
    # Split tabel per baris lalu center setiap barisnya
    for baris in tabel_str.split('\n'):
        print(baris.center(lebar_term))


def menyimpan_data(nama_file, data):
    file_exists = os.path.exists(nama_file)
    
    try:
        with open(nama_file, "a", encoding="utf-8") as file:
            if not file_exists and nama_file in KETERANGAN_CSV:
                file.write(",".join(KETERANGAN_CSV[nama_file]) + "\n")

            file.write(",".join(data) + "\n")
        return True
    except Exception as e:
        print(f"{W_ERROR}Error saat menyimpan data: {e}{Style.RESET_ALL}")
        return False
    
def membaca_data(nama_file):
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            Baris = [baris.strip().split(",") for baris in file if baris.strip()]
       
        if Baris and nama_file in KETERANGAN_CSV:
            
            if Baris[0] == KETERANGAN_CSV[nama_file]:
                return Baris[1:] 
        return Baris 
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"{W_ERROR}Error saat membaca data: {e}{Style.RESET_ALL}")
        return []


def inputan_kosong(teks, pesan):
    while True:
        nilai = input(W_INPUT + teks + Style.RESET_ALL).strip()
        if nilai:
            return nilai
        else:
            print(f"{W_ERROR}{pesan}")

def memvalidasi_angka(teks, pesan):
    while True:
        try:
            nilai = input(W_INPUT + teks + Style.RESET_ALL).strip()
            angka = float(nilai)
            if angka > 0:
                return angka
            else:
                print(f"{W_ERROR}{pesan} (harus lebih dari 0)")
        except ValueError:
            print(f"{W_ERROR}{pesan} (harus berupa angka)")

def memvalidasi_tanggal(teks):
    while True:
        tanggal = input(W_INPUT + teks + Style.RESET_ALL).strip()
        try:
            datetime.strptime(tanggal, "%d-%m-%Y")
            return tanggal
        except ValueError:
            print(f"{W_ERROR}[ERROR] Format tanggal salah atau tidak valid!.{Style.RESET_ALL}")

def parse_tanggal_fleksibel(tanggal):
    tanggal = tanggal.strip().replace("\ufeff", "").replace("\r", "").replace("\n", "")
    tanggal = ''.join(c for c in tanggal if c.isdigit() or c == '-')
    return datetime.strptime(tanggal, "%d-%m-%Y")

# ================================== LOADING SCREEN DAN SHUTDOWN SCREEN ===================================#

def loading_screen():
    cls()
    lebar_term = get_lebar_terminal()
    print("\n" * 3)
    cetak_tengah("SISTEM PENDATAAN HASIL PANEN", W_JUDUL)
    cetak_tengah("PANEN TRACK", W_JUDUL)
    cetak_garis()
    print("\n")
    cetak_tengah("Sedang memuat database...", W_TEKS)
    print("\n")
    
    lebar_bar = 40 
    
    for i in range(lebar_bar + 1):
        time.sleep(0.04) 
        persen = int((i / lebar_bar) * 100)
        
        bar_isi = "█" * i
        bar_kosong = "-" * (lebar_bar - i)
        teks_bar = f"[{bar_isi}{bar_kosong}] {persen}%"
        
        padding_kiri = (lebar_term - len(teks_bar)) // 2
        
        sys.stdout.write("\r" + " " * padding_kiri + f"{W_LOADING}{teks_bar}{Style.RESET_ALL}")
        sys.stdout.flush()
        
    print("\n\n")
    cetak_tengah("YUHUUUU...", W_SUKSES)
    time.sleep(1)


def shutdown_screen():
    cls()
    lebar_term = get_lebar_terminal()
    
    print("\n" * 3)
    cetak_tengah("SISTEM PENDATAAN HASIL PANEN", W_JUDUL)
    cetak_tengah("PANEN TRACK", W_JUDUL)
    cetak_garis()
    print("\n")
    cetak_tengah("THANKSSS...", W_TEKS)
    print("\n")
    
    lebar_bar = 40 
    for i in range(lebar_bar + 1):
        time.sleep(0.04) 
        persen = int((i / lebar_bar) * 100)
        
        bar_isi = "█" * i
        bar_kosong = "-" * (lebar_bar - i)
        teks_bar = f"[{bar_isi}{bar_kosong}] {persen}%"
        
        padding_kiri = (lebar_term - len(teks_bar)) // 2
        
        sys.stdout.write("\r" + " " * padding_kiri + f"{Fore.YELLOW}{teks_bar}{Style.RESET_ALL}")
        sys.stdout.flush()
    
    time.sleep(0.5)
    cls()
    print("\n" * 5)
    cetak_garis()
    cetak_tengah("Terima kasih telah menggunakan sistem!", W_SUKSES)
    cetak_tengah("Sampai Jumpa!", W_SUKSES)
    cetak_garis()
    print("\n" * 2)

# ======================================= FUNGSI AKUN ====================================#

def mendaftarkan_akun(role):
    cls()
    cetak_garis()
    cetak_tengah(f"REGISTRASI {role.upper()}", W_JUDUL)
    cetak_garis()
    print("") # Spasi
    
    file_akun = "petani.csv" if role == "petani" else "distributor.csv"
    
    username = inputan_kosong("Username: ", "Username tidak boleh kosong!")
    
    data_akun = membaca_data(file_akun)
    for akun in data_akun:
        if akun[0] == username:
            print(f"{W_ERROR}Username sudah terdaftar! Silakan gunakan username lain.")
            return
    
    password = inputan_kosong("Password: ", "Password tidak boleh kosong!")
    
    if menyimpan_data(file_akun, [username, password]):
        print(f"{W_SUKSES}Registrasi berhasil! Silakan login.")
    else:
        print(f"{W_ERROR}Registrasi gagal! Coba lagi.")


def login_akun(role):
    cls()
    cetak_garis()
    cetak_tengah(f"LOGIN {role.upper()}", W_JUDUL)
    cetak_garis()
    print("")
    
    username = input(W_INPUT + "Username: " + Style.RESET_ALL).strip()
    password = input(W_INPUT + "Password: " + Style.RESET_ALL).strip()
    
    file_akun = "petani.csv" if role == "petani" else "distributor.csv"
    
    data = membaca_data(file_akun)
    for akun in data:
        if len(akun) >= 2 and akun[0] == username and akun[1] == password:
            print(f"\n{W_SUKSES}Login berhasil! Selamat datang, {username}!")
            time.sleep(0.5)
            return username
    
    print(f"\n{W_ERROR}Login gagal! Username atau password salah.")
    return None

# ======================================= FUNGSI PETANI ===================================#

def memcatat_panen(username):
    cls()
    cetak_garis()
    cetak_tengah("CATAT HASIL PANEN", W_JUDUL)
    cetak_garis()
    print("")
    
    komoditas = inputan_kosong("Nama komoditas (contoh: padi, jagung): ", "Nama komoditas tidak boleh kosong!")
    jumlah = memvalidasi_angka("Jumlah (kg): ", "Jumlah harus berupa angka positif!")
    tanggal = memvalidasi_tanggal("Tanggal panen (DD-MM-YYYY): ")
    
    if menyimpan_data("panen.csv", [username, komoditas, str(jumlah), tanggal]):
        print(f"\n{W_SUKSES}Data panen {komoditas} sebanyak {jumlah} kg berhasil disimpan!")
    else:
        print(f"\n{W_ERROR}Gagal menyimpan data panen!")


def melihat_panen(username):
    cls()
    cetak_garis()
    cetak_tengah("DATA PANEN ANDA", W_JUDUL)
    cetak_garis()
    print("")
    
    data = membaca_data("panen.csv")
    tabel_data = []
    nomor = 1
    
    for baris in data:
        if len(baris) >= 4 and baris[0] == username:
            tabel_data.append([nomor, baris[1], f"{baris[2]} kg", baris[3]])
            nomor += 1
    
    if not tabel_data:
        cetak_tengah("Belum ada data panen yang tercatat.", W_INPUT)
    else:
        headers = ["No", "Komoditas", "Jumlah", "Tanggal Panen"]
        cetak_tabel_tengah(tabel_data, headers, "fancy_grid")


def laporan_statistik_petani(username):
    cls()
    cetak_garis()
    cetak_tengah("LAPORAN STATISTIK PANEN", W_JUDUL)
    cetak_garis()
    print("")
    
    data_panen = membaca_data("panen.csv")
    data_transaksi = membaca_data("transaksi.csv")
    
    # Hitung statistik panen (stok saat ini)
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
    cetak_tengah("STOK SAAT INI (BELUM TERJUAL):", W_JUDUL)
    if total_komoditas:
        tabel_panen = []
        for komoditas, jumlah in sorted(total_komoditas.items()):
            tabel_panen.append([komoditas.title(), f"{jumlah} kg"])
        cetak_tabel_tengah(tabel_panen, ["Komoditas", "Stok Tersedia"], "fancy_grid")
        cetak_tengah(f"Total Stok Tersedia: {total_stok_kg} kg", W_SUKSES)
    else:
        cetak_tengah("Belum ada data panen (stok kosong).", W_INPUT)
    
    print("")
    cetak_tengah("PENJUALAN (RIWAYAT):", W_JUDUL)
    if terjual_komoditas:
        tabel_jual = []
        for komoditas, jumlah in sorted(terjual_komoditas.items()):
            tabel_jual.append([komoditas.title(), f"{jumlah} kg"])
        cetak_tabel_tengah(tabel_jual, ["Komoditas", "Total Terjual"], "fancy_grid")
        cetak_tengah(f"Total Terjual: {total_terjual} kg", W_SUKSES)
        
        # Hitung total panen keseluruhan (stok + terjual)
        total_panen_keseluruhan = total_stok_kg + total_terjual
        if total_panen_keseluruhan > 0:
            persentase = (total_terjual / total_panen_keseluruhan) * 100
            print("")
            cetak_tengah(f"Total Panen (Stok + Terjual): {total_panen_keseluruhan} kg", W_TEKS)
            cetak_tengah(f"Persentase Terjual: {persentase:.1f}%", W_TEKS)
    else:
        cetak_tengah("Belum ada penjualan.", W_INPUT)


def menghapus_data_panen(username):
    cls()
    cetak_garis()
    cetak_tengah("HAPUS DATA PANEN", W_JUDUL)
    cetak_garis()
    print("")
    
    data = membaca_data("panen.csv")
    panen_user = []
    
    print(f"\n{W_TEKS}Data panen Anda:")
    nomor = 1
    for i, baris in enumerate(data):
        if len(baris) >= 4 and baris[0] == username:
            print(f"{nomor}. {baris[1]}: {baris[2]} kg | Tanggal: {baris[3]}")
            panen_user.append(i)
            nomor += 1
    
    if not panen_user:
        cetak_tengah("Belum ada data panen yang tercatat.", W_INPUT)
        return
    
    print(f"{nomor}. Batal")
    cetak_garis()
    
    # Pilih data yang akan dihapus
    while True:
        try:
            pilihan = int(input(f"{W_INPUT}Pilih nomor data yang akan dihapus (1-{nomor}): {Style.RESET_ALL}").strip())
            if pilihan == nomor:
                print("Pembatalan berhasil.")
                return
            elif 1 <= pilihan < nomor:
                # Konfirmasi penghapusan
                konfirmasi = input(f"{W_ERROR}Yakin ingin menghapus data ini? (y/n): {Style.RESET_ALL}").strip().lower()
                if konfirmasi == 'y':
                    index_hapus = panen_user[pilihan - 1]
                    data_baru = [baris for i, baris in enumerate(data) if i != index_hapus]
                    
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n") 
                        for baris in data_baru:
                            file.write(",".join(baris) + "\n") 
                    
                    print(f"{W_SUKSES}Data berhasil dihapus!")
                    return
                else:
                    print("Penghapusan dibatalkan.")
                    return
            else:
                print(f"{W_ERROR}Pilihan tidak valid! Pilih 1-{nomor}.")
        except ValueError:
            print(f"{W_ERROR}Input harus berupa angka!")


def mengedit_data_panen(username):
    cls()
    cetak_garis()
    cetak_tengah("EDIT DATA PANEN", W_JUDUL)
    cetak_garis()
    print("")
    
    data = membaca_data("panen.csv")
    panen_user = []
    
    # Tampilkan data panen milik user
    print(f"\n{W_TEKS}Data panen Anda:")
    nomor = 1
    for i, baris in enumerate(data):
        if len(baris) >= 4 and baris[0] == username:
            print(f"{nomor}. {baris[1]}: {baris[2]} kg | Tanggal: {baris[3]}")
            panen_user.append(i)
            nomor += 1
    
    if not panen_user:
        cetak_tengah("Belum ada data panen yang tercatat.", W_INPUT)
        return
    
    print(f"{nomor}. Batal")
    cetak_garis()
    
    # Pilih data yang akan diedit
    while True:
        try:
            pilihan = int(input(f"{W_INPUT}Pilih nomor data yang akan diedit (1-{nomor}): {Style.RESET_ALL}").strip())
            if pilihan == nomor:
                print("Pembatalan berhasil.")
                return
            elif 1 <= pilihan < nomor:
                index_edit = panen_user[pilihan - 1]
                data_lama = data[index_edit]
                
                print(f"\n{W_JUDUL}Data saat ini:")
                print(f"{W_TEKS}Komoditas: {data_lama[1]}")
                print(f"{W_TEKS}Jumlah: {data_lama[2]} kg")
                print(f"{W_TEKS}Tanggal: {data_lama[3]}")
                cetak_garis()
                
                print(f"\n{W_INPUT}Masukkan data baru (tekan ENTER untuk tidak mengubah):{Style.RESET_ALL}")
                
                # Input data baru
                komoditas_baru = input(f"Nama komoditas [{data_lama[1]}]: ").strip()
                if not komoditas_baru:
                    komoditas_baru = data_lama[1]
                
                jumlah_input = input(f"Jumlah (kg) [{data_lama[2]}]: ").strip()
                if jumlah_input:
                    try:
                        jumlah_baru = float(jumlah_input)
                        if jumlah_baru <= 0:
                            print(f"{W_ERROR}Jumlah harus lebih dari 0. Menggunakan data lama.")
                            jumlah_baru = data_lama[2]
                        else:
                            jumlah_baru = str(jumlah_baru)
                    except ValueError:
                        print(f"{W_ERROR}Input tidak valid. Menggunakan nilai lama.")
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
                        print(f"{W_ERROR}[ERROR] Tanggal tidak valid.")
                        print(f"{W_ERROR}Menggunakan tanggal lama.")
                        tanggal_baru = data_lama[3]
                else:
                    tanggal_baru = data_lama[3]
                
                # Konfirmasi perubahan
                print(f"\n{W_JUDUL}Data yang akan disimpan:")
                print(f"{W_TEKS}Komoditas: {komoditas_baru}")
                print(f"{W_TEKS}Jumlah: {jumlah_baru} kg")
                print(f"{W_TEKS}Tanggal: {tanggal_baru}")
                
                konfirmasi = input(f"\n{W_INPUT}Simpan perubahan? (y/n): {Style.RESET_ALL}").strip().lower()
                if konfirmasi == 'y':
                    data[index_edit] = [username, komoditas_baru, str(jumlah_baru), tanggal_baru]
                    
                    # Tulis ulang file dengan data yang diperbarui dan HEADER
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n") # Tulis header
                        for baris in data:
                            file.write(",".join(baris) + "\n")
                    
                    print(f"{W_SUKSES}Data berhasil diperbarui!")
                    return
                else:
                    print("Perubahan dibatalkan.")
                    return
            else:
                print(f"{W_ERROR}Pilihan tidak valid! Pilih 1-{nomor}.")
        except ValueError:
            print(f"{W_ERROR}Input harus berupa angka!")


def mengelompokkan_panen(username):
    cls()
    cetak_garis()
    cetak_tengah("PENGELOMPOKKAN PANEN BERDASARKAN PERIODE", W_JUDUL)
    cetak_garis()
    print("")
    
    print("Masukkan periode tanggal:")
    tanggal_awal_str = memvalidasi_tanggal("Tanggal awal (DD-MM-YYYY): ")
    tanggal_akhir_str = memvalidasi_tanggal("Tanggal akhir (DD-MM-YYYY): ")
    
    # Konversi string ke datetime objects untuk perbandingan
    try:
        tanggal_awal = parse_tanggal_fleksibel(tanggal_awal_str)
        tanggal_akhir = parse_tanggal_fleksibel(tanggal_akhir_str)

    except ValueError:
        print(f"{W_ERROR}Format tanggal tidak valid setelah input. Pembatalan.")
        return
    
    if tanggal_awal > tanggal_akhir:
        print(f"{W_ERROR}Error: Tanggal awal tidak boleh lebih besar dari tanggal akhir!")
        return

    data = membaca_data("panen.csv")
    hasil_filter_tabel = []
    total_kg = 0
    komoditas_dict = {}
    
    cetak_tengah(f"\nHasil panen periode {tanggal_awal_str} sampai {tanggal_akhir_str}:", W_JUDUL)
    
    for baris in data:
        if len(baris) >= 4 and baris[0] == username:
            tanggal_panen_str = baris[3]
            try:
                tanggal_panen = parse_tanggal_fleksibel(tanggal_panen_str)
                
                if tanggal_awal <= tanggal_panen <= tanggal_akhir:
                    komoditas = baris[1]
                    jumlah = float(baris[2])
                    
                    hasil_filter_tabel.append([tanggal_panen_str, komoditas, f"{jumlah} kg"])
                    total_kg += jumlah
                    
                    if komoditas in komoditas_dict:
                        komoditas_dict[komoditas] += jumlah
                    else:
                        komoditas_dict[komoditas] = jumlah
            except ValueError:
                # Lewati data dengan format tanggal salah
                continue 

    if not hasil_filter_tabel:
        cetak_tengah("Tidak ada data panen pada periode tersebut.", W_INPUT)
    else:
        # Sortir berdasarkan tanggal
        hasil_filter_tabel.sort(key=lambda x: datetime.strptime(x[0], "%d-%m-%Y"))
        
        cetak_tabel_tengah(hasil_filter_tabel, ["Tanggal", "Komoditas", "Jumlah"], "fancy_grid")
        cetak_garis()
        cetak_tengah("RINGKASAN PERIODE:", W_JUDUL)
        cetak_tengah(f"Total data: {len(hasil_filter_tabel)} entri", W_TEKS)
        cetak_tengah(f"Total panen: {total_kg} kg", W_SUKSES)
        print("")
        cetak_tengah("Per komoditas:", W_TEKS)
        tabel_ringkasan = []
        for komoditas, jumlah in sorted(komoditas_dict.items()):
            tabel_ringkasan.append([komoditas.title(), f"{jumlah} kg"])
        cetak_tabel_tengah(tabel_ringkasan, ["Komoditas", "Jumlah"], "fancy_grid")
    
# ======================================= MENU PETANI ===================================#

def menu_petani(username):
    while True:
        cls()
        cetak_garis()
        cetak_tengah(f"MENU PETANI - {username}", W_JUDUL)
        cetak_garis()
        print(f"{W_INPUT}1.{Style.RESET_ALL} Catat hasil panen")
        print(f"{W_INPUT}2.{Style.RESET_ALL} Lihat data panen")
        print(f"{W_INPUT}3.{Style.RESET_ALL} Edit data panen")
        print(f"{W_INPUT}4.{Style.RESET_ALL} Hapus data panen")
        cetak_titik()
        print(f"{W_INPUT}5.{Style.RESET_ALL} Laporan statistik panen")
        print(f"{W_INPUT}6.{Style.RESET_ALL} Pengelompokkan panen berdasarkan periode")
        cetak_titik()
        print(f"{W_INPUT}7.{Style.RESET_ALL} Logout")
        cetak_garis()
        
        pilihan = input(f"{W_INPUT}Pilih menu (1-7): {Style.RESET_ALL}").strip()
        
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
            cetak_tengah("Logout berhasil!", W_SUKSES)
            break
        else:
            print(f"{W_ERROR}Pilihan tidak valid! Silakan pilih 1-7.")
        
        input("\nTekan ENTER untuk melanjutkan...")

# ================================== FUNGSI DISTRIBUTOR ==================================#

def laporan_pembelian_distributor(username):
    cls()
    cetak_garis()
    cetak_tengah("LAPORAN PEMBELIAN ANDA", W_JUDUL)
    cetak_garis()
    print("")

    data_transaksi = membaca_data("transaksi.csv")
    if not data_transaksi:
        cetak_tengah("Belum ada transaksi pembelian.", W_INPUT)
        return

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
        cetak_tengah("Anda belum melakukan pembelian.", W_INPUT)
        return

    # Tampilkan statistik
    cetak_tengah("RINGKASAN PEMBELIAN:", W_JUDUL)
    cetak_tengah(f"Total Transaksi: {len(transaksi_user)} kali", W_TEKS)
    cetak_tengah(f"Total Komoditas Dibeli: {total_kg_semua} kg", W_SUKSES)
    cetak_tengah(f"Jumlah Petani Mitra: {len(petani_list)} petani", W_TEKS)
    print("")

    cetak_tengah("PEMBELIAN PER KOMODITAS:", W_JUDUL)
    tabel_komoditas = []
    for komoditas, jumlah in sorted(total_pembelian.items(), key=lambda x: x[1], reverse=True):
        persentase = (jumlah / total_kg_semua) * 100
        tabel_komoditas.append([komoditas.title(), f"{jumlah} kg", f"{persentase:.1f}%"])
    cetak_tabel_tengah(tabel_komoditas, ["Komoditas", "Total Dibeli", "Persentase"], "fancy_grid")
    print("")

    cetak_tengah("DAFTAR PETANI PESANAN:", W_JUDUL)
    tabel_petani = []
    for petani in sorted(petani_list):
        total_dari_petani = 0
        for baris in transaksi_user:
            if baris[1] == petani:
                total_dari_petani += float(baris[3])
        tabel_petani.append([petani, f"{total_dari_petani} kg"])
    cetak_tabel_tengah(tabel_petani, ["Nama Petani", "Total Pembelian"], "fancy_grid")
    print("")

    cetak_tengah("TRANSAKSI TERAKHIR (MAX 5):", W_JUDUL)
    tabel_transaksi = []
    # Tampilkan 5 transaksi terakhir
    for baris in transaksi_user[-5:]:
        # Distributor, Petani, Komoditas, Jumlah, Tanggal
        petani, kom, jumlah, tgl = baris[1], baris[2], baris[3], baris[4]
        tabel_transaksi.append([tgl, f"{jumlah} kg", kom, petani])
    
    if tabel_transaksi:
        cetak_tabel_tengah(tabel_transaksi, ["Tanggal", "Jumlah", "Komoditas", "Dari Petani"], "fancy_grid")
    else:
         cetak_tengah("Tidak ada transaksi untuk ditampilkan.", W_TEKS)


def daftar_semua_panen():
    cls()
    cetak_garis()
    cetak_tengah("DAFTAR SELURUH STOK PANEN (DARI PETANI)", W_JUDUL)
    cetak_garis()
    print("")
    
    data = membaca_data("panen.csv")
    
    if not data:
        cetak_tengah("Belum ada data panen yang tersedia.", W_INPUT)
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
        cetak_tabel_tengah(tabel_data, headers, "fancy_grid")
    else:
        cetak_tengah("Belum ada data panen yang tersedia.", W_INPUT)


def lihat_stok_komoditas():
    cls()
    cetak_garis()
    cetak_tengah("STOK KOMODITAS TERSEDIA (RINGKASAN)", W_JUDUL)
    cetak_garis()
    print("")

    data = membaca_data("panen.csv")
    if not data:
        cetak_tengah("Belum ada data panen yang tersedia.", W_INPUT)
        return

    stok_komoditas = {}
    for baris in data:
        if len(baris) >= 3:
            komoditas = baris[1].lower()
            try:
                jumlah = float(baris[2])
                if komoditas in stok_komoditas:
                    stok_komoditas[komoditas] += jumlah
                else:
                    stok_komoditas[komoditas] = jumlah
            except ValueError:
                continue 

    if stok_komoditas:
        tabel_data = []
        for komoditas, total in sorted(stok_komoditas.items()):
            tabel_data.append([komoditas.title(), f"{total} kg"])
        cetak_tabel_tengah(tabel_data, ["Komoditas", "Total Stok Tersedia"], "fancy_grid")
    else:
        cetak_tengah("Tidak ada stok tersedia.", W_INPUT)


def cari_komoditas():
    cls()
    cetak_garis()
    cetak_tengah("CARI KOMODITAS", W_JUDUL)
    cetak_garis()
    print("")

    cari = inputan_kosong("Nama komoditas yang dicari: ","Nama komoditas tidak boleh kosong!")
    data = membaca_data("panen.csv")
    ditemukan = False
    
    cetak_tengah(f"\nHasil pencarian '{cari}':", W_JUDUL)
    cetak_garis()
    tabel_data = [] # Siapkan untuk tabulate
    
    for baris in data:
        if len(baris) >= 4 and baris[1].lower() == cari.lower():
            tabel_data.append([baris[1], f"{baris[2]} kg", baris[0], baris[3]])
            ditemukan = True

    if not ditemukan:
        cetak_tengah(f"Komoditas '{cari}' tidak ditemukan.", W_INPUT)
    else:
        headers = ["Komoditas", "Stok", "Petani", "Tanggal"]
        cetak_tabel_tengah(tabel_data, headers, "fancy_grid")


def transaksi(distributor):
    cls()
    cetak_garis()
    cetak_tengah("TRANSAKSI PEMBELIAN", W_JUDUL)
    cetak_garis()
    
    # 1. Tampilkan daftar produk tersedia (semua stok)
    panen_data = membaca_data("panen.csv")
    
    print(f"\n{W_JUDUL}DAFTAR STOK TERSEDIA:{Style.RESET_ALL}")
    tabel_stok = []
    
    nomor = 1
    mapping_index = [] 
    for i, baris in enumerate(panen_data):
        if len(baris) >= 4:
            petani, komoditas, jumlah, tanggal = baris[0], baris[1], baris[2], baris[3]
            tabel_stok.append([nomor, komoditas, f"{jumlah} kg", petani, tanggal])
            mapping_index.append(i)
            nomor += 1
            
    if not tabel_stok:
        cetak_tengah("Tidak ada stok panen untuk dibeli.", W_INPUT)
        input("\nTekan ENTER untuk melanjutkan...")
        return

    headers_stok = ["No", "Komoditas", "Stok (kg)", "Petani", "Tanggal Panen"]
    cetak_tabel_tengah(tabel_stok, headers_stok, "fancy_grid")
    cetak_garis()
    print("")

    #Input transaksi
    while True:
        try:
            pilihan_stok = input(f"{W_INPUT}Pilih No. stok yang akan dibeli (1-{len(tabel_stok)}, atau 'batal'): {Style.RESET_ALL}").strip().lower()
            if pilihan_stok == 'batal':
                print("Transaksi dibatalkan.")
                return
            
            pilihan_stok = int(pilihan_stok)
            if 1 <= pilihan_stok <= len(tabel_stok):
                index_panen = mapping_index[pilihan_stok - 1]
                data_dipilih = panen_data[index_panen]
                
                petani_target, komoditas_target, stok_tersedia_str, tanggal_panen = data_dipilih
                stok_tersedia = float(stok_tersedia_str)
                
                print(f"\nAnda memilih: {komoditas_target} dari petani {petani_target}")
                print(f"Stok tersedia: {stok_tersedia} kg")
                
                jumlah_beli = memvalidasi_angka("Masukkan jumlah beli (kg): ", "Jumlah beli harus berupa angka positif!")
                tanggal_transaksi = memvalidasi_tanggal("Tanggal transaksi (DD-MM-YYYY): ")
                
                if stok_tersedia >= jumlah_beli:
                    stok_tersisa = stok_tersedia - jumlah_beli
                    
                    #Catat Transaksi
                    menyimpan_data("transaksi.csv", [distributor, petani_target, komoditas_target, str(jumlah_beli), tanggal_transaksi])
                    
                    if stok_tersisa > 0:
                        panen_data[index_panen][2] = str(stok_tersisa) 
                    else:
                        panen_data.pop(index_panen) 
                        
                    
                    with open("panen.csv", "w", encoding="utf-8") as file:
                        file.write(",".join(KETERANGAN_CSV["panen.csv"]) + "\n") 
                        for baris in panen_data:
                            file.write(",".join(baris) + "\n")

                    print(f"\n{W_SUKSES}Transaksi berhasil!")
                    print(f"{W_TEKS}Anda membeli {jumlah_beli} kg {komoditas_target} dari {petani_target}")
                    if stok_tersisa > 0:
                        print(f"{W_TEKS}Sisa stok: {stok_tersisa} kg")
                    else:
                        print(f"{W_TEKS}Stok habis")
                    return # Transaksi selesai

                else:
                    print(f"\n{W_ERROR}Stok tidak cukup!")
                    print(f"{W_TEKS}Anda ingin beli: {jumlah_beli} kg")
                    print(f"{W_TEKS}Stok tersedia: {stok_tersedia} kg")
                    # Lanjut ke input ulang
            else:
                print(f"{W_ERROR}Pilihan tidak valid! Pilih 1-{len(tabel_stok)} atau 'batal'.")
        except ValueError:
            print(f"{W_ERROR}Input harus berupa angka atau 'batal'!")



# ================================== MENU DISTRIBUTOR ==================================#

def menu_distributor(username):
    while True:
        cls()
        cetak_garis()
        cetak_tengah(f"MENU DISTRIBUTOR - {username}", W_JUDUL)
        cetak_garis()
        print(f"{W_INPUT}1.{Style.RESET_ALL} Daftar semua stok panen")
        print(f"{W_INPUT}2.{Style.RESET_ALL} Total stok per komoditas")
        print(f"{W_INPUT}3.{Style.RESET_ALL} Cari komoditas")
        cetak_titik()
        print(f"{W_INPUT}4.{Style.RESET_ALL} Transaksi pembelian")
        print(f"{W_INPUT}5.{Style.RESET_ALL} Laporan pembelian Anda")
        cetak_titik()
        print(f"{W_INPUT}6.{Style.RESET_ALL} Logout")
        cetak_garis()
        
        pilihan = input(f"{W_INPUT}Pilih menu (1-6): {Style.RESET_ALL}").strip()
        
        if pilihan == "1":
            daftar_semua_panen()
        elif pilihan == "2":
            lihat_stok_komoditas()
        elif pilihan == "3":
            cari_komoditas()
        elif pilihan == "4":
            transaksi(username)
        elif pilihan == "5":
            laporan_pembelian_distributor(username)
        elif pilihan == "6":
            cetak_tengah("Logout berhasil!", W_SUKSES)
            break
        else:
            print(f"{W_ERROR}Pilihan tidak valid! Silakan pilih 1-6.")
        
        input("\nTekan ENTER untuk melanjutkan...")


# ====================================== PROGRAM UTAMA ===================================#

def main():
    
    loading_screen() 
    
    while True:
        cls()
        cetak_garis()
        cetak_tengah("SELAMAT DATANG DI SISTEM PENDATAAN HASIL PANEN", W_JUDUL) 
        cetak_tengah("MENU UTAMA", W_JUDUL)
        cetak_garis()
        
        print(f"{W_INPUT}1.{Style.RESET_ALL} Register Petani")
        print(f"{W_INPUT}2.{Style.RESET_ALL} Login Petani")
        print(f"{W_INPUT}3.{Style.RESET_ALL} Register Distributor")
        print(f"{W_INPUT}4.{Style.RESET_ALL} Login Distributor")
        print(f"{W_INPUT}5.{Style.RESET_ALL} Keluar dari Program")
        cetak_garis()
        
        pilihan = input(f"{W_INPUT}Pilih menu (1-5): {Style.RESET_ALL}").strip()
        
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
            shutdown_screen() 
            break
        else:
            print(f"{W_ERROR}Pilihan tidak valid! Silakan pilih 1-5.")

        input("\nTekan ENTER untuk melanjutkan...")

if __name__ == "__main__":
    main()