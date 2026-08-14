# Bansos AI Hunter 🚀

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Bansos AI Hunter** adalah perangkat lunak pemindai (*scraper*) dan penguji (*validator*) otomatis sumber terbuka (*open-source*) untuk menemukan **AI Proxy / Relay Station ("AI中转站")**, penyedia kuota API gratisan, serta kunci API publik (*OpenAI-Compatible Endpoints*) secara real-time.

Perangkat ini dirancang khusus untuk memindai jejaring pencarian web dan forum teknologi internasional/Mandarin menggunakan kueri kata kunci spesifik, mengekstrak URL penyedia layanan relay (*One-API*, *New-API*, *NextChat*), serta memverifikasi kelayakan konektivitas agen AI (*LLM Completion & Latency Testing*).

---

## 🌟 Fitur Utama

- 🔍 **Multi-Source Harvester**: Pemindaian otomatis menggunakan kata kunci spesifik bahasa Mandarin (`AI中转站`, `免费额度`, `免费API`, `注册送额度`, `模型中转`, `大模型API`, `AI接口`, `余额`) dan bahasa Inggris/Indonesia.
- ⚡ **Flagship AI Model Priority**: Mengutamakan pencarian dan validasi untuk model-model AI tingkat tertinggi (*flagship*), seperti **Claude 3.7 Sonnet, Claude 3.5 Sonnet, Claude Opus, GPT-4o, GPT-4.5, O1, O3-Mini, DeepSeek R1/V3, Gemini 2.0 Flash, Qwen Max, Fable**, dan model populer lainnya.
- 🤖 **Agent Workability Test**: Tidak hanya mengecek status HTTP 200, tetapi melakukan *lightweight completion request* ke `/v1/chat/completions` untuk memastikan agen AI dapat memproses pesan secara aktual.
- ⏱️ **Real-Time Latency & Quota Checker**: Mengukur kecepatan respon dalam milidetik (ms) dan mengekstrak sisa saldo/kuota gratis yang tersedia pada endpoint terkait.
- 🛡️ **Spam & Referral Filter**: Penyaringan otomatis terhadap tautan referral tanpa kuota dan domain yang terdaftar dalam *blacklist*.
- 📊 **Multi-Format Reporting**: Menyajikan tabel interaktif berwarna di terminal (`rich`), serta mengekspor hasil pemindaian ke format **JSON**, **CSV**, dan **Dashboard HTML Interaktif**.

---

## 🛠️ Instalasi

### Persyaratan Sistem
- Python 3.10 atau versi yang lebih baru
- `pip` (Python Package Installer)

### Langkah Instalasi

1. **Klon Repository**:
   ```bash
   git clone https://github.com/username/bansos-ai-hunter.git
   cd bansos-ai-hunter
   ```

2. **Pasang Dependensi**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Panduan Penggunaan

### 1. Memulai Pemindaian Otomatis (*Scan Mode*)
Jalankan pemindaian otomatis ke berbagai sumber web:
```bash
python3 main.py scan
```

#### Opsi PemindaianTambahan:
- **Pengaturan Format Output**:
  ```bash
  python3 main.py scan --format html
  ```
  *(Pilihan format: `table`, `html`, `json`, `csv`, `all`)*

- **Pengaturan Kata Kunci Kustom**:
  ```bash
  python3 main.py scan --keywords "Claude 3.5 Sonnet free relay,DeepSeek R1 free api"
  ```

- **Mengatur Concurrency & Timeout**:
  ```bash
  python3 main.py scan --concurrency 20 --timeout 5.0
  ```

### 2. Pengujian Endpoint Tunggal (*Direct Test Mode*)
Uji konektivitas dan kapabilitas agen AI pada satu Base URL secara langsung:
```bash
python3 main.py scan test --url "https://api.example-relay.com" --key "sk-xxxxxx"
```

---

## 📂 Struktur Proyek

```
bansos-ai-hunter/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── pyproject.toml
├── main.py                     # Entry point CLI
├── bansos_ai/
│   ├── __init__.py
│   ├── config.py               # Kata kunci, regex, & daftar model AI
│   ├── core/
│   │   ├── models.py           # Data model Pydantic
│   │   ├── scraper.py          # Harvester & pemroses URL
│   │   ├── validator.py        # Penguji konektivitas & agen AI
│   │   └── reporter.py         # Format tabel & generator Dashboard HTML
│   └── utils/
│       ├── logger.py           # Integrasi Rich Console Logger
│       └── net.py              # HTTP Client Asinkron
└── tests/
    ├── test_scraper.py         # Unit test pemroses URL & Key
    └── test_validator.py       # Unit test validator konektivitas
```

---

## 🖥️ Tampilan Dashboard HTML

Setelah pemindaian selesai dengan opsi `--format html` atau `all`, dokumen dashboard interaktif akan dibuat pada `output_reports/bansos_dashboard.html`. Anda dapat membedahnya melalui peramban web untuk menyalin (*copy*) Base URL dan API Key dalam satu klik.

---

## 🤝 Kontribusi

Kontribusi dari komunitas sangat diapresiasi. Apabila Anda ingin menambahkan fitur baru, memperbaiki bug, atau memperbarui daftar kata kunci:

1. *Fork* repository ini.
2. Buat *feature branch* baru (`git checkout -b feature/FiturBaru`).
3. Lakukan *commit* perubahan Anda (`git commit -m 'Menambahkan FiturBaru'`).
4. *Push* ke branch (`git push origin feature/FiturBaru`).
5. Buat *Pull Request* baru.

---

## 📜 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).

> **Penafian (*Disclaimer*)**: Perangkat lunak ini ditujukan hanya untuk keperluan edukasi, riset konektivitas jaringan, dan pengujian independen. Pengguna bertanggung jawab penuh atas penggunaan endpoint dan kunci API publik yang ditemukan.
