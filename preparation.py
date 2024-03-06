import pandas as pd


class Preparation_dataset1:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        data1 = pd.read_excel(self.file_path, sheet_name=0)
        data2 = pd.read_excel(self.file_path, sheet_name=1)
        data3 = pd.read_excel(self.file_path, sheet_name=2)

        return data1, data2, data3

    def preparation_dataset1(self):
        data1, data2, data3 = self.load_data()

        # Rename Header
        data1 = data1.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': 'Jumlah Kecelakaan',
                             'Unnamed: 3': 'MD', 'Unnamed: 4': 'LB', 'Unnamed: 5': 'LR', 'Unnamed: 6': 'Kerugian Material', 'L412 A': 'Ket'})
        data2 = data2.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': 'Jumlah Kecelakaan', 'Unnamed: 3': 'Sepeda Motor',
                             'Unnamed: 4': 'Ran Penumpang', 'Unnamed: 5': 'Ran Barang', 'Unnamed: 6': 'Bus', 'Unnamed: 7': 'Ran Khusus', 'L412 P': 'Ket', 'Unnamed: 9': 'Kol 1', 'Unnamed: 10': 'Kol 2'})
        data3 = data3.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': '0 - 9', 'Unnamed: 3': '10 - 15',
                             'Unnamed: 4': '16 - 30', 'Unnamed: 5': '31 - 40', 'Unnamed: 6': '41 - 50', 'Unnamed: 7': '51 KEATAS', 'L412 H': 'Ket', 'Unnamed: 9': 'Kol 1', 'Unnamed: 10': 'Kol 2'})

        def ambil_data_setelah_NO(indeks_NO, data_sumber, jumlah_baris=10):
            data_terambil = []
            if indeks_NO < len(data_sumber) - 1:
                for i in range(2, 2 + jumlah_baris):
                    if indeks_NO + i < len(data_sumber):
                        baris_selanjutnya = data_sumber.iloc[indeks_NO + i]
                        data_terambil.append(baris_selanjutnya)
            return pd.DataFrame(data_terambil)

        def proses_dan_cetak_data(dataframe, nama_data):
            baris_terfilter = dataframe[dataframe['No'] == 'NO']
            data_tahunan = {}

            for idx, indeks_NO in enumerate(baris_terfilter.index):
                tahun = f"Laka_{2018 + idx}"
                data_tahunan[tahun] = ambil_data_setelah_NO(
                    indeks_NO, dataframe)

            return data_tahunan

        # Memanggil fungsi untuk setiap DataFrame
        data_laka = proses_dan_cetak_data(data1, "Data Kecelakaan")
        data_kendaraan = proses_dan_cetak_data(data2, "Data Kendaraan")
        data_korban = proses_dan_cetak_data(data3, "Data Korban")

        def bersihkan_data(data_tahunan, kolom_untuk_dihapus):
            data_bersih = {}
            for tahun, data in data_tahunan.items():
                data_cleaned = data.dropna(how='all').drop(
                    kolom_untuk_dihapus, axis=1)
                data_bersih[tahun] = data_cleaned
            return data_bersih

        def proses_dan_cetak_data(data_tahunan, kolom_untuk_dijumlahkan, label_data):
            for tahun, df in data_tahunan.items():
                if all(col in df.columns for col in kolom_untuk_dijumlahkan):
                    df['Jumlah ' + label_data] = df.loc[:,
                                                        kolom_untuk_dijumlahkan].sum(axis=1)
            return data_tahunan  # Add this line to return the processed data

        # Kolom untuk data korban
        kolom_korban = ['0 - 9', '10 - 15', '16 - 30',
                        '31 - 40', '41 - 50', '51 KEATAS']

        # Kolom untuk data kendaraan
        kolom_kendaraan = ['Sepeda Motor', 'Ran Penumpang',
                           'Ran Barang', 'Bus', 'Ran Khusus']

        # Misalkan Anda sudah memiliki data_laka, data_kendaraan, dan data_korban yang berisi data mentah
        # Bersihkan data tersebut terlebih dahulu
        data_laka_bersih = bersihkan_data(data_laka, ['MD', 'LB', 'LR', 'Ket'])
        data_kendaraan_bersih = bersihkan_data(
            data_kendaraan, ['Jumlah Kecelakaan', 'Ket'])
        data_korban_bersih = bersihkan_data(data_korban, ['Ket'])

        # Proses dan cetak data korban dan kendaraan
        proses_dan_cetak_data(data_korban_bersih, kolom_korban, "Korban")
        proses_dan_cetak_data(data_kendaraan_bersih,
                              kolom_kendaraan, "Kendaraan")

        for tahun in data_laka_bersih.keys():
            # Gabungkan 'Jumlah Kendaraan' dari data_kendaraan_bersih jika ada
            if tahun in data_kendaraan_bersih and 'Jumlah Kendaraan' in data_kendaraan_bersih[tahun].columns:
                df_kendaraan = data_kendaraan_bersih[tahun][[
                    'Jumlah Kendaraan']].reset_index(drop=True)
                data_laka_bersih[tahun] = pd.concat(
                    [data_laka_bersih[tahun].reset_index(drop=True), df_kendaraan], axis=1)

            # Gabungkan 'Jumlah Korban' dari data_korban_bersih jika ada
            if tahun in data_korban_bersih and 'Jumlah Korban' in data_korban_bersih[tahun].columns:
                df_korban = data_korban_bersih[tahun][[
                    'Jumlah Korban']].reset_index(drop=True)
                data_laka_bersih[tahun] = pd.concat(
                    [data_laka_bersih[tahun].reset_index(drop=True), df_korban], axis=1)

        # Gabungkan semua DataFrame untuk tahun-tahun tertentu
        data_laka_gabungan = pd.concat(
            data_laka_bersih.values(), ignore_index=True)

        # Gunakan fungsi groupby untuk mengelompokkan berdasarkan kolom 'Kesatuan'
        grouped_data = data_laka_gabungan.groupby('Kesatuan')

        # Hitung jumlah dari setiap grup menggunakan fungsi sum hanya untuk kolom yang diinginkan
        aggregated_data = grouped_data[[
            'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']].sum().reset_index()

        # Tambahkan kolom 'No' tanpa menghitung jumlahnya
        aggregated_data['No'] = grouped_data['No'].first().values

        # Urutkan DataFrame berdasarkan kolom 'No'
        aggregated_data_sorted = aggregated_data.sort_values(by='No')

        # Hapus indeks dan simpan 'No' pada posisi pertama
        aggregated_data_sorted = aggregated_data_sorted.set_index('No')

        # Cetak hasil aggregated_data_sorted tanpa menampilkan indeks
        self.data = aggregated_data_sorted

    def get_data(self):
        return self.data


class Preparation_dataset2:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_excel(self.file_path)
        return self.data

    def aggregate_data2(self):
        # Pastikan 'No' adalah kolom di DataFrame sebelum operasi value_counts
        self.data = self.data.reset_index()

        # Tambahkan kolom 'No' untuk penomoran data
        self.data['No'] = range(1, len(self.data) + 1)

        # Simpan 'No' sebelum operasi value_counts
        no_column = self.data['No']

        # Ubah nama kolom setelah operasi value_counts
        self.data = self.data['Street'].value_counts().reset_index()
        self.data.columns = ['Street', 'Sum of Accident']

        # Gabungkan kembali dengan 'No' menggunakan merge
        self.data = pd.merge(self.data, pd.DataFrame(
            {'No': no_column, 'Street': self.data['Street']}), on='Street')

        # Set ulang indeks dengan 'No' sebagai indeks
        self.data = self.data.set_index('No')

    def get_data(self):
        return self.data
