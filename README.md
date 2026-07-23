# 🌿 Herbalife Customer Segmentation Dashboard

Dashboard Streamlit untuk analisis segmentasi pelanggan Herbalife berdasarkan
**RFM Analysis (Recency, Frequency, Monetary)**, **K-Means Clustering**, dan
**Decision Tree**, sesuai dengan alur analisis pada `Data_herbalife.ipynb`.

## Isi Folder
- `app.py` — kode utama dashboard
- `dataset_herbalife2425_koreksi.csv` — dataset transaksi (default)
- `requirements.txt` — daftar library yang dibutuhkan

## Cara Menjalankan

1. Pastikan Python 3.9+ sudah terpasang.
2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan dashboard:
   ```bash
   streamlit run app.py
   ```
4. Browser akan otomatis terbuka di `http://localhost:8501`.

> Jika ingin memakai dataset lain, gunakan fitur **"Ganti dataset (opsional)"**
> di sidebar — cukup upload file CSV dengan kolom yang sama:
> `Customer_ID, Tanggal_Transaksi, Menu, Qty, Harga_Satuan, Total_Transaksi`.

## Fitur

| Fitur | Keterangan |
|---|---|
| 🏠 Dashboard Utama | Metric cards, pencarian pelanggan, filter cluster, grafik interaktif (scatter, pie, bar, radar), download hasil clustering |
| 🌳 Decision Tree | Akurasi model, gambar pohon keputusan, feature importance, confusion matrix, elbow method |
| 🎯 Strategi Pemasaran | Kartu strategi per segmen, perbandingan RFM antar segmen, download data + strategi |
| 📄 Data Mentah | Tabel data transaksi & data RFM lengkap |

## Alur Analisis (mengikuti notebook)
1. Load data & pembersihan (hapus duplikat, konversi tanggal)
2. Hitung nilai RFM per `Customer_ID`
3. Standardisasi fitur RFM
4. Tentukan K optimal (Elbow Method) → **K = 5**
5. Clustering dengan **K-Means** (`random_state=42`)
6. Latih **Decision Tree** (`max_depth=4`) untuk mempelajari aturan klasifikasi cluster
7. Susun **strategi pemasaran** berdasarkan karakteristik tiap cluster
