import streamlit as st
from logika import *

st.set_page_config(
    page_title="TrackIP — Kalkulator IP & Target IPK",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Styling ringan: tipografi rapi, angka tabular sejajar, tanpa badge/efek berlebihan
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

      html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      }
      .block-container {
        max-width: 1120px;
        padding-top: 2.25rem;
        padding-bottom: 3rem;
      }
      .mono-num {
        font-family: 'IBM Plex Mono', monospace;
        font-variant-numeric: tabular-nums;
      }
      .trackip-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
      }
      .trackip-label {
        font-size: 0.78rem;
        color: #64748B;
        margin-bottom: 0.2rem;
      }
      .trackip-value {
        font-family: 'IBM Plex Mono', monospace;
        font-variant-numeric: tabular-nums;
        font-size: 2rem;
        font-weight: 600;
        color: #0F172A;
        line-height: 1.15;
      }
      .trackip-sub {
        font-size: 0.82rem;
        color: #0369A1;
        font-weight: 500;
        margin-top: 0.25rem;
      }
      hr.hairline {
        border: none;
        border-top: 1px solid #E2E8F0;
        margin: 1rem 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============ FUNGSI: ANTARMUKA (Hanif) ============
def tampilkan_rekap_ip(daftar_mk):
    if len(daftar_mk) == 0:
        st.info("Belum ada mata kuliah. Tambahkan minimal satu mata kuliah di form atas.")
        return

    h = st.columns([0.6, 3.6, 0.9, 0.9, 1.0, 1.0, 1.2])
    h[0].caption("No")
    h[1].caption("Mata Kuliah")
    h[2].caption("SKS")
    h[3].caption("Nilai")
    h[4].caption("Bobot")
    h[5].caption("Mutu")
    h[6].caption("Aksi")

    for k, mk in enumerate(daftar_mk):
        baris = st.columns([0.6, 3.6, 0.9, 0.9, 1.0, 1.0, 1.2], vertical_alignment="center")
        baris[0].markdown(f"<span class='mono-num'>{k + 1}</span>", unsafe_allow_html=True)
        baris[1].write(mk.nama)
        baris[2].markdown(f"<span class='mono-num'>{mk.sks}</span>", unsafe_allow_html=True)
        baris[3].markdown(f"<span class='mono-num'><b>{mk.nilai_huruf}</b></span>", unsafe_allow_html=True)
        baris[4].markdown(f"<span class='mono-num'>{mk.ambil_bobot():.2f}</span>", unsafe_allow_html=True)
        baris[5].markdown(f"<span class='mono-num'>{mk.ambil_mutu():.2f}</span>", unsafe_allow_html=True)
        if baris[6].button("Hapus", key=f"hapus_{k}", use_container_width=True):
            daftar_mk.pop(k)
            st.rerun()

    st.markdown("<hr class='hairline' />", unsafe_allow_html=True)
    total_sks = hitung_total_sks(daftar_mk)
    total_mutu = sum(mk.ambil_mutu() for mk in daftar_mk)
    f1, f2, f3 = st.columns([4.2, 2.0, 3.0])
    f1.markdown(f"**Total ({len(daftar_mk)} mata kuliah)**")
    f2.markdown(f"<span class='mono-num'><b>{total_sks} SKS</b></span>", unsafe_allow_html=True)
    f3.markdown(f"<span class='mono-num'>Mutu: <b>{total_mutu:.2f}</b></span>", unsafe_allow_html=True)


# ============ INISIALISASI STATE ============
if "DAFTAR_MK" not in st.session_state:
    st.session_state.DAFTAR_MK = []


# ============ HEADER ============
st.title("TrackIP")
st.caption("Kalkulator IP Semester dan Simulasi Target IPK · Skala 4.00")
st.markdown("<hr class='hairline' />", unsafe_allow_html=True)


# ============ LAYOUT DUA KOLOM ============
col_kiri, col_kanan = st.columns([7, 5], gap="large")

with col_kiri:
    # --- 1. Data Akademik Sebelumnya & Target ---
    st.subheader("Data Akademik")
    st.caption("Isi 0 untuk IPK lama dan SKS lama jika kamu masih semester 1.")

    c1, c2, c3 = st.columns(3)
    with c1:
        ipk_lama = st.number_input("IPK lama", min_value=0.0, max_value=4.0, value=0.0, step=0.01, format="%.2f")
    with c2:
        sks_lama = st.number_input("SKS lama", min_value=0, value=0, step=1)
    with c3:
        target_ipk = st.number_input("Target IPK", min_value=0.0, max_value=4.0, value=3.50, step=0.01, format="%.2f")

    data_lama_valid = validasi_data_lama(ipk_lama, sks_lama)
    if not data_lama_valid:
        st.error("IPK atau SKS lama tidak valid. Jika SKS lama 0, IPK lama harus 0.00.")

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    # --- 2. Form Tambah Mata Kuliah ---
    st.subheader("Tambah Mata Kuliah")
    with st.form("form_tambah_mk", clear_on_submit=True):
        f_nama, f_sks, f_nilai, f_btn = st.columns([4.5, 1.5, 2.0, 2.0], vertical_alignment="bottom")
        with f_nama:
            nama = st.text_input("Nama mata kuliah", placeholder="Contoh: Algoritma & Pemrograman")
        with f_sks:
            sks = st.number_input("SKS", min_value=1, max_value=6, value=3, step=1)
        with f_nilai:
            nilai_huruf = st.selectbox("Nilai huruf", list(BOBOT_NILAI.keys()))
        with f_btn:
            submitted = st.form_submit_button("Tambah", type="primary", use_container_width=True)

        if submitted:
            valid, pesan = validasi_input(nama, sks, nilai_huruf)
            if valid:
                st.session_state.DAFTAR_MK.append(Matakuliah(nama.strip(), sks, nilai_huruf))
                st.success(f"'{nama.strip()}' ditambahkan.")
            else:
                st.error(pesan)

    st.markdown("<div style='height: 0.75rem'></div>", unsafe_allow_html=True)

    # --- 3. Rekap Mata Kuliah ---
    h_rekap, h_reset = st.columns([4, 1], vertical_alignment="center")
    h_rekap.subheader("Rekap Mata Kuliah")
    if len(st.session_state.DAFTAR_MK) > 0:
        if h_reset.button("Reset", use_container_width=True):
            st.session_state.DAFTAR_MK = []
            st.rerun()

    tampilkan_rekap_ip(st.session_state.DAFTAR_MK)


with col_kanan:
    st.subheader("Hasil & Simulasi Target")
    daftar = st.session_state.DAFTAR_MK

    if len(daftar) == 0:
        st.markdown(
            """
            <div class="trackip-card">
              <div class="trackip-label">Ringkasan Perhitungan</div>
              <p style="color:#64748B; font-size:0.9rem; margin:0.4rem 0 0 0;">
                Hasil IP Semester, Proyeksi IPK, dan kebutuhan nilai minimal akan muncul otomatis di sini setelah kamu menambahkan minimal satu mata kuliah.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif not data_lama_valid:
        st.warning("Perbaiki isian IPK/SKS lama terlebih dahulu untuk melihat proyeksi IPK.")
    else:
        ip_sem = hitung_ip_semester(daftar)
        predikat = tentukan_predikat_ip(ip_sem)
        ipk_proyeksi = proyeksi_ipk(ipk_lama, sks_lama, daftar)
        sks_baru = hitung_total_sks(daftar)
        minimal, status = nilai_minimal_target(ipk_lama, sks_lama, sks_baru, target_ipk)

        delta_ipk = ipk_proyeksi - ipk_lama if sks_lama > 0 else 0.0
        delta_teks = (
            f"+{delta_ipk:.2f} dari IPK lama"
            if sks_lama > 0 and delta_ipk > 0
            else f"{delta_ipk:.2f} dari IPK lama"
            if sks_lama > 0 and delta_ipk < 0
            else "Semester pertama" if sks_lama == 0 else "Tetap dibanding IPK lama"
        )

        # Kartu 1: IP Semester & Proyeksi IPK
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(
                f"""
                <div class="trackip-card">
                  <div class="trackip-label">IP Semester Ini</div>
                  <div class="trackip-value">{ip_sem:.2f}</div>
                  <div class="trackip-sub">{predikat}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f"""
                <div class="trackip-card">
                  <div class="trackip-label">Proyeksi IPK</div>
                  <div class="trackip-value">{ipk_proyeksi:.2f}</div>
                  <div class="trackip-sub" style="color:#475569;">{delta_teks}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Kartu 2: Simulasi Target IPK
        tampilan_min = f"{max(0.0, minimal):.2f}"
        catatan_min = (
            "Melebihi batas maksimal 4.00 pada jumlah SKS semester ini."
            if minimal > 4.0
            else f"Untuk mencapai target IPK {target_ipk:.2f} dengan total {sks_lama + sks_baru} SKS."
        )
        st.markdown(
            f"""
            <div class="trackip-card">
              <div class="trackip-label">IP Semester Minimal untuk Target ({target_ipk:.2f})</div>
              <div class="trackip-value">{tampilan_min}</div>
              <div class="trackip-sub">Status: {status}</div>
              <p style="font-size:0.82rem; color:#475569; margin:0.5rem 0 0 0;">{catatan_min}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Lihat Skala Bobot Nilai"):
        st.table(
            [{"Nilai Huruf": k, "Bobot": f"{v:.2f}"} for k, v in BOBOT_NILAI.items()]
        )