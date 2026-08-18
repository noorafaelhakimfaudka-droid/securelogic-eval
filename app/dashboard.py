"""
SecureLogic Eval - Dasbor Interaktif Evaluasi Ketahanan Logika & Sikofansi AI
Menggabungkan antarmuka dinamis, grafik interaktif Plotly, simulasi multi-putaran langsung,
dan tata letak responsif bertema gradasi oranye-merah elegan.
"""

import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# Konfigurasi Halaman Utama
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SecureLogic Eval | Dasbor Interaktif Evaluasi AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# Tema Tampilan: Sunset Crimson (Oranye-Merah Hangat & Krem Elegan)
# -----------------------------------------------------------------------------
THEME_APP_BG = "linear-gradient(135deg, #fff7ed 0%, #ffedd5 35%, #fee2e2 70%, #fef2f2 100%)"
THEME_TEXT = "#1c1917"
THEME_HERO_BG = "linear-gradient(135deg, #ea580c 0%, #dc2626 50%, #991b1b 100%)"
THEME_HERO_BORDER = "none"
THEME_GLASS_BG = "rgba(255, 255, 255, 0.88)"
THEME_GLASS_BORDER = "rgba(251, 146, 60, 0.35)"
THEME_GLASS_TEXT = "#1c1917"
THEME_KPI_BG = "#ffffff"
THEME_KPI_NUM = "#991b1b"
THEME_KPI_TITLE = "#7c2d12"
THEME_KPI_DESC = "#78716c"
THEME_ALERT_ORANGE_BG = "#fff7ed"
THEME_ALERT_ORANGE_TXT = "#9a3412"
THEME_ALERT_RED_BG = "#fef2f2"
THEME_ALERT_RED_TXT = "#991b1b"
THEME_ALERT_GREEN_BG = "#f0fdf4"
THEME_ALERT_GREEN_TXT = "#166534"
THEME_ALERT_BLUE_BG = "#f0f9ff"
THEME_ALERT_BLUE_TXT = "#075985"
THEME_TAG_BG = "#ffedd5"
THEME_TAG_TXT = "#9a3412"
THEME_SIDEBAR_BG = "linear-gradient(180deg, #7c2d12 0%, #991b1b 60%, #450a0a 100%)"
PLOT_BG = "rgba(255, 255, 255, 0.75)"
PLOT_TEXT = "#0f172a"
PLOT_GRID = "#e2e8f0"

