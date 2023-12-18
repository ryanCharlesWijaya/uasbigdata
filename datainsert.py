import requests
import mysql.connector
 
# Konfigurasi database
db_config = {
    'host': 'localhost',
    'user': 'ryan',
    'password': 'password',
    'database': 'uasbigdata'
}
 
# Alamat URL API
api_url = "https://data.jabarprov.go.id/api-backend/bigdata/dinkes/od_17598_jml_kesakitan_akibat_malaria__jk"
 
try:
    # Mengirim permintaan GET ke API
    response = requests.get(api_url)
 
    # Memeriksa status kode respons
    if response.status_code == 200:
        # Parse data JSON yang diterima
        user_data = response.json().get("data")
 
        # Membuka koneksi ke database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
 
        # Menambahkan data pengguna ke dalam tabel
        for user in user_data:
            cursor.execute('''
                INSERT INTO malaria (
                    id,
                    kode_provinsi,
                    nama_provinsi,
                    kode_kabupaten_kota,
                    nama_kabupaten_kota,
                    jenis_kelamin,
                    jumlah_kesakitan,
                    satuan,
                    tahun
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                ''',
                (
                    user['id'],
                    user['kode_provinsi'],
                    user['nama_provinsi'],
                    user['kode_kabupaten_kota'],
                    user['nama_kabupaten_kota'],
                    user['jenis_kelamin'],
                    user['jumlah_kesakitan'],
                    user['satuan'],
                    user['tahun']
                ))
 
        # Menyimpan perubahan dan menutup koneksi
        conn.commit()
        conn.close()
 
        print("Data pengguna telah disimpan ke database MySQL.")
    else:
        print(f"Gagal mengambil data. Kode status: {response.status_code}")
 
except requests.exceptions.RequestException as e:
    print(f"Terjadi kesalahan saat menghubungi API: {str(e)}")
 