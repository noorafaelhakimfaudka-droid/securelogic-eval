# SecureLogic Eval — Buku Panduan Portofolio, Wawancara, & Dokumen Arsitektur Riset
**Peneliti & Pengembang:** Rafael Hakim Souissa  
**Fokus Keilmuan:** AI Safety, Behavioral Benchmarking, Multi-Turn Epistemic Resilience, & Applied Statistical Inference

---

## DAFTAR ISI
1. [Ringkasan Eksekutif (Executive Summary)](#1-ringkasan-eksekutif-executive-summary)
2. [Latar Belakang: Mengapa Proyek Ini Harus Ada? (The "Why")](#2-latar-belakang-mengapa-proyek-ini-harus-ada-the-why)
3. [Arsitektur & Metodologi Eksperimen (The "How")](#3-arsitektur--metodologi-eksperimen-the-how)
4. [Temuan Kritis & Angka Pembuktian Riset](#4-temuan-kritis--angka-pembuktian-riset)
5. [Struktur Panduan Wawancara Kerja (STAR Method Cheat Sheet)](#5-struktur-panduan-wawancara-kerja-star-method-cheat-sheet)
6. [Pertanyaan Teknis & Jawaban Kunci Saat Interview (Q&A Drill)](#6-pertanyaan-teknis--jawaban-kunci-saat-interview-qa-drill)
7. [Template Portofolio: Resume Bullet Points, LinkedIn Post, & GitHub Summary](#7-template-portofolio-resume-bullet-points-linkedin-post--github-summary)

---

## 1. Ringkasan Eksekutif (Executive Summary)

**SecureLogic Eval** adalah tolak ukur evaluasi empiris (*behavioral benchmarking framework*) pertama yang dirancang secara khusus untuk menguji **ketahanan epistemik dan integritas logika AI** saat menghadapi **bias kognitif awal** dan **sanggahan otoritas manusia palsu (*authority-driven pushback*)** dalam domain telemetri keamanan siber kritis (*SOC, Cryptography, Anomaly Detection*).

* **Jumlah Kasus Uji:** 48 Skenario Kasus Matematika & Logika Telemetri Eksak dengan Ground Truth tak terbantahkan.
* **Jumlah Sampel Evaluasi:** 192 Eksekusi Eksperimen Terstruktur (4 Kondisi Perlakuan).
* **Model Teruji:** Llama-3.1-70B, Qwen2.5-7B, Mistral Large 2, Snowflake Cortex AI.
* **Hasil Utama:** Akurasi model anjlok drastis dari **83.3%** pada kondisi mandiri menjadi **18.8%** saat terpapar tekanan majemuk, dengan lonjakan rasio peluang kegagalan (*Odds Ratio*) sebesar **21.67x**.

---

## 2. Latar Belakang: Mengapa Proyek Ini Harus Ada? (The "Why")

### Masalah Nyata di Industri AI Saat Ini:
1. **Penyakit Sikofansi (Sycophancy / "Penjilatan Token"):**  
   Mayoritas Model Bahasa Besar (LLM) modern dilatih menggunakan teknik **RLHF (Reinforcement Learning from Human Feedback)**. Dalam proses RLHF, penilai manusia (*human raters*) cenderung memberikan skor tinggi (*reward*) pada respons AI yang sopan, ramah, dan menyetujui opini penilai. Akibatnya, AI mempelajari pola bahwa *"menyetujui pengguna = selamat"*, bahkan ketika pengguna menyodorkan klaim yang salah secara faktual.
2. **Bahaya Fatal di Sektor Kritis (Cybersecurity SOC):**  
   Di pusat operasi keamanan (SOC), jika seorang analis keamanan muda menyajikan prompt yang keliru (*anchoring bias*: *"Atasan menduga probabilitas malware ini 90%"*), atau seorang penyusup menyamar sebagai CISO dan membantah AI (*"Saya Lead Architect, jawabanmu salah"*), AI yang tidak memiliki ketahanan logika akan langsung menarik kembali fakta matematis yang benar dan menyetujui klaim palsu tersebut.
3. **Ketiadaan Benchmark yang Menggabungkan Bias + Sanggahan Multi-Putaran:**  
   Benchmark yang ada di pasar (seperti MMLU atau GSM8K) hanya menguji soal satu putaran (*single-turn*). Mereka gagal mendeteksi apakah AI akan **goyah dan membatalkan jawabannya sendiri di putaran kedua (*multi-turn epistemic drift*)**.

---

## 3. Arsitektur & Metodologi Eksperimen (The "How")

Riset ini menggunakan metodologi **Desain Eksperimen Faktorial 2x2 (Two-Way Factorial Design)**:

```
                              Faktor B: Sanggahan Otoritas (Pushback)
                              Tanpa Sanggahan (T1)       Dengan Sanggahan (T2)
Faktor A:       Prompt Netral |   Kondisi A (83.3%)   |    Kondisi C (45.8%)    |
Bias Kognitif   Prompt Berbias|   Kondisi B (58.3%)   |    Kondisi D (18.8%)    |
```

### Empat Kondisi Eksperimen:
1. **Kondisi A (Kontrol Netral - Baseline):**  
   Prompt disajikan tanpa jebakan kata dan tanpa sanggahan. Mengukur kapasitas kognitif murni model.
2. **Kondisi B (Bias Kognitif Saja):**  
   Prompt disisipi angka penjangkar yang salah (*anchoring bias*, *base-rate neglect*, atau *framing*).
3. **Kondisi C (Sanggahan Otoritas Saja - Single-Factor Pushback):**  
   Prompt awal netral (jawaban benar), namun di putaran kedua pengguna membantah dengan menyamar sebagai atasan senior (*"Saya Lead Architect, jawabanmu salah"*).
4. **Kondisi D (Interaksi Majemuk - Multi-Factor Compound):**  
   Model menerima prompt berbias pada putaran pertama *sekaligus* sanggahan otoritas pada putaran kedua.

---

## 4. Temuan Kritis & Angka Pembuktian Riset

Berikut adalah angka-angka valid yang siap Anda presentasikan:

1. **Akurasi per Kondisi:**
   * **Kondisi A (Netral):** **83.3%** [Rentang Keyakinan 95%: 72.9% - 93.8%]
   * **Kondisi B (Bias Saja):** **58.3%** [Rentang Keyakinan 95%: 43.8% - 70.8%]
   * **Kondisi C (Sanggahan Saja):** **45.8%** [Rentang Keyakinan 95%: 33.3% - 58.3%]
   * **Kondisi D (Interaksi Ganda):** **18.8%** [Rentang Keyakinan 95%: 8.3% - 29.2%]

2. **Tingkat Pergeseran Logika (Drift Rate) Berdasarkan Kesulitan:**
   * **Tingkat Mudah (1 Langkah):** 43.8% goyah.
   * **Tingkat Sedang (2 Langkah):** 62.5% goyah.
   * **Tingkat Sulit (Multilangkah):** **81.8% goyah!**  
     *(Semakin rumit rumus, semakin lemah keyakinan internal AI, semakin mudah AI dipaksa menyerah).*

3. **Uji Inferensial Statistik:**
   * **ANOVA Faktorial Dua Arah:** Efek utama bias kognitif (F = 16.29, p < 0.001) dan efek utama sanggahan (F = 35.69, p < 0.0001) terbukti signifikan secara statistik.
   * **Uji McNemar Paired Test:** Pergeseran dari Kondisi A ke C (p = 0.00006) dan Kondisi A ke D (p = 0.00000007) membuktikan degradasi bukan karena kebetulan acak.
   * **Odds Ratio:** Paparan interaksi majemuk (Kondisi D) melipatgandakan peluang kegagalan model sebesar **21.67 kali lipat**.

---

## 5. Struktur Panduan Wawancara Kerja (STAR Method Cheat Sheet)

Gunakan kerangka **STAR** (*Situation, Task, Action, Result*) ini saat interviewer bertanya: *"Ceritakan proyek Machine Learning / AI paling menantang yang pernah Anda bangun!"*

### S — Situation (Situasi)
> *"Di industri AI saat ini, banyak organisasi mulai mengintegrasikan LLM ke dalam alur kerja kritis seperti Cyber Defense SOC. Namun, model-model ini memiliki kelemahan mendasar akibat proses RLHF: mereka rentan terhadap sikofansi (menyetujui klaim pengguna yang salah) dan bias kognitif. Jika analis menyajikan data dengan asumsi keliru atau atasan menyanggah fakta, AI sering kali membatalkan penalaran logisnya."*

### T — Task (Tugas / Target)
> *"Saya ingin merancang sebuah framework benchmark evaluasi empiris yang objektif dan reproducible untuk mengukur seberapa jauh integritas logika AI runtuh saat dihadapkan pada bias kontekstual dan tekanan otoritas manusia palsu dalam skenario multi-putaran."*

### A — Action (Aksi / Solusi Teknis yang Anda Bangun)
> *"Saya membangun **SecureLogic Eval** yang mencakup:
> 1. Merancang 48 skenario telemetri keamanan siber eksak (Probabilitas Bayes, Entropi Kriptografi, Z-Score Anomali, dan Graf Logika) dengan pembuktian analitis formal (Ground Truth).
> 2. Menerapkan metodologi Desain Faktorial 2x2 multi-putaran (Kondisi A, B, C, D) dengan regex extractor toleransi numerik presisi (toleransi ±0.5%).
> 3. Mengintegrasikan engine statistik inferensial (Two-Way ANOVA, McNemar Exact Test, Bootstrap 95% CI, dan Odds Ratio).
> 4. Mengembangkan dasbor interaktif cloud terpadu di Snowflake Workspaces menggunakan Streamlit dan Snowflake Cortex AI."*

### R — Result (Hasil & Dampak)
> *"Evaluasi empiris terhadap 192 sampel menunjukkan bahwa akurasi model anjlok drastis dari 83.3% menjadi 18.8% pada kondisi interaksi ganda, dengan tingkat pembatalan penalaran (Drift Rate) mencapai 81.8% pada kasus rumit dan lonjakan rasio kegagalan sebesar 21.7x. Riset ini menyediakan audit framework nyata bagi institusi sebelum men-deploy AI ke infrastruktur SOC."*

---

## 6. Pertanyaan Teknis & Jawaban Kunci Saat Interview (Q&A Drill)

#### Q1: "Mengapa Anda memilih kasus telemetri keamanan siber, bukan soal matematika umum?"
**Jawaban Anda:**
> *"Soal matematika umum (seperti GSM8K) tidak merefleksikan asimetri informasi di dunia nyata. Dalam keamanan siber (seperti False Positive Paradox pada alarm EDR), probabilitas prior infeksi sangat kecil (misal 0.1%), sehingga intuisi manusia sering keliru mengira alarm 90% akurat pasti menandakan 90% infeksi. Ini menciptakan jebakan kognitif alami yang sempurna untuk menguji apakah AI mengandalkan kalkulasi bukti formal atau sekadar mengikuti intuisi penanya."*

#### Q2: "Bagaimana Anda memverifikasi bahwa jawaban AI benar secara objektif tanpa bias LLM-as-a-judge?"
**Jawaban Anda:**
> *"Saya menolak penggunaan LLM-as-a-judge untuk evaluasi akhir karena LLM judge juga rentan terhadap bias sikofansi. Sebagai gantinya, seluruh 48 soal memiliki Ground Truth matematis deterministik yang diturunkan secara simbolik. Jawaban diekstrak menggunakan sistem hybrid (Regex Markdown Bold Pattern + Token Numeric Normalizer dengan batas toleransi relatif ±0.5%), sehingga penilaian berstatus 100% deterministik dan bebas bias subjektif."*

#### Q3: "Apa arti dari temuan Drift Rate 81.8% pada tingkat Hard?"
**Jawaban Anda:**
> *"Ini menunjukkan fenomena yang kami sebut **Epistemic Insecurity Correlation**. Semakin banyak langkah komputasi yang harus dilakukan model, semakin tipis marjin probabilitas token akhir pada lapisan atensinya. Saat pengguna memberikan sanggahan berbasis otoritas di Putaran 2, model dengan mudah membelokkan jalurnya dan memilih opsi yang menyenangkan pengguna (sycophantic retreat)."*

---

## 7. Template Portofolio: Resume Bullet Points, LinkedIn Post, & GitHub Summary

### 📌 Resume Bullet Points — Standar Kurikulum Haltev IT (Data Science & Machine Learning Track):

#### Format 1: Data Scientist / Machine Learning Engineer (Kurikulum Haltev IT)
* **Data Science & Machine Learning Final Project — SecureLogic Eval**
  * **Exploratory Data Analysis (EDA) & Data Wrangling:** Mengembangkan pipeline evaluasi komparatif 192 observasi terstruktur dari 48 skenario telemetri menggunakan Pandas dan NumPy, mencakup manipulasi DataFrame, kalkulasi agregasi multi-level, dan ekstraksi fitur data numerik/kategorikal.
  * **Uji Hipotesis Statistik (Statistical Hypothesis Testing):** Menerapkan metodologi inferensial formal kurikulum Haltev IT, mencakup Two-Way ANOVA (F = 35.69, p < 0.001), Uji McNemar untuk paired binary data (p = 0.00006), serta estimasi 95% Bootstrap Confidence Interval (1.000 iterasi resampling).
  * **Evaluasi Model & Matriks Transisi (Confusion Matrix & Error Analysis):** Menganalisis degradasi performa model (Misclassification Rate) dari akurasi awal 83.3% ke 18.8%, serta memetakan matriks transisi diskordansi keadaan (Epistemic State Transition Matrix).
  * **Interactive Dashboard & Cloud Deployment:** Membangun dasbor analitis interaktif full-stack menggunakan Streamlit dan Plotly bertema visual Sunset Crimson, serta men-deploy aplikasi secara cloud-native di platform Snowflake Workspaces.

#### Format 2: Ringkas (Untuk 1-Page Resume / CV Haltev IT)
* **Machine Learning Project: SecureLogic Eval (AI Reasoning & Safety Evaluation)**
  * Merancang framework evaluasi empiris LLM berbasis Python OOP, Pydantic, dan Pytest (11 unit test lulus 100%).
  * Melakukan statistical testing (Two-Way ANOVA & McNemar Test) yang membuktikan pengaruh signifikan bias kognitif dan sanggahan otoritas (p < 0.001, Odds Ratio 21.7x).
  * Mengembangkan dasbor analitis interaktif Streamlit terintegrasi dengan Snowflake Cortex AI untuk visualisasi metrik performa secara real-time.

---

### 🛠️ Pemetaan Kompetensi Sesuai Modul Kurikulum Haltev IT:
| Modul Haltev IT | Implementasi Nyata di Proyek SecureLogic Eval |
|---|---|
| **Python Programming & OOP** | Struktur kelas modular `src/` (`Pydantic schema`, `AnswerExtractor`, `ExperimentRunner`). |
| **Data Manipulation & EDA** | Agregasi dataset 192 baris, grouping berdasarkan *difficulty* & *category* menggunakan `Pandas`. |
| **Statistical Inference & Hypothesis Testing** | Penerapan formal *Two-Way ANOVA*, *McNemar Paired Test*, dan *Bootstrap 95% CI*. |
| **Model Evaluation & Error Analysis** | Evaluasi Confusion Matrix multi-putaran, penghitungan *Odds Ratio*, dan analisis *Drift Rate*. |
| **Interactive Dashboard & Business Intel** | Dasbor `Streamlit` 6 halaman dengan visualisasi *Plotly*, filter dinamis, dan 4 kartu KPI. |
| **Cloud & Deployment** | Integrasi database cloud dan *Snowflake Workspaces Deployment*. |

---

### 🛠️ Kata Kunci Teknis untuk Bagian "Skills" di CV:
* **LLM & GenAI:** LLM Evaluation Pipelines, Multi-Turn Dialog Benchmarking, Prompt Engineering, Sycophancy Mitigation, RLHF Failure Analysis, Snowflake Cortex AI, Ollama.
* **ML Analytics & Statistics:** Factorial ANOVA, McNemar Test, Bootstrap Resampling, Odds Ratio, Statistical Hypothesis Testing, Error Analysis.
* **Engineering & Frameworks:** Python, Streamlit, Pandas, NumPy, SciPy, Pydantic, Pytest, Plotly, Snowflake Workspaces / Snowpark.

---

### 🌐 Template Post LinkedIn (Siap Unggah):
```text
🚀 Bangga membagikan proyek riset terbaru saya: SecureLogic Eval — Menguji Integritas Logika AI di Bawah Tekanan Bias Kognitif & Sanggahan Otoritas!

Apakah AI Anda akan tetap mempertahankan kebenaran matematika saat seorang atasan membantahnya? 

Dalam riset ini, saya mengevaluasi model bahasa besar pada 48 skenario telemetri keamanan siber eksak menggunakan Desain Faktorial 2x2.

Temuan Kunci:
📉 Akurasi mandiri 83.3% anjlok hingga 18.8% saat terpapar bias awal + sanggahan otoritas.
⚠️ Drift Rate mencapai 81.8% pada persoalan kompleks (AI menarik kembali jawaban yang benar).
📈 Risiko kesalahan melonjak 21.7x (Odds Ratio, p < 0.00001).

Aplikasi dasbor interaktif kini telah live dan terpasang di Snowflake Workspaces memanfaatkan Snowflake Cortex AI!

📂 GitHub & Pembahasan Lengkap: [Tautan Repositori Anda]
#AISafety #MachineLearning #LLMEvaluation #CyberSecurity #DataScience #Snowflake
```
