import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman & Tema Pastel
st.set_page_config(page_title="idMe Error Tracker SKTB", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #FFF5F8; }
    [data-testid="stMetricValue"] { color: #FF1493; font-family: 'Courier New'; }
    .stHeader { background-color: #FFB6C1; padding: 10px; border-radius: 10px; text-align: center; }
    h1 { color: #C71585; text-shadow: 2px 2px #FFD1DC; }
    </style>
    """, unsafe_allow_html=True)

# Tajuk Dashboard
st.markdown("<div class='stHeader'><h1>🌸 Dashboard Analisis Ralat idMe SKTB 🌸</h1></div>", unsafe_allow_html=True)
st.write("")

# --- SAMBUNGAN GOOGLE SHEETS ---
url = "https://docs.google.com/spreadsheets/d/1y8BvpG0NN5WwwhSFWS2AOI4Qe8O4HYg5M-LPrMmzjk/edit#gid=1718218161"

conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Kita baca tab 'DASHBOARD'
    # header=7 bermaksud kita mula baca dari baris ke-8 (A8 & B8)
    df_raw = conn.read(spreadsheet=url, worksheet="DASHBOARD", ttl="10s", header=7)
    
    # Pilih Kolum A & B sahaja (Kelas & Jumlah Ralat)
    df = df_raw.iloc[:, [0, 1]].copy()
    df.columns = ['Kelas', 'Jumlah Ralat']
    
    # 1. Bersihkan data: Buang row yang tak ada nama kelas
    # 2. Buang row '457' (jumlah besar kat bawah tu) supaya carta tak pelik
    df = df.dropna(subset=['Kelas'])
    df = df[df['Kelas'] != '457'] # Elakkan ambil total bawah sekali sebagai kelas
    
    # Tukar Jumlah Ralat kepada nombor
    df['Jumlah Ralat'] = pd.to_numeric(df['Jumlah Ralat'], errors='coerce').fillna(0)
    
except Exception as e:
    st.error(f"Alamak! Ada masalah teknikal: {e}")
    st.stop()
# --- RINGKASAN ATAS ---
total_ralat = df['Jumlah Ralat'].sum()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Ralat Belum Setel", f"{int(total_ralat)} ⚠️")
with col2:
    # Mencari kelas yang paling banyak ralat untuk perhatian
    kelas_max = df.loc[df['Jumlah Ralat'].idxmax(), 'Kelas']
    st.metric("Kelas Paling Tinggi Ralat", kelas_max)
with col3:
    st.metric("Status Data", "LIVE (Auto-Refresh)")

st.divider()

# --- VISUALISASI UTAMA ---
c1, c2 = st.columns([3, 2])

with c1:
    st.subheader("📊 Statistik Ralat Ikut Kelas")
    # Warna pastel mengikut jumlah ralat (merah kalau banyak, hijau kalau sikit)
    fig = px.bar(df, x='Kelas', y='Jumlah Ralat', 
                 text_auto=True,
                 color='Jumlah Ralat',
                 color_continuous_scale='RdYlGn_r') # Red to Green reversed
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📋 Senarai Semak")
    # Papar jadual ringkas
    st.dataframe(df[['Kelas', 'Jumlah Ralat']].sort_values(by='Jumlah Ralat', ascending=False), 
                 hide_index=True, use_container_width=True)

# Footer & Manual Refresh
st.write("")
if st.button('🔄 Refresh Data Sekarang'):
    st.cache_data.clear()
    st.rerun()

st.caption("Nota Bubu: Dashboard ini akan auto-update setiap kali tanda '✓' dipadam dalam Google Sheets.")
