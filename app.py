# app.py - Antarmuka Streamlit TrackIP
# Jalankan dengan: streamlit run app.py

import streamlit as st
from logika import *

# ============ FUNGSI: ANTARMUKA (Hanif) ============
def tampilkan_rekap_ip(daftar_mk):
    if len(daftar_mk) == 0:
        st.info("Belum ada mata kuliah")
        return

    # Header tabel
    h = st.columns([1, 4, 1, 1, 1, 1, 2])
    h[0].write("**No**")
    h[1].write("**Mata Kuliah**")
    h[2].write("**SKS**")
    h[3].write("**Nilai**")
    h[4].write("**Bobot**")
    h[5].write("**Mutu**")
    h[6].write("**Aksi**")

    # Baris tabel: perulangan untuk setiap mata kuliah
    nomor = 1
    for k in range(len(daftar_mk)):
        mk = daftar_mk[k]
        baris = st.columns([1, 4, 1, 1, 1, 1, 2])
        baris[0].write(nomor)
        baris[1].write(mk.nama)
        baris[2].write(mk.sks)
        baris[3].write(mk.nilai_huruf)
        baris[4].write(mk.ambil_bobot())
        baris[5].write(mk.ambil_mutu())
        if baris[6].button("Hapus", key="hapus_" + str(k)):
            daftar_mk.pop(k)   # hapus mata kuliah ke-k
            st.rerun()         # muat ulang halaman
        nomor = nomor + 1

    st.write("**Total SKS: " + str(hitung_total_sks(daftar_mk)) + "**")


# ============ PROGRAM UTAMA ============
# Simpan daftar mata kuliah di session_state supaya tidak hilang
if "DAFTAR_MK" not in st.session_state:
    st.session_state.DAFTAR_MK = []

st.title("TrackIP")
st.write("Kalkulator IP Semester dan Simulasi Target IPK")

# --- Input data lama & target ---
st.subheader("Data Akademik")
st.write("Isi 0 untuk IPK lama dan SKS lama jika kamu masih semester 1.")
nama_mahasiswa = st.text_input("Nama Mahasiswa")
ipk_lama = st.number_input("IPK lama", min_value=0.0, max_value=4.0, value=0.0, step=0.01)
sks_lama = st.number_input("SKS lama", min_value=0, value=0, step=1)
target_ipk = st.number_input("Target IPK", min_value=0.0, max_value=4.0, value=3.5, step=0.01)

# --- Input mata kuliah ---
st.subheader("Tambah Mata Kuliah")
nama = st.text_input("Nama mata kuliah")
sks = st.number_input("SKS", min_value=1, max_value=6, value=3, step=1)
nilai_huruf = st.selectbox("Nilai huruf", list(BOBOT_NILAI.keys()))

if st.button("Tambah"):
    valid, pesan = validasi_input(nama, sks, nilai_huruf)
    if valid:
        st.session_state.DAFTAR_MK.append(Matakuliah(nama, sks, nilai_huruf))
        st.success("Mata kuliah ditambahkan")
    else:
        st.error(pesan)

# --- Rekap (tombol Hapus ada di dalam tabel) ---
st.subheader("Rekap Mata Kuliah")
tampilkan_rekap_ip(st.session_state.DAFTAR_MK)

if st.button("Reset"):
    st.session_state.DAFTAR_MK = []
    st.rerun()

# --- Hitung ---
st.subheader("Hasil")
if st.button("Hitung"):
    daftar = st.session_state.DAFTAR_MK

    if nama_mahasiswa.strip() == "":
        st.error("Masukkan nama kamu terlebih dahulu")
    elif len(daftar) == 0:
        st.error("Tambahkan minimal 1 mata kuliah")
    elif validasi_data_lama(ipk_lama, sks_lama) == False:
        st.error("IPK/SKS lama tidak valid")
    else:
        st.write("**Nama Mahasiswa: " + nama_mahasiswa + "**")

        # Fitur 1: Kalkulator IP Semester
        ip_sem = hitung_ip_semester(daftar)
        predikat = tentukan_predikat_ip(ip_sem)
        st.write("**IP Semester: " + str(round(ip_sem, 2)) + " (" + predikat + ")**")

        # Fitur 2: Simulasi Target IPK
        ipk_proyeksi = proyeksi_ipk(ipk_lama, sks_lama, daftar)
        sks_baru = hitung_total_sks(daftar)
        minimal, status = nilai_minimal_target(ipk_lama, sks_lama, sks_baru, target_ipk)

        st.write("Proyeksi IPK: " + str(round(ipk_proyeksi, 2)))
        st.write("IP semester minimal untuk target: " + str(round(minimal, 2)))
        st.write("Status: " + status)