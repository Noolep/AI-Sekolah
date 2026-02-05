import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CS Sekolah AI", page_icon="🏫")

# --- DATABASE SEKOLAH (SIMULASI) ---
# Ini adalah "otak" pengetahuan sekolah. Sensei bisa ubah isinya sesuai sekolah asli.
DATA_SEKOLAH = """
NAMA SEKOLAH: SMKN 2 Indramayu
1. JURUSAN (AKADEMIK):
   - RPL (Rekayasa Perangkat Lunak): Belajar Python, Web, Mobile App. KKM 75.
   - TKJ (Teknik Komputer Jaringan): Belajar Mikrotik, Cisco, Server.
   - NKPI (Nautika Kapal Penangkapan Ikan): Belajar Jadi Nelayan.
   - JB (Jasa Boga): Belajar Memasak, Kue, Manajemen Restoran.
   - TAB (Teknik Alat Berat): Belajar Excavator, Bulldozer, Crane.
   - APHPI (Agribisnis Perikanan dan Pengolahan Hasil Perikanan): Belajar Budidaya Ikan, Pengolahan Hasil Laut.
   - APAPL (Agribisnis Pengolahan Air Payau dan Laut): Belajar Pengolahan Air Payau dan Laut.
2. FASILITAS (SARPRAS):
   - Lab Komputer: Ada Terdapat 10 Lab, Spesifikasi Intel i5, RAM 8GB, SSD 512GB.
   - Kantin: Terdapat 6 Kantin Dengan Varian jualan yang Berbeda (mungkin), pembayaran pakai QRIS.
   - Masjid: Kapasitas 500 orang, AC.
   - Free WiFi: Kecepatan lelet seluruh area sekolah.
3. LULUSAN & KARIR (HUMAS):
   - Penyerapan Kerja: 90% lulusan langsung kerja sebelum wisuda.
   - Mitra Industri: Bekerjasama dengan Google, Microsoft, dan Telkom.
   - Alumni Terkenal: Saparudin, bekerja sebagai Senior Dev di Gojek.
"""

# --- SIDEBAR: SETTING API ---
with st.sidebar:
    st.header("⚙️ Pengaturan")
    st.info("Dapatkan API Key Gratis di: https://console.groq.com/keys")
    groq_api_key = st.text_input("Masukkan Groq API Key", type="password")

st.title("🏫 AI Customer Service Sekolah")
st.write("Tanyakan apa saja tentang Jurusan, Fasilitas, atau Lulusan!")

# --- INPUT USER ---
user_question = st.text_input("Pertanyaan Anda:", placeholder="Contoh: Apa saja yang dipelajari di jurusan RPL?")

# --- LOGIKA UTAMA ---
if st.button("Tanya AI") and user_question:
    if not groq_api_key:
        st.error("⚠️ Mohon masukkan Groq API Key di sidebar sebelah kiri!")
    else:
        # Set Environment Variable
        os.environ["GROQ_API_KEY"] = groq_api_key
        
        # Inisialisasi Model LLM (Pakai Groq Llama3 biar Gratis & Cepat)
        llm = ChatGroq(
            temperature=0, 
            groq_api_key=groq_api_key, 
            model_name="llama-3.3-70b-versatile"
        )

        # 1. AGENT AKADEMIK
        agent_akademik = Agent(
            role='Spesialis Akademik & Kurikulum',
            goal='Menjelaskan detail jurusan, pelajaran, dan syarat kenaikan kelas.',
            backstory="Kamu adalah Guru senior yang hafal semua kurikulum sekolah. "
                      "Kamu menjawab pertanyaan seputar Jurusan (RPL/TKJ/DKV) dan kegiatan belajar mengajar.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # 2. AGENT SARPRAS (FASILITAS)
        agent_fasilitas = Agent(
            role='Staff Sarana Prasarana',
            goal='Memberikan informasi tentang gedung, lab, kantin, dan infrastruktur sekolah.',
            backstory="Kamu adalah pengelola fasilitas sekolah. Kamu tahu spek komputer di lab, "
                      "menu kantin, hingga ketersediaan WiFi.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # 3. AGENT HUMAS (ALUMNI)
        agent_humas = Agent(
            role='Humas & Bursa Kerja',
            goal='Menjelaskan prospek karir, cerita sukses alumni, dan kemitraan industri.',
            backstory="Kamu mengurus hubungan industri. Kamu bangga dengan pencapaian alumni "
                      "dan tahu perusahaan mana saja yang bekerjasama dengan sekolah.",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        # --- TASK ---
        # Kita buat satu Task komprehensif agar CrewAI memilih agent mana yang paling cocok
        # atau menggabungkan jawaban mereka.
        main_task = Task(
            description=f"""
            Jawab pertanyaan user ini: '{user_question}'
            
            Gunakan informasi berikut sebagai referensi fakta (JANGAN MENGARANG BEBAS):
            {DATA_SEKOLAH}
            
            Jika pertanyaan tentang jurusan, biarkan Spesialis Akademik menjawab.
            Jika tentang gedung/alat, biarkan Staff Sarana menjawab.
            Jika tentang kerja/alumni, biarkan Humas menjawab.
            
            Jawab dengan ramah, sopan, dan menggunakan Bahasa Indonesia yang baik selayaknya Customer Service sekolah.
            """,
            expected_output="Jawaban lengkap dan ramah untuk calon siswa/orang tua.",
            agent=agent_akademik # Agent default (lead), dia bisa tanya ke yang lain jika perlu
        )

        # --- CREW ---
        school_crew = Crew(
            agents=[agent_akademik, agent_fasilitas, agent_humas],
            tasks=[main_task],
            verbose=2,
            process=Process.sequential # Proses berurutan/kolaborasi
        )

        with st.spinner('Sedang mendiskusikan pertanyaan Anda...'):
            result = school_crew.kickoff()
            
        st.success("Selesai!")
        st.markdown("### 🤖 Jawaban CS Sekolah:")
        st.write(result)