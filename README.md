# 📸 Foto Kita Blur

Aplikasi real-time camera blur yang mendeteksi gesture peace sign menggunakan AI (MediaPipe Hand Landmarker).

---

## ✨ Kegunaan

**Foto Kita Blur** adalah aplikasi yang berguna untuk:

- 🎬 **Membuat konten media sosial** - Blur otomatis untuk efek visual yang menarik
- 🎥 **Fotografi/Videografi** - Trigger blur dengan gesture peace sign
- 🎮 **Fun Filter** - Hiburan interaktif dengan kontrol gestur tangan
- 📸 **Content Creation** - Membuat video pendek dengan efek blur yang cool
- 🎭 **Privacy Protection** - Blur area sensitif dalam live streaming

---

## 📋 Fitur

- ✅ **Deteksi Gesture Peace Sign** - Mengenali gesture peace (index & middle jari naik)
- ✅ **Blur Real-time** - Blur frame kamera secara instan saat gesture terdeteksi
- ✅ **Sound Effect** - Audio feedback saat blur aktif
- ✅ **Visualisasi Tangan** - Tampilkan kerangka tangan dengan 21 landmark point
- ✅ **Teks "Foto Kita Blur"** - Muncul saat blur aktif
- ✅ **Webcam Mirror** - Tampilan selfie yang natural
- ✅ **Low CPU Usage** - Optimasi untuk performa maksimal

---

## 🚀 Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/MFikriZaelani/foto-kita-blur.git
cd foto-kita-blur
```

### 2. Buat Virtual Environment (Opsional tapi Direkomendasikan)

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Pastikan Model MediaPipe Ada

Pastikan file berada di lokasi yang benar:

```
foto-kita-blur/
├── models/
│   └── hand_landmarker.task  ← File harus ada di sini
├── assets/
│   └── sound-foto-kita-blur.mp3  ← Sound file (opsional)
└── blur.py
```

---

## 📦 Requirements

**File: `requirements.txt`**

```
opencv-python==4.8.1.78
mediapipe==0.10.3
numpy==1.24.3
```

**Sistem:**

- Python 3.8 atau lebih tinggi
- Webcam/Kamera laptop
- FFplay (untuk audio - opsional)

---

## 🎮 Cara Menggunakan

### 1. Jalankan Aplikasi

```bash
python blur.py
```

### 2. Kontrol Gesture

| Gesture                                      | Efek                        |
| -------------------------------------------- | --------------------------- |
| 🤘 **Peace Sign** (index & middle jari naik) | Trigger blur + sound + teks |
| ✋ **Hand Normal**                           | Blur hilang, kamera normal  |

### 3. Keyboard Controls

| Tombol  | Fungsi               |
| ------- | -------------------- |
| **ESC** | Keluar dari aplikasi |
| **Q**   | Keluar dari aplikasi |

### 4. Visualisasi

- 🔴 **Titik Merah** = Landmark point (sendi jari)
- 🟢 **Garis Hijau** = Koneksi antar landmark
- 💛 **Teks Kuning** = "foto kita blur" (saat gesture terdeteksi)

---

## 🎯 Contoh Penggunaan

### Skenario 1: Live Streaming

```
1. Buka aplikasi blur.py
2. Tampilkan tangan ke kamera
3. Buat gesture peace sign untuk blur area tertentu
4. Rekam screen atau share kamera
```

### Skenario 2: Content Creation

```
1. Jalankan aplikasi
2. Posisikan tangan sesuai kebutuhan
3. Trigger blur dengan peace sign
4. Rekam video dengan blur effect
5. Edit dan publish ke media sosial
```

### Skenario 3: Testing/Development

```
1. Jalankan blur.py
2. Lihat landmark visualization untuk debug
3. Perhatikan console output untuk gesture detection
```

---

## 🔧 Troubleshooting

### Error: "Could not open camera 0"

- **Solusi**: Pastikan webcam terhubung dan tidak digunakan aplikasi lain
- Coba ganti port: `cv2.VideoCapture(1)` atau `cv2.VideoCapture(2)`

### Error: "Missing MediaPipe model"

- **Solusi**: Download `hand_landmarker.task` dari:
  https://developers.google.com/mediapipe/solutions/vision/hand_landmarker
- Tempatkan di folder `models/`

### Sound tidak terdengar

- **Solusi**: Install FFplay atau ganti sound file di folder `assets/`
- Command untuk install FFplay: `choco install ffmpeg` (Windows)

### Gesture tidak terdeteksi

- **Solusi**: Pastikan pencahayaan cukup
- Tangan harus jelas terlihat di layar
- Buat gesture peace sign dengan jelas (index & middle jari naik)

---

## 📁 Struktur Folder

```
foto-kita-blur/
├── blur.py                          # Main application
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── LICENSE                          # License
├── models/
│   └── hand_landmarker.task        # MediaPipe model
├── assets/
│   └── sound-foto-kita-blur.mp3    # Sound effect
├── scripts/
│   ├── run.sh                      # Run script (Linux/Mac)
│   └── run.bat                     # Run script (Windows)
└── tests/
    ├── test_cam.py                 # Camera test
    └── test_sound.py               # Sound test
```

---

## 🎨 Customization

### Ubah Warna Teks

Di file `blur.py`, cari bagian:

```python
color = (0, 255, 255)  # BGR format (Yellow)
```

Ganti dengan:

- `(255, 0, 0)` = Biru
- `(0, 255, 0)` = Hijau
- `(0, 0, 255)` = Merah

### Ubah Ukuran Blur

```python
frame = cv2.GaussianBlur(frame, (61, 61), 0)
# Ubah (61, 61) ke nilai yang lebih besar untuk blur lebih kuat
# Harus angka ganjil
```

### Ubah Sensitivity Gesture

```python
min_hand_detection_confidence=0.1,  # 0.0-1.0 (lebih rendah = lebih sensitif)
min_hand_presence_confidence=0.1,
min_tracking_confidence=0.1,
```

### Ubah Teks

```python
text = "foto kita blur"  # Ganti dengan teks yang diinginkan
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

---

## 📜 License

Project ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

## 👤 Author

**M. Fikri Zaelani**

- GitHub: [@MFikriZaelani](https://github.com/MFikriZaelani)

---

## 📞 Support

Jika ada pertanyaan atau issue:

- Buka [GitHub Issues](https://github.com/MFikriZaelani/foto-kita-blur/issues)
- Email: support@example.com

---

## 🙏 Terima Kasih

- **MediaPipe** - Hand detection framework
- **OpenCV** - Computer vision library
- **Community** - Support dan feedback

---

**Selamat menggunakan Foto Kita Blur! 📸✨**
