# ============ KONSTANTA ============
BOBOT_NILAI = {
    "A": 4.0,
    "A-": 3.75,
    "B+": 3.5,
    "B": 3.0,
    "B-": 2.75,
    "C+": 2.5,
    "C": 2.0,
    "C-": 0.0,
}


# ============ CLASS ============
class Matakuliah:
    def __init__(self, nama, sks, nilai_huruf):
        self.nama = nama
        self.sks = sks
        self.nilai_huruf = nilai_huruf

    def ambil_bobot(self):
        return BOBOT_NILAI[self.nilai_huruf]

    def ambil_mutu(self):
        # mutu = SKS x bobot
        return self.sks * self.ambil_bobot()


# ============ FUNGSI: ANALIS (Fahri) ============
def validasi_input(nama, sks, nilai_huruf):
    if nama.strip() == "":
        return False, "Nama mata kuliah tidak boleh kosong"
    if sks != int(sks) or sks < 1 or sks > 6:
        return False, "SKS harus bilangan bulat 1-6"
    if nilai_huruf not in BOBOT_NILAI:
        return False, "Nilai huruf tidak valid"
    return True, "OK"


def validasi_data_lama(ipk_lama, sks_lama):
    if ipk_lama < 0 or ipk_lama > 4.0:
        return False
    if sks_lama < 0:
        return False
    if sks_lama == 0 and ipk_lama != 0:  # semester 1
        return False
    return True


# ============ FUNGSI: LOGIKA (Zulfaa) ============
def hitung_mutu_Rekursif(daftar_mk, i):
    # Menjumlahkan mutu secara rekursif dari indeks ke-i sampai akhir list
    if i == len(daftar_mk):  # basis: sudah lewat elemen terakhir
        return 0
    return daftar_mk[i].ambil_mutu() + hitung_mutu_Rekursif(daftar_mk, i + 1)


def hitung_total_sks(daftar_mk):
    total = 0
    for mk in daftar_mk:
        total = total + mk.sks
    return total


def hitung_ip_semester(daftar_mk):
    total_sks = hitung_total_sks(daftar_mk)
    if total_sks == 0:
        return 0.0
    total_mutu = hitung_mutu_Rekursif(daftar_mk, 0)
    return total_mutu / total_sks


def proyeksi_ipk(ipk_lama, sks_lama, daftar_mk):
    sks_baru = hitung_total_sks(daftar_mk)
    mutu_baru = hitung_mutu_Rekursif(daftar_mk, 0)
    mutu_lama = ipk_lama * sks_lama
    if (sks_lama + sks_baru) == 0:
        return 0.0
    return (mutu_lama + mutu_baru) / (sks_lama + sks_baru)


def nilai_minimal_target(ipk_lama, sks_lama, sks_baru, target_ipk):
    if sks_baru == 0:
        return 0.0, "Belum ada SKS semester ini"

    mutu_dibutuhkan = target_ipk * (sks_lama + sks_baru) - (ipk_lama * sks_lama)
    rata_dibutuhkan = mutu_dibutuhkan / sks_baru  # IP semester minimal

    if rata_dibutuhkan > 4.0:
        return rata_dibutuhkan, "TIDAK TERCAPAI semester ini"
    if rata_dibutuhkan <= 0:
        return 0.0, "SUDAH AMAN, target tercapai"
    return rata_dibutuhkan, "TERCAPAI jika IP semester >= " + str(round(rata_dibutuhkan, 2))


# ============ FUNGSI: PENGUJI (Juniatun) ============
def tentukan_predikat_ip(ip):
    # Sesuaikan batas predikat dengan aturan akademik STT-NF
    if ip >= 3.51:
        return "Sangat Memuaskan"
    if ip >= 3.00:
        return "Memuaskan"
    if ip >= 2.00:
        return "Cukup"
    return "Perlu Perbaikan"