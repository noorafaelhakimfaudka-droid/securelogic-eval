# Panduan Lengkap: Deploy Streamlit App di Snowflake (Streamlit in Snowflake / SiS)

Proyek **SecureLogic Eval** dapat di-deploy secara *native* langsung di dalam platform **Snowflake** menggunakan fitur bawaan **Streamlit in Snowflake (SiS)**.

---

## Opsi 1: Deploy Lewat Snowflake Web Console (Snowsight UI) — Paling Mudah (2 Menit)

1. **Buka Snowflake Snowsight:**
   - Masuk ke akun Snowflake Anda di browser (`https://app.snowflake.com`).
2. **Navigasi ke Menu Streamlit:**
   - Di menu sebelah kiri, klik **Projects** $\to$ **Streamlit**.
   - Klik tombol biru **`+ Streamlit App`** di pojok kanan atas.
3. **Konfigurasi Aplikasi:**
   - **App Name:** `SECURELOGIC_EVAL_APP`
   - **App Location (Database & Schema):** Pilih `SECURELOGIC_DB` (atau database apa pun yang Anda miliki, misal `DEMO_DB.PUBLIC`).
   - **Warehouse:** Pilih warehouse aktif Anda (misal `COMPUTE_WH`).
   - Klik **Create**.
4. **Pasang Kode:**
   - Hapus kode contoh bawaan Snowflake di editor.
   - Buka berkas [`snowflake/streamlit_in_snowflake.py`](file:///c:/Users/asus/.gemini/antigravity-ide/scratch/securelogic-eval/snowflake/streamlit_in_snowflake.py) di proyek ini.
   - Salin seluruh isi berkas dan tempelkan (*Paste*) ke editor Snowflake.
5. **Tambahkan Paket Eksternal (Packages):**
   - Di bagian atas editor Streamlit Snowflake, klik dropdown **Packages**.
   - Cari dan tambahkan:
     * `plotly`
     * `pandas`
     * `scipy`
6. **Jalankan Aplikasi:**
   - Klik tombol **`Run`** di pojok kanan atas.
   - Aplikasi Streamlit interaktif Anda kini aktif dan dapat diakses langsung di Snowflake Cloud!

---

## Opsi 2: Deploy Otomatis via SQL & Snowflake Stage

Jika Anda lebih menyukai perintah SQL, jalankan skrip berikut di **Snowflake Worksheets**:

```sql
-- 1. Buat Database dan Schema
CREATE DATABASE IF NOT EXISTS SECURELOGIC_DB;
CREATE SCHEMA IF NOT EXISTS SECURELOGIC_DB.EVAL_SCHEMA;
USE SCHEMA SECURELOGIC_DB.EVAL_SCHEMA;

-- 2. Buat Internal Stage untuk Menyimpan Berkas Streamlit
CREATE STAGE IF NOT EXISTS STREAMLIT_STAGE;

-- 3. Unggah Berkas (Jalankan dari SnowSQL CLI atau Upload di Web UI Stage):
-- PUT file://./snowflake/streamlit_in_snowflake.py @STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
-- PUT file://./snowflake/environment.yml @STREAMLIT_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;

-- 4. Buat Aplikasi Streamlit Resmi di Snowflake
CREATE OR REPLACE STREAMLIT SECURELOGIC_EVAL_APP
ROOT_LOCATION = '@SECURELOGIC_DB.EVAL_SCHEMA.STREAMLIT_STAGE'
MAIN_FILE = '/streamlit_in_snowflake.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'
COMMENT = 'SecureLogic Eval - AI Safety & Empirical Reasoning Benchmark Dashboard';
```

---

## Keuntungan Menjalankan Streamlit di Snowflake:
1. **Inferensi AI Super Cepat via Snowflake Cortex:**
   - Aplikasi memanggil fungsi `SNOWFLAKE.CORTEX.COMPLETE(...)` secara instan untuk model besar (Llama-3.1-70B, Mistral, Arctic) tanpa lag atau beban CPU lokal.
2. **Koneksi Data Otomatis (*Zero Credentials Leak*):**
   - Aplikasi otomatis menggunakan `get_active_session()` bawaan Snowflake tanpa perlu menulis kata sandi atau API Key.
3. **Dapat Dibagikan ke Tim / Perekrut (*Shareable Enterprise Link*):**
   - Anda dapat membagikan URL aplikasi Streamlit Snowflake langsung kepada rekan kerja atau perekrut (*Recruiter*).
