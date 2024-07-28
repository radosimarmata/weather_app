# Weather App
Weather App adalah aplikasi untuk mencari dan menampilkan prakiraan cuaca di berbagai lokasi di Indonesia menggunakan data dari [BMKG](https://www.bmkg.go.id/). Aplikasi ini dapat mengambil data lokasi dan prakiraan cuaca dari situs web [BMKG](https://data.bmkg.go.id/prakiraan-cuaca/), serta menyimpannya dalam format JSON.

## Fitur
- Mengambil daftar lokasi cuaca dari situs BMKG.
- Menampilkan daftar lokasi untuk dipilih pengguna.
- Menampilkan prakiraan cuaca untuk lokasi yang dipilih.
- Menyimpan hasil prakiraan cuaca ke file JSON.

## Prasyarat
Pastikan Anda memiliki hal berikut sebelum menjalankan proyek ini:
- Python 3.x
- requests library: Install dengan perintah pip install requests
- beautifulsoup4 library: Install dengan perintah pip install beautifulsoup4

## Instalasi
1. Clone repositori ini ke mesin lokal Anda.
```
https://github.com/radosimarmata/weather_app.git
```
```
cd weather_app
```
2. Install dependensi yang diperlukan.
```
pip install -r requirements.txt
```

## Penggunaan
1. Jalankan skrip utama.
```
python main.py
```
2. Pilih salah satu opsi yang tersedia di menu:
- Pilih 1 untuk mengambil daftar lokasi dari situs BMKG.
- Pilih 2 untuk menampilkan daftar lokasi dan memilih lokasi untuk melihat prakiraan cuaca.
- Pilih 3 untuk keluar dari aplikasi.

3. Jika Anda memilih 2, Anda dapat memilih lokasi dari daftar yang tersedia dan memasukkan nama file untuk menyimpan hasil prakiraan cuaca. Jika tidak memasukkan nama file, nama lokasi akan digunakan sebagai nama file dengan format huruf kecil dan spasi diganti dengan garis bawah.

## Struktur Proyek
```
weather-app/
├── result/                # Folder untuk menyimpan hasil prakiraan cuaca
├── data_location.json     # File JSON yang berisi daftar lokasi
├── main.py                # Skrip utama aplikasi
├── requirements.txt       # File dependensi
└── README.md              # Dokumentasi proyek
```

## Sumber Data
Data prakiraan cuaca diambil dari situs [BMKG](https://data.bmkg.go.id/prakiraan-cuaca/).