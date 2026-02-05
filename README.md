# 🏫 AI Customer Service Sekolah (CrewAI + Groq)

Project ini adalah sistem Customer Service cerdas berbasis AI yang dibuat menggunakan **CrewAI**, **LangChain**, dan **Streamlit**. AI ini bertugas menjawab pertanyaan seputar sekolah (Jurusan, Fasilitas, Alumni) menggunakan 3 Agent otonom.

Menggunakan **Groq API** (Llama-3) sebagai otak AI agar respon sangat cepat dan **GRATIS**.

---

## 📋 Prasyarat (System Requirements)

Sebelum menjalankan aplikasi, pastikan komputer Anda memenuhi kriteria berikut:

### 1. Python Version (Sangat Penting!)
* **Wajib:** Python **3.10** atau **3.11** (Direkomendasikan: **3.11.x**)
* **Dilarang:** Python 3.14 (Belum support library AI) atau Python 3.13.

### 2. API Key
* Anda memerlukan **Groq API Key** (Gratis).
* Dapatkan di: [https://console.groq.com/keys](https://console.groq.com/keys)

---

## 🛠️ Instalasi

Ikuti langkah-langkah berikut di terminal (PowerShell/CMD):

### 1. Pastikan Python Benar
Cek versi python Anda:
```bash
python --version
# Output harus Python 3.11.x
```
### 2. Install Library
Install paket-paket berikut dengan versi yang spesifik untuk menghindari konflik (Dependency Hell):

```Bash
pip install crewai==0.28.8 langchain-groq streamlit
```
### ⚠️ PENTING: 
Jika Anda mengalami error ImportError: cannot import name 'BaseTool', jalankan perintah ini untuk menghapus paket konflik:

```Bash
pip uninstall -y crewai-tools
```
### 🚀 Cara Menjalankan Aplikasi
1. Buka folder project di terminal.

2. Jalankan perintah berikut:

```Bash
streamlit run app.py
```
3. Browser akan otomatis terbuka.

4. Masukkan Groq API Key di sidebar sebelah kiri.

5. Mulai bertanya tentang sekolah!

### 📂 Struktur Project
app.py: Kode utama aplikasi (Streamlit UI & Logika Agent).

README.md: Dokumentasi instalasi.
🔧 Konfigurasi Model
Jika terjadi error Model decommissioned, buka file app.py dan ganti nama model pada bagian ChatGroq:

```bash
Python
llm = ChatGroq(
    ...
    model_name="llama-3.3-70b-versatile" # Gunakan versi terbaru ini
)
```