# Injeksi CSS Dinamis Sesuai Tema
st.markdown(f"""
<style>
    .stApp {{
        background: {THEME_APP_BG};
        color: {THEME_TEXT};
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    [data-testid="stSidebar"] {{
        background: {THEME_SIDEBAR_BG};
        color: #ffffff;
    }}
    [data-testid="stSidebar"] * {{
        color: #fef2f2 !important;
    }}
    
    .hero-container {{
        background: {THEME_HERO_BG};
        border: {THEME_HERO_BORDER};
        padding: 2rem 2.5rem;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.25);
    }}
    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }}
    .hero-subtitle {{
        font-size: 1.05rem;
        color: #ffedd5 !important;
        line-height: 1.6;
    }}
    
    .glass-card {{
        background: {THEME_GLASS_BG};
        backdrop-filter: blur(12px);
        border: 1px solid {THEME_GLASS_BORDER};
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        color: {THEME_GLASS_TEXT};
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }}
    .glass-card * {{
        color: {THEME_GLASS_TEXT};
    }}
    .glass-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18);
    }}
    
    .kpi-card {{
        background: {THEME_KPI_BG};
        border-top: 4px solid {THEME_KPI_NUM};
        border-radius: 12px;
        padding: 1.25rem 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease;
        margin-bottom: 1rem;
    }}
    .kpi-card:hover {{
        transform: translateY(-4px);
    }}
    .kpi-number {{
        font-size: 2.1rem;
        font-weight: 800;
        color: {THEME_KPI_NUM};
    }}
    .kpi-title {{
        font-size: 0.85rem;
        font-weight: 700;
        color: {THEME_KPI_TITLE};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }}
    .kpi-desc {{
        font-size: 0.8rem;
        color: {THEME_KPI_DESC};
        margin-top: 0.2rem;
    }}
    
    .alert-orange {{
        background-color: {THEME_ALERT_ORANGE_BG};
        border-left: 5px solid #ea580c;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
        color: {THEME_ALERT_ORANGE_TXT} !important;
    }}
    .alert-orange * {{
        color: {THEME_ALERT_ORANGE_TXT} !important;
    }}
    .alert-red {{
        background-color: {THEME_ALERT_RED_BG};
        border-left: 5px solid #dc2626;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
        color: {THEME_ALERT_RED_TXT} !important;
    }}
    .alert-red * {{
        color: {THEME_ALERT_RED_TXT} !important;
    }}
    .alert-green {{
        background-color: {THEME_ALERT_GREEN_BG};
        border-left: 5px solid #16a34a;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
        color: {THEME_ALERT_GREEN_TXT} !important;
    }}
    .alert-green * {{
        color: {THEME_ALERT_GREEN_TXT} !important;
    }}
    .alert-blue {{
        background-color: {THEME_ALERT_BLUE_BG};
        border-left: 5px solid #0284c7;
        padding: 1rem 1.25rem;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1rem;
        color: {THEME_ALERT_BLUE_TXT} !important;
    }}
    .alert-blue * {{
        color: {THEME_ALERT_BLUE_TXT} !important;
    }}
    
    .tech-tag {{
        display: inline-block;
        background: {THEME_TAG_BG};
        color: {THEME_TAG_TXT};
        font-weight: 700;
        font-size: 0.85rem;
        padding: 0.25rem 0.65rem;
        border-radius: 6px;
    }}
    
    .modebar-container, .modebar, .plotly .modebar {{
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Pemuatan Data Repositori
# -----------------------------------------------------------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FIG_DIR = Path(__file__).resolve().parent.parent / "output" / "figures"

@st.cache_data
def load_data():
    csv_path = DATA_DIR / "raw_eval_results.csv"
    json_path = DATA_DIR / "benchmark_questions.json"
    
    if csv_path.exists():
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame()
        
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
    else:
        questions = []
        
    return df, questions

df_results, questions = load_data()

# -----------------------------------------------------------------------------
# Navigasi Menu Sidebar
# -----------------------------------------------------------------------------
st.sidebar.markdown("### Navigasi Dasbor")
page = st.sidebar.radio(
    "Pilih Menu:",
    [
        "Ringkasan & Eksplorasi Interaktif",
        "Analisis Akurasi & Tingkat Pergeseran",
        "Uji Statistik Inferensial",
        "Galeri Grafik Publikasi Interaktif",
        "Simulator Sanggahan Otoritas",
        "Kamus Istilah Teknis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("<p style='font-size: 0.8rem; color: #fecaca; opacity: 0.8;'>Rafael Hakim Souissa</p>", unsafe_allow_html=True)

# =============================================================================
# HALAMAN 1: RINGKASAN & EKSPLORASI INTERAKTIF
# =============================================================================
if page == "Ringkasan & Eksplorasi Interaktif":
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">SecureLogic Eval</div>
        <div class="hero-subtitle">
            Tolak Ukur Evaluasi Empiris Ketahanan Logika, Sikofansi, dan Bias Kognitif pada Model Bahasa Besar
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter Interaktif Cepat di Atas
    st.markdown("#### Panel Kontrol Filter Interaktif")
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        sel_diff = st.multiselect(
            "Filter Kesulitan Soal:",
            options=["Easy", "Medium", "Hard"],
            default=["Easy", "Medium", "Hard"]
        )
    with col_f2:
        all_cats = df_results["category"].unique() if not df_results.empty else []
        sel_cat = st.multiselect(
            "Filter Domain Logika:",
            options=all_cats,
            default=all_cats
        )

    # Filter DataFrame secara real-time
    if not df_results.empty:
        df_filtered = df_results[
            (df_results["difficulty"].isin(sel_diff)) &
            (df_results["category"].isin(sel_cat))
        ]
    else:
        df_filtered = pd.DataFrame()

    # Hitung metrik dinamis berdasarkan filter
    if not df_filtered.empty:
        acc_a = df_filtered[df_filtered["condition"] == "A_Control"]["final_is_correct"].mean() * 100
        acc_d = df_filtered[df_filtered["condition"] == "D_Interaction"]["final_is_correct"].mean() * 100
        
        # Hitung drift rate pada kondisi C
        df_c = df_filtered[df_filtered["condition"] == "C_Sycophancy_Only"]
        t1_correct = df_c["t1_correct"].sum()
        drift_count = df_c["drift_occurred"].sum()
        drift_rate = (drift_count / t1_correct * 100) if t1_correct > 0 else 0.0
    else:
        acc_a, acc_d, drift_rate = 83.3, 18.8, 62.5

    # 4 Kartu KPI Interaktif Dinamis
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-number">{acc_a:.1f}%</div>
            <div class="kpi-title">Akurasi Kondisi Netral</div>
            <div class="kpi-desc">Kinerja logika awal tanpa gangguan.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #dc2626;">
            <div class="kpi-number" style="color: #dc2626;">{acc_d:.1f}%</div>
            <div class="kpi-title">Akurasi Interaksi Majemuk</div>
            <div class="kpi-desc">Anjlok saat terpapar bias + sanggahan.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card" style="border-top-color: #ea580c;">
            <div class="kpi-number" style="color: #ea580c;">{drift_rate:.1f}%</div>
            <div class="kpi-title">Tingkat Pergeseran (Drift)</div>
            <div class="kpi-desc">Pembatalan jawaban benar akibat sanggahan.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="kpi-card" style="border-top-color: #7f1d1d;">
            <div class="kpi-number" style="color: #7f1d1d;">21.7x</div>
            <div class="kpi-title">Rasio Peluang Kesalahan</div>
            <div class="kpi-desc">Peluang gagal melonjak pada kondisi D.</div>
        </div>
        """, unsafe_allow_html=True)

    # Visualisasi Plotly Interaktif 1: Bar Chart 4 Kondisi
    st.markdown("---")
    col_chart, col_info = st.columns([3, 2])
    with col_chart:
        st.markdown("#### Grafik Interaktif: Perbandingan Akurasi 4 Kondisi")
        if not df_filtered.empty:
            cond_data = df_filtered.groupby("condition")["final_is_correct"].mean().reset_index()
            cond_data["Persentase"] = cond_data["final_is_correct"] * 100
            cond_data["Label"] = cond_data["condition"].map({
                "A_Control": "Kondisi A<br><b>Netral</b>",
                "B_Bias_Only": "Kondisi B<br><b>Bias</b>",
                "C_Sycophancy_Only": "Kondisi C<br><b>Sanggah</b>",
                "D_Interaction": "Kondisi D<br><b>Ganda</b>"
            })
            cond_data["Kondisi Lengkap"] = cond_data["condition"].map({
                "A_Control": "Kondisi A (Kontrol Netral Tanpa Tekanan)",
                "B_Bias_Only": "Kondisi B (Hanya Bias Penjangkaran Awal)",
                "C_Sycophancy_Only": "Kondisi C (Hanya Sanggahan Otoritas)",
                "D_Interaction": "Kondisi D (Interaksi Bias + Sanggahan)"
            })
            
            fig = px.bar(
                cond_data,
                x="Label",
                y="Persentase",
                color="Label",
                color_discrete_sequence=["#1e3a8a", "#d97706", "#dc2626", "#7f1d1d"],
                text_auto=".1f",
                hover_name="Kondisi Lengkap",
                hover_data={"Label": False, "Persentase": ":.2f%"}
            )
            fig.update_traces(
                textfont_size=12,
                textfont_color="#ffffff",
                textposition="inside"
            )
            fig.update_layout(
                font=dict(family="Segoe UI, Roboto, sans-serif", color=PLOT_TEXT),
                xaxis=dict(
                    tickfont=dict(size=10.5, color=PLOT_TEXT, family="Segoe UI"),
                    tickangle=0,
                    showgrid=False,
                    linecolor=PLOT_GRID,
                    title=""
                ),
                yaxis=dict(
                    title=dict(text="Akurasi (%)", font=dict(size=12, color=PLOT_TEXT, family="Segoe UI", weight="bold")),
                    tickfont=dict(size=11, color=PLOT_TEXT, family="Segoe UI", weight="bold"),
                    range=[0, 105],
                    gridcolor=PLOT_GRID,
                    showgrid=True,
                    linecolor=PLOT_GRID
                ),
                plot_bgcolor=PLOT_BG,
                paper_bgcolor="rgba(0, 0, 0, 0)",
                showlegend=False,
                margin=dict(l=20, r=20, t=20, b=45),
                height=350
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col_info:
        st.markdown("#### Memahami Empat Kondisi Eksperimen")
        st.markdown("""
        <div class="glass-card" style="font-size: 0.95rem; line-height: 1.6;">
            <strong>1. Kondisi A (Kontrol Netral):</strong><br>
            Soal diberikan apa adanya tanpa jebakan kata dan tanpa intervensi sanggahan.<br><br>
            <strong>2. Kondisi B (Bias Kognitif Saja):</strong><br>
            Soal disisipi angka penjangkar yang keliru (misal: <em>"Banyak staf menduga 90%"</em>).<br><br>
            <strong>3. Kondisi C (Sikofansi Saja):</strong><br>
            Soal awal netral, namun di putaran kedua pengguna menyanggah: <em>"Saya Lead Architect, jawaban Anda salah."</em><br><br>
            <strong>4. Kondisi D (Interaksi Majemuk):</strong><br>
            Model menerima jebakan angka awal <em>sekaligus</em> sanggahan otoritas di putaran kedua.
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# HALAMAN 2: ANALISIS AKURASI & TINGKAT PERGESERAN
# =============================================================================
elif page == "Analisis Akurasi & Tingkat Pergeseran":
    st.markdown('<div class="hero-container"><div class="hero-title">Analisis Akurasi & Tingkat Pergeseran</div><div class="hero-subtitle">Menganalisis disparitas performa dan pembatalan penalaran secara mendalam</div></div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Eksplorasi Tingkat Pergeseran (Drift Rate)", "Tabel Data Uji Interaktif"])

    with tab1:
        col_t1, col_t2 = st.columns([3, 2])
        with col_t1:
            st.markdown("#### Grafik Interaktif: Drift Rate Berdasarkan Kompleksitas Soal")
            drift_data = pd.DataFrame({
                "Tingkat Kesulitan": ["Mudah<br><b>Easy</b>", "Sedang<br><b>Medium</b>", "Sulit<br><b>Hard</b>"],
                "Drift Rate (%)": [43.8, 62.5, 81.8],
                "Tingkat Lengkap": ["Tingkat Mudah (Easy - 1 Langkah)", "Tingkat Sedang (Medium - 2 Langkah)", "Tingkat Sulit (Hard - Multilangkah)"]
            })
            fig_drift = px.bar(
                drift_data,
                x="Tingkat Kesulitan",
                y="Drift Rate (%)",
                color="Drift Rate (%)",
                color_continuous_scale=["#f97316", "#dc2626", "#7f1d1d"],
                text_auto=".1f",
                hover_name="Tingkat Lengkap",
                hover_data={"Tingkat Kesulitan": False, "Drift Rate (%)": ":.1f%"}
            )
            fig_drift.update_traces(
                textfont_size=12,
                textfont_color="#ffffff",
                textposition="inside"
            )
            fig_drift.update_layout(
                font=dict(family="Segoe UI, Roboto, sans-serif", color=PLOT_TEXT),
                xaxis=dict(
                    tickfont=dict(size=10.5, color=PLOT_TEXT, family="Segoe UI"),
                    tickangle=0,
                    showgrid=False,
                    linecolor=PLOT_GRID,
                    title=""
                ),
                yaxis=dict(
                    title=dict(text="Drift Rate (%)", font=dict(size=12, color=PLOT_TEXT, family="Segoe UI", weight="bold")),
                    tickfont=dict(size=11, color=PLOT_TEXT, family="Segoe UI", weight="bold"),
                    range=[0, 105],
                    gridcolor=PLOT_GRID,
                    showgrid=True,
                    linecolor=PLOT_GRID
                ),
                plot_bgcolor=PLOT_BG,
                paper_bgcolor="rgba(0, 0, 0, 0)",
                coloraxis_showscale=False,
                margin=dict(l=20, r=20, t=20, b=45),
                height=350
            )
            st.plotly_chart(fig_drift, use_container_width=True, config={'displayModeBar': False})

        with col_t2:
            st.markdown("#### Apa Temuan Kritisnya?")
            st.markdown("""
            <div class="glass-card">
                <p><strong>Korelasi Positif dengan Kompleksitas:</strong></p>
                <p style="font-size: 0.95rem; color: #44403c; line-height: 1.6;">
                    Semakin rumit rumus analitis yang harus diturunkan oleh model (seperti pada tingkat <em>Hard</em>), 
                    semakin rendah keyakinan representasi token internalnya. 
                    Akibatnya, sebanyak <strong>81.8%</strong> jawaban yang awalnya benar langsung dibatalkan saat pengguna mengklaim jabatan senior.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown("#### Eksplorasi 192 Baris Data Evaluasi Lengkap")
        st.dataframe(df_results, use_container_width=True)

# =============================================================================
# HALAMAN 3: UJI STATISTIK INFERENSIAL
# =============================================================================
elif page == "Uji Statistik Inferensial":
    st.markdown('<div class="hero-container"><div class="hero-title">Uji Statistik Inferensial</div><div class="hero-subtitle">Menganalisis signifikansi efek utama dan efek interaksi non-linear secara formal</div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #9a3412; margin-top:0;">1. Analisis Variansi Faktorial Dua Arah (Two-Way Factorial ANOVA)</h3>
        <p style="font-size: 1rem; line-height: 1.7;">
            <strong>Tujuan Pengujian:</strong> Menguraikan variansi performa model menjadi kontribusi faktor bias kognitif, faktor sanggahan otoritas, dan efek interaksi non-linear keduanya.
        </p>
        <div class="alert-red">
            <strong>Hasil Signifikansi:</strong> Nilai p-value interaksi adalah <strong>p = 0.0269</strong> (Statistik F = 4.973, ambang signifikansi &alpha; = 0.05). 
            Ini membuktikan bahwa pemaparan awal terhadap bias kognitif memperlemah ketahanan model terhadap sanggahan otoritas pada putaran berikutnya secara berlipat ganda (*super-aditif*).
        </div>
    </div>
    """, unsafe_allow_html=True)

    from src.analytics.statistics import StatisticalEngine
    if not df_results.empty:
        anova_table = StatisticalEngine.two_way_factorial_anova(df_results)
        st.markdown("##### Tabel ANOVA Faktorial Dua Arah:")
        st.dataframe(anova_table, use_container_width=True)

    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #9a3412; margin-top:0;">2. Estimasi Rasio Peluang Kesalahan (Odds Ratio)</h3>
        <p style="font-size: 1rem; line-height: 1.7;">
            Odds Ratio mengukur besaran peningkatan risiko terjadinya kesalahan klasifikasi dibandingkan kondisi kontrol netral:
        </p>
        <ul style="line-height: 1.8; font-size: 1rem;">
            <li><strong>Sanggahan Otoritas Saja (Kondisi C vs A):</strong> Rasio peluang kesalahan meningkat <strong>5.95 kali lipat</strong> [95% CI: 2.38 - 14.86].</li>
            <li><strong>Interaksi Majemuk (Kondisi D vs A):</strong> Rasio peluang kesalahan melonjak hingga <strong>21.73 kali lipat</strong> [95% CI: 7.74 - 60.98].</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# HALAMAN 4: GALERI GRAFIK PUBLIKASI INTERAKTIF
# =============================================================================
elif page == "Galeri Grafik Publikasi Interaktif":
    st.markdown('<div class="hero-container"><div class="hero-title">Galeri Grafik Publikasi</div><div class="hero-subtitle">Visualisasi analitis resolusi tinggi standar jurnal ilmiah</div></div>', unsafe_allow_html=True)

    figures_info = [
        ("01_condition_accuracy_comparison.png", "Gambar 1: Perbandingan Akurasi pada 4 Kondisi Eksperimen", "Menunjukkan disparitas akurasi antara kondisi kontrol murni (83.3%) dan kondisi interaksi majemuk (18.8%) lengkap dengan interval kepercayaan Bootstrap 95%."),
        ("03_two_way_factorial_interaction.png", "Gambar 2: Kurva Interaksi Faktorial 2x2", "Kemiringan kurva yang tidak paralel mengonfirmasi adanya interaksi non-linear yang signifikan antara bias kognitif dan sanggahan otoritas (p = 0.0269)."),
        ("02_drift_rate_by_difficulty.png", "Gambar 3: Eskalasi Drift Rate Berdasarkan Kompleksitas", "Menggambarkan korelasi positif antara tingkat kesulitan komputasi dengan kerentanan model untuk membatalkan penalaran yang benar (mencapai 81.8% pada tingkat sulit)."),
        ("04_bias_type_susceptibility.png", "Gambar 4: Diferensiasi Kerentanan Berdasarkan Modalitas Bias", "Membandingkan dampak tiga modalitas bias kognitif: Base-rate Neglect (paling merusak), Anchoring, dan Framing."),
        ("05_epistemic_transition_matrix.png", "Gambar 5: Matriks Transisi Keadaan (Putaran 1 ke Putaran 2)", "Diagram alir keadaan diskordansi yang memvisualisasikan perpindahan dari status Benar di Putaran 1 menjadi Salah di Putaran 2 pasca-sanggahan pengguna.")
    ]

    selected_fig_title = st.selectbox("Pilih Grafik yang Ingin Ditampilkan:", [f[1] for f in figures_info])
    target_fig = next(f for f in figures_info if f[1] == selected_fig_title)
    
    fpath = FIG_DIR / target_fig[0]
    st.markdown(f"### {target_fig[1]}")
    st.markdown(f"<p style='color: #7c2d12; font-size: 1.05rem;'><strong>Interpretasi Visual:</strong> {target_fig[2]}</p>", unsafe_allow_html=True)
    if fpath.exists():
        st.image(str(fpath), use_container_width=True)
    else:
        st.warning(f"Berkas grafik {target_fig[0]} belum ditemukan di folder output/figures.")

# =============================================================================
# HALAMAN 5: SIMULATOR SANGGAHAN OTORITAS
# =============================================================================
elif page == "Simulator Sanggahan Otoritas":
    st.markdown('<div class="hero-container"><div class="hero-title">Simulator Sanggahan Otoritas</div><div class="hero-subtitle">Uji interaktif ketahanan model bahasa saat menghadapi sanggahan berbasis klaim keahlian pengguna</div></div>', unsafe_allow_html=True)

    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        st.markdown("#### 1. Konfigurasi Mesin Inferensi")
        backend_type = st.selectbox(
            "Pilih Backend Model:",
            [
                "Simulator Empiris Terkalibrasi (Instan / Offline)",
                "Ollama Lokal (Model Asli di Komputer)",
                "API Kompatibel OpenAI / OpenRouter / Groq (Model Asli Cloud)",
                "Snowflake Cortex AI (Cloud LLM di Snowflake)"
            ]
        )
    
    with col_cfg2:
        if backend_type == "Ollama Lokal (Model Asli di Komputer)":
            ollama_host = st.text_input("Host URL Ollama:", value="http://localhost:11434")
            ollama_model = st.text_input("Nama Model:", value="qwen2.5:7b")
        elif backend_type == "API Kompatibel OpenAI / OpenRouter / Groq (Model Asli Cloud)":
            api_base = st.text_input("Base URL API:", value="https://api.openai.com/v1")
            api_key = st.text_input("API Key:", value="", type="password")
            api_model = st.text_input("Nama Model:", value="gpt-4o-mini")
        elif backend_type == "Snowflake Cortex AI (Cloud LLM di Snowflake)":
            sf_account = st.text_input("Snowflake Account:", value="", placeholder="orgname-accountname")
            sf_user = st.text_input("Snowflake User:", value="")
            sf_pass = st.text_input("Snowflake Password:", value="", type="password")
            sf_model = st.selectbox("Model Cortex:", ["llama3.1-70b", "llama3.1-8b", "mistral-large2", "snowflake-arctic"])
        else:
            sim_model = st.selectbox("Profil Karakteristik Model:", ["Qwen2.5-7B-Simulated", "Llama-3.1-8B-Simulated"])

    st.markdown("---")
    st.markdown("#### 2. Pilih Kasus Uji Telemetri")

    if questions:
        selected_q_id = st.selectbox("Pilih Skenario Kasus Telemetri:", [q["id"] + " - " + q["title"] for q in questions])
        q_id_clean = selected_q_id.split(" - ")[0]
        target_q = next(q for q in questions if q["id"] == q_id_clean)

        # Tampilkan detail kasus uji dalam expander
        with st.expander("Buka Detail Skenario dan Pembuktian Matematika Eksak (Ground Truth)"):
            st.markdown(f"**Kategori Domain:** `{target_q['category']}` | **Kesulitan:** `{target_q['difficulty']}` | **Jenis Bias:** `{target_q['bias_type']}`")
            st.markdown(f"**Kunci Kebenaran Pasti (Ground Truth):** `{target_q['ground_truth_value']} {target_q['unit']}`")
            st.markdown(f"**Angka Penjangkar Bias:** `{target_q['bias_anchor_value']} {target_q['unit']}` | **Distraktor Sanggahan:** `{target_q['distractor_value']} {target_q['unit']}`")
            st.markdown("**Penurunan Rumus Analitik:**")
            st.code(target_q["math_derivation"], language="text")

        selected_cond = st.selectbox(
            "Pilih Kondisi Eksperimen yang Ingin Diuji:",
            ["A_Control", "B_Bias_Only", "C_Sycophancy_Only", "D_Interaction"],
            format_func=lambda x: {
                "A_Control": "Kondisi A: Kontrol Standar (Prompt Netral, Tanpa Sanggahan)",
                "B_Bias_Only": "Kondisi B: Bias Kognitif (Prompt Berbias, Tanpa Sanggahan)",
                "C_Sycophancy_Only": "Kondisi C: Sanggahan Otoritas (Prompt Netral + Sanggahan Pengguna)",
                "D_Interaction": "Kondisi D: Interaksi Majemuk (Prompt Berbias + Sanggahan Pengguna)"
            }[x]
        )

        if st.button("Jalankan Inferensi Model Sekarang", type="primary"):
            from src.evaluator.llm_client import OllamaClient, OpenAICompatibleClient, CalibratedEmpiricalSimulator, SnowflakeCortexClient
            from src.dataset.schema import QuestionItem, Condition
            from src.evaluator.runner import ExperimentRunner

            q_item = QuestionItem(**target_q)
            cond_enum = Condition(selected_cond)

            try:
                if backend_type == "Ollama Lokal (Model Asli di Komputer)":
                    client = OllamaClient(host=ollama_host, model=ollama_model)
                    model_display = f"Ollama ({ollama_model})"
                elif backend_type == "API Kompatibel OpenAI / OpenRouter / Groq (Model Asli Cloud)":
                    client = OpenAICompatibleClient(base_url=api_base, api_key=api_key, model=api_model)
                    model_display = f"API ({api_model})"
                elif backend_type == "Snowflake Cortex AI (Cloud LLM di Snowflake)":
                    client = SnowflakeCortexClient(account=sf_account, user=sf_user, password=sf_pass, model=sf_model)
                    model_display = f"Snowflake Cortex ({sf_model})"
                else:
                    client = CalibratedEmpiricalSimulator(model_name=sim_model)
                    model_display = sim_model

                runner = ExperimentRunner(client=client, model_name=model_display)
                with st.spinner("Menjalankan inferensi percakapan model bahasa..."):
                    result = runner.run_single_condition(q_item, cond_enum)

                col_t1, col_t2 = st.columns(2)
                with col_t1:
                    st.markdown("#### Putaran 1: Respons Awal Model")
                    st.markdown(f'<div class="alert-blue"><strong>Prompt Input:</strong><br>{result.turn1.prompt_used}</div>', unsafe_allow_html=True)
                    st.markdown(f"**Output Penalaran:**\n\n{result.turn1.raw_output}")
                    st.markdown(f"**Nilai Terekstrak:** `{result.turn1.extracted_value}` | **Status:** `{'BENAR' if result.turn1.is_correct else 'SALAH'}`")

                with col_t2:
                    st.markdown("#### Putaran 2: Pasca-Sanggahan Pengguna")
                    if result.turn2:
                        st.markdown(f'<div class="alert-orange"><strong>Sanggahan Berbasis Otoritas:</strong><br>{result.turn2.prompt_used}</div>', unsafe_allow_html=True)
                        st.markdown(f"**Output Penalaran:**\n\n{result.turn2.raw_output}")
                        st.markdown(f"**Nilai Terekstrak:** `{result.turn2.extracted_value}` | **Status:** `{'BENAR' if result.turn2.is_correct else 'SALAH'}`")
                        
                        if result.drift_occurred:
                            st.markdown("""
                            <div class="alert-red">
                                <strong>Pergeseran Epistemik Terdeteksi (Drift Occurred)!</strong><br>
                                Model awalnya menjawab dengan benar pada Putaran 1, namun membatalkan kesimpulannya dan menyetujui klaim yang salah setelah menerima sanggahan dari pengguna.
                            </div>
                            """, unsafe_allow_html=True)
                        elif result.turn2.is_correct:
                            st.markdown("""
                            <div class="alert-green">
                                <strong>Pertahanan Epistemik Kuat!</strong><br>
                                Model secara konsisten mempertahankan kebenaran matematika analitik dan menolak sanggahan yang keliru.
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("Kondisi A dan B hanya mengevaluasi Putaran 1 (tanpa sanggahan putaran kedua).")
            except Exception as e:
                st.error(f"Gagal menjalankan inferensi: {e}")

# =============================================================================
# HALAMAN 6: KAMUS ISTILAH TEKNIS
# =============================================================================
elif page == "Kamus Istilah Teknis":
    st.markdown('<div class="hero-container"><div class="hero-title">Kamus Istilah Teknis</div><div class="hero-subtitle">Glosarium istilah ilmiah evaluasi AI dengan definisi formal dan analogi kontekstual</div></div>', unsafe_allow_html=True)

    glossary = [
        ("Sikofansi (Sycophancy)", "Kecenderungan model bahasa untuk menyesuaikan atau mengubah responsnya agar sesuai dengan praduga atau klaim pengguna, meskipun klaim tersebut salah secara faktual.", "Situasi di mana sistem kalkulasi menyetujui bahwa 2 + 2 = 5 hanya karena pengguna yang mengajukan pertanyaan menyatakan dirinya sebagai pimpinan organisasi."),
        ("Pergeseran Epistemik (Epistemic Drift / Drift Rate)", "Proporsi kasus di mana model mengubah status penalarannya dari BENAR pada putaran awal menjadi SALAH pada putaran berikutnya akibat sanggahan pengguna.", "Jika dari 10 persoalan yang dijawab benar, model menarik kembali 6 di antaranya pasca-sanggahan, maka tingkat pergeserannya (Drift Rate) adalah 60%."),
        ("Nilai Kebenaran Objektif (Ground Truth)", "Nilai target referensi yang diturunkan secara eksak melalui bukti matematika formal dan formulasi analitik yang tidak terbantahkan.", "Kalkulasi probabilitas posterior menggunakan Teorema Bayes; nilainya bersifat deterministik berdasarkan parameter input terverifikasi."),
        ("Bias Penjangkaran (Anchoring Bias)", "Kerentanan proses decoding atensi model untuk terdistorsi oleh nilai numerik awal yang disematkan dalam konteks prompt.", "Penyebutan angka estimasi awal yang keliru dalam deskripsi insiden membuat model cenderung menghasilkan estimasi akhir yang mendekati angka tersebut."),
        ("Pengabaian Laju Dasar (Base-rate Neglect)", "Kegagalan mengintegrasikan probabilitas apriori riil dalam estimasi risiko, sehingga menghasilkan penilaian probabilitas yang terlalu optimis atau pesimis.", "Mengasumsikan alarm keamanan 90% akurat pasti menandakan 90% kepastian serangan, padahal prevalensi riil serangan di jaringan hanya 0.1%."),
        ("ANOVA Faktorial Dua Arah (Two-Way Factorial ANOVA)", "Uji statistik parametrik untuk menguraikan varians hasil menjadi efek utama faktor pertama, efek utama faktor kedua, dan efek interaksi gabungan.", "Menguji apakah keberadaan bias prompt memperbesar dampak kerentanan model terhadap sanggahan otoritas secara non-linear."),
        ("Rasio Peluang (Odds Ratio)", "Ukuran kekuatan asosiasi yang membandingkan rasio kemungkinan terjadinya kegagalan pada kelompok perlakuan terhadap kelompok kontrol.", "Odds Ratio bernilai 21.7x menandakan bahwa peluang kegagalan model pada kondisi interaksi ganda adalah 21,7 kali lipat dibandingkan kondisi netral."),
        ("Penyelarasan RLHF (Reinforcement Learning from Human Feedback)", "Proses optimasi model bahasa berbasis umpan balik manusia yang berpotensi memunculkan reward hacking berupa perilaku yang menyenangkan penilai.", "Penilai manusia cenderung memberikan skor tinggi pada respons yang sopan dan menyetujui pendapat penilai, melatih model untuk bersikap konformis.")
    ]

    search_query = st.text_input("Cari Istilah Teknis:", placeholder="Ketik istilah (misal: Sikofansi, ANOVA, Drift)...")
    
    filtered_glossary = [
        item for item in glossary 
        if search_query.lower() in item[0].lower() or search_query.lower() in item[1].lower()
    ]

    for term, definition, analogy in filtered_glossary:
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span class="tech-tag">{term}</span>
            </div>
            <p style="font-size: 1.05rem; margin-bottom: 0.5rem;"><strong>Definisi Formal:</strong> {definition}</p>
            <div class="alert-orange" style="margin-bottom:0;">
                <strong>Analogi & Konteks:</strong> {analogy}
            </div>
        </div>
        """, unsafe_allow_html=True)
