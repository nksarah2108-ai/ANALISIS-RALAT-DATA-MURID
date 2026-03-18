import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman
st.set_page_config(page_title="idMe Master SKTB", layout="wide")

# --- TEMA CERAH (CLEAN & PINK) ---
st.markdown("""
    <style>
    .stApp { background-color: #fdf2f5; }
    .metric-card {
        background-color: white; padding: 15px; border-radius: 12px;
        border: 1px solid #ffc1d6; text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
    }
    h1, h3 { color: #ff4d88; text-align: center; }
    [data-testid="stMetricValue"] { color: #ff4d88; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk
st.markdown("<h1>🌸 Dashboard Ralat idMe (Master) 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h3>SK Telok Berembang</h3>", unsafe_allow_html=True)

# URL Master Tab (Guna link Publish to Web - CSV)
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSC4K9zTk5to3U37As72duwLP7GRqYMkauaAhjr6ANe8s6bl7Qz85ojUXeSDOYw3-iQkMvKV-gq4ZXf/pub?output=csv"

@st.cache_data(ttl=10)
def load_master_data():
    # Baca data (Adjust skiprows jika tajuk Master Tab Cikgu bukan di baris 1)
    df = pd.read_csv(url)
    
    # Pastikan nama kolum bersih
    df.columns = df.columns.str.strip()
    
    # Tukar Jumlah Ralat kepada nombor
    if 'Jumlah Ralat' in df.columns:
        df['Jumlah Ralat'] = pd.to_numeric(df['Jumlah Ralat'], errors='coerce').fillna(0)
    
    return df

try:
    df_master = load_master_data()
    
    # --- BAHAGIAN DROPDOWN (PILIH KELAS) ---
    st.write("### 🔍 Carian Mengikut Kelas")
    senarai_kelas = sorted(df_master['Kelas'].unique().tolist())
    pilihan_kelas = st.selectbox("Sila Pilih Kelas:", ["SEMUA KELAS"] + senarai_kelas)

    # Tapis data mengikut pilihan
    if pilihan_kelas == "SEMUA KELAS":
        df_filtered = df_master
    else:
        df_filtered = df_master[df_master['Kelas'] == pilihan_kelas]

    # --- KAD RINGKASAN (METRICS) ---
    total_murid_ralat = len(df_filtered[df_filtered['Jumlah Ralat'] > 0])
    total_kes_ralat = int(df_filtered['Jumlah Ralat'].sum())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-card'><h4>Murid Terlibat</h4><h2>{total_murid_ralat}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><h4>Jumlah Kes Ralat</h4><h2>{total_kes_ralat}</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><h4>Status</h4><h2 style='color:#ff4d88;'>TINDAKAN GURU</h2></div>", unsafe_allow_html=True)

    st.divider()

    # --- JADUAL DETAIL (NAMA MURID & JENIS RALAT) ---
    st.write(f"### 📋 Senarai Murid & Jenis Ralat: {pilihan_kelas}")
    
    # Pilih kolum yang penting sahaja untuk dipaparkan
    # (Pastikan nama kolum ni sama dengan dalam Google Sheet Cikgu)
    cols_to_show = ['Nama Murid', 'Kelas', 'Jumlah Ralat']
    
    # Jika Cikgu ada kolum ralat spesifik, Bubu tambahkan sekali
    all_cols = df_master.columns.tolist()
    ralat_cols = [c for c in all_cols if c not in ['Nama Murid', 'Kelas', 'Jumlah Ralat', 'Bil']]
    
    # Paparkan jadual
    st.dataframe(df_filtered[cols_to_show + ralat_cols], 
                 use_container_width=True, 
                 hide_index=True)

    # --- GRAF PRESTASI ---
    st.write("---")
    st.write("### 📊 Analisis Ralat")
    fig = px.bar(df_filtered.head(15), x='Nama Murid', y='Jumlah Ralat', 
                 color='Jumlah Ralat', 
                 color_continuous_scale='RdPu')
    fig.update_layout(plot_bgcolor='white', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Sila pastikan link CSV Master Tab betul dan tajuk kolum tepat: {e}")

if st.button('🔄 Kemaskini Data Sekarang'):
    st.cache_data.clear()
    st.rerun()
