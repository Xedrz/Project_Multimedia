# Project_Multimedia

# Tiru Gerakan Game 🎮🖐️

Sebuah game interaktif berbasis gesture tangan menggunakan **Ursina Engine** dan **OpenCV**, di mana pemain diminta untuk menirukan gesture yang ditampilkan oleh musuh dalam waktu terbatas.

## 📘 Logbook Proyek

### 🗓️ Minggu 1 – Menentukan Ide
- Menetapkan konsep game berbasis deteksi gesture tangan.
- Merancang alur dasar dan mekanik permainan.

### 🗓️ Minggu 2 – Mencari Asset Jalan
- Mencari dan mengumpulkan aset visual untuk karakter musuh dan latar belakang game.
- Menyusun visualisasi gerakan dalam konteks game.

### 🗓️ Minggu 3 – Mencari Asset Emoji
- Menentukan representasi visual untuk gesture berupa emoji/ikon.
- Menyesuaikan emoji dengan gesture yang dikenali oleh sistem.

### 🗓️ Minggu 4 – Implementasi dan Pengujian
- Mengimplementasikan kode deteksi gesture dan logika game.
- Mengintegrasikan aset ke dalam sistem.
- Melakukan uji coba game dan memperbaiki bug minor.
- Menyusun dokumentasi proyek.

## 🎯 Fitur

- Deteksi gesture tangan secara real-time melalui webcam menggunakan Mediapipe
- Game 3D sederhana dengan tampilan musuh dan player
- Gesture buffer untuk stabilitas deteksi
- Sistem kemenangan dan kekalahan otomatis
- Reset game dengan tombol `R`, keluar dengan tombol `Q`

## 🧠 Gesture yang Didukung

- ✌️ Peace (`peace`)
- 🖐️ Stop (`stop`)
- ☝️ Satu Jari (`one_finger_up`)
- ✊ Fist (`fist`)
- 👍 Thumbs Up (`thumbs_up`)

## 🛠️ Teknologi yang Digunakan

- [Ursina Engine](https://www.ursinaengine.org/) – untuk antarmuka dan interaksi game 3D
- [OpenCV](https://opencv.org/) – untuk menangkap video dari webcam
- [Mediapipe](https://google.github.io/mediapipe/) – untuk pendeteksian tangan dan landmark jari
- Python 3.x

## 🗂️ Struktur Proyek

```
gesture-mimic-game/
│
├── main.py # Game utama menggunakan Ursina dan deteksi gesture
├── hand_detection.py # Modul deteksi gesture tangan
├── game_controls.py # Modul animasi gesture tangan
├── assets/ # Folder untuk asset emoji 2D
│ ├── one.png
│ ├── two.png
│ ├── thumb.png
│ ├── fist.png
│ └── stop.png
├── source/ # Folder untuk asset jalan 3D 
│ └── g.glb # gambar jalan 3d
└── README.md # Dokumentasi proyek
```

## 🚀 Cara Menjalankan

1. **Clone repository ini**

```bash
git clone https://github.com/Xedrz/Project_Multimedia.git
cd Project_Multimedia
```

2. **Install dependencies**

install python 3.10 
```bash
pip install -r requirements.txt
```
atau jika secara manual:
```bash
pip install ursina opencv-python mediapipe
```

3. **Jalankan Game**

```bash
python main.py
```

## 🎮 Controls

Tombol                Fungsi

R                 Reset Permainan
Q                 Keluar dari Game  

## 📸 Screenshot
![image](https://github.com/user-attachments/assets/3ab07904-c333-43fc-8182-9f57a07e73f8)

## 💡 Catatan
- Pastikan kamera webcam aktif dan berfungsi.
- Lingkungan yang terang akan meningkatkan akurasi pendeteksian gesture tangan.
