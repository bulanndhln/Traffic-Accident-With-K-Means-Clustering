import pandas as pd


class Preparation_dataset1:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    # load data from excel
    def load_data(self):
        data1 = pd.read_excel(self.file_path, sheet_name=0)
        data2 = pd.read_excel(self.file_path, sheet_name=1)
        data3 = pd.read_excel(self.file_path, sheet_name=4)



        return data1, data2, data3

    def preparation_data1(self):
        data1, data2, data3 = self.load_data()

        # Rename Header
        data1 = data1.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': 'Jumlah Kecelakaan',
                             'Unnamed: 3': 'MD', 'Unnamed: 4': 'LB', 'Unnamed: 5': 'LR', 'Unnamed: 6': 'Kerugian Material', 'L412 A': 'Ket'})
        data2 = data2.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': 'Jumlah Kecelakaan', 'Unnamed: 3': 'Sepeda Motor',
                             'Unnamed: 4': 'Ran Penumpang', 'Unnamed: 5': 'Ran Barang', 'Unnamed: 6': 'Bus', 'Unnamed: 7': 'Ran Khusus', 'L412 P': 'Ket', 'Unnamed: 9': 'Kol 1', 'Unnamed: 10': 'Kol 2'})
        data3 = data3.rename(columns={'KEPOLISIAN NEGARA REPUBLIK INDONESIA': 'No', 'Unnamed: 1': 'Kesatuan', 'Unnamed: 2': '0 - 9', 'Unnamed: 3': '10 - 15',
                             'Unnamed: 4': '16 - 30', 'Unnamed: 5': '31 - 40', 'Unnamed: 6': '41 - 50', 'Unnamed: 7': '51 KEATAS', 'L412 H': 'Ket', 'Unnamed: 9': 'Kol 1', 'Unnamed: 10': 'Kol 2'})

        # Proses selanjutnya untuk membersihkan dan menggabungkan data

        data1_cleaned = data1.dropna(how='all')
        data1_cleaned = data1_cleaned.drop(['MD', 'LB', 'LR', 'Ket'], axis=1)

        data2_cleaned = data2.dropna(how='all')
        data2_cleaned = data2_cleaned.drop(
            ['Jumlah Kecelakaan', 'Ket', 'Kol 1', 'Kol 2'], axis=1)

        data3_cleaned = data3.dropna(how='all')
        data3_cleaned = data3_cleaned.drop(['Ket', 'Kol 1', 'Kol 2'], axis=1)

        # Memilih kolom yang memiliki nilai dan mengelompokkan data berdasarkan 'Kesatuan'
        def aggregate_and_rename_laka(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Jumlah Kecelakaan'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Jumlah Kecelakaan_{year}']
            return aggregated

        def aggregate_and_rename_kermat(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Kerugian Material'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Kerugian Material_{year}']
            return aggregated

        def aggregate_and_rename_spd(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Sepeda Motor'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Sepeda Motor_{year}']
            return aggregated

        def aggregate_and_rename_ranPen(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Ran Penumpang'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Ran Penumpang_{year}']
            return aggregated

        def aggregate_and_rename_ranBar(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Ran Barang'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Ran Barang_{year}']
            return aggregated

        def aggregate_and_rename_bus(df, year):
            aggregated = df.groupby('Kesatuan')['Bus'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Bus_{year}']
            return aggregated

        def aggregate_and_rename_ranKhus(df, year):
            aggregated = df.groupby('Kesatuan')[
                'Ran Khusus'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'Ran Khusus_{year}']
            return aggregated

        def aggregate_and_rename_0_9(df, year):
            aggregated = df.groupby('Kesatuan')['0 - 9'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'0 - 9_{year}']
            return aggregated

        def aggregate_and_rename_10_15(df, year):
            aggregated = df.groupby('Kesatuan')['10 - 15'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'10 - 15_{year}']
            return aggregated

        def aggregate_and_rename_16_30(df, year):
            aggregated = df.groupby('Kesatuan')['16 - 30'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'16 - 30_{year}']
            return aggregated

        def aggregate_and_rename_31_40(df, year):
            aggregated = df.groupby('Kesatuan')['31 - 40'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'31 - 40_{year}']
            return aggregated

        def aggregate_and_rename_41_50(df, year):
            aggregated = df.groupby('Kesatuan')['41 - 50'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'41 - 50_{year}']
            return aggregated

        def aggregate_and_rename_50up(df, year):
            aggregated = df.groupby('Kesatuan')[
                '51 KEATAS'].sum().reset_index()
            aggregated.columns = ['Kesatuan', f'51 KEATAS_{year}']
            return aggregated
        # ----------------------------------------------------------
        # Menghitung total kecelakaan per kesatuan untuk setiap rentang baris dan tahun
        total_df1_laka = aggregate_and_rename_laka(
            data1_cleaned.iloc[6:16], 2018)
        total_df2_laka = aggregate_and_rename_laka(
            data1_cleaned.iloc[24:34], 2019)
        total_df3_laka = aggregate_and_rename_laka(
            data1_cleaned.iloc[42:52], 2020)
        total_df4_laka = aggregate_and_rename_laka(
            data1_cleaned.iloc[60:70], 2021)
        total_df5_laka = aggregate_and_rename_laka(
            data1_cleaned.iloc[78:88], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_laka = total_df1_laka
        for df in [total_df2_laka, total_df3_laka, total_df4_laka, total_df5_laka]:
            total_merged_laka = pd.merge(
                total_merged_laka, df, on='Kesatuan', how='outer')

        # Menghitung total kerugian material per kesatuan untuk setiap rentang baris dan tahun
        total_df1_kermat = aggregate_and_rename_kermat(
            data1_cleaned.iloc[6:16], 2018)
        total_df2_kermat = aggregate_and_rename_kermat(
            data1_cleaned.iloc[24:34], 2019)
        total_df3_kermat = aggregate_and_rename_kermat(
            data1_cleaned.iloc[42:52], 2020)
        total_df4_kermat = aggregate_and_rename_kermat(
            data1_cleaned.iloc[60:70], 2021)
        total_df5_kermat = aggregate_and_rename_kermat(
            data1_cleaned.iloc[78:88], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_kermat = total_df1_kermat
        for df in [total_df2_kermat, total_df3_kermat, total_df4_kermat, total_df5_kermat]:
            total_merged_kermat = pd.merge(
                total_merged_kermat, df, on='Kesatuan', how='outer')

        # Menggabungkan data 'Jumlah Kecelakaan' dan 'Kerugian Material' untuk setiap tahun
        total_merged = pd.merge(
            total_merged_laka, total_merged_kermat, on='Kesatuan', how='outer')
        total_merged = pd.DataFrame(total_merged)

        # Menghitung total sepeda motor per kesatuan untuk setiap rentang baris dan tahun
        total_df1_spd = aggregate_and_rename_spd(
            data2_cleaned.iloc[6:16], 2018)
        total_df2_spd = aggregate_and_rename_spd(
            data2_cleaned.iloc[25:35], 2019)
        total_df3_spd = aggregate_and_rename_spd(
            data2_cleaned.iloc[44:54], 2020)
        total_df4_spd = aggregate_and_rename_spd(
            data2_cleaned.iloc[63:73], 2021)
        total_df5_spd = aggregate_and_rename_spd(
            data2_cleaned.iloc[82:92], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_spd = total_df1_spd
        for df in [total_df2_spd, total_df3_spd, total_df4_spd, total_df5_spd]:
            total_merged_spd = pd.merge(
                total_merged_spd, df, on='Kesatuan', how='outer')

        # Menghitung total ran penumpang per kesatuan untuk setiap rentang baris dan tahun
        total_df1_ranPen = aggregate_and_rename_ranPen(
            data2_cleaned.iloc[6:16], 2018)
        total_df2_ranPen = aggregate_and_rename_ranPen(
            data2_cleaned.iloc[25:35], 2019)
        total_df3_ranPen = aggregate_and_rename_ranPen(
            data2_cleaned.iloc[44:54], 2020)
        total_df4_ranPen = aggregate_and_rename_ranPen(
            data2_cleaned.iloc[63:73], 2021)
        total_df5_ranPen = aggregate_and_rename_ranPen(
            data2_cleaned.iloc[82:92], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_ranPen = total_df1_ranPen
        for df in [total_df2_ranPen, total_df3_ranPen, total_df4_ranPen, total_df5_ranPen]:
            total_merged_ranPen = pd.merge(
                total_merged_ranPen, df, on='Kesatuan', how='outer')

        # Menghitung total ran barang per kesatuan untuk setiap rentang baris dan tahun
        total_df1_ranBar = aggregate_and_rename_ranBar(
            data2_cleaned.iloc[6:16], 2018)
        total_df2_ranBar = aggregate_and_rename_ranBar(
            data2_cleaned.iloc[25:35], 2019)
        total_df3_ranBar = aggregate_and_rename_ranBar(
            data2_cleaned.iloc[44:54], 2020)
        total_df4_ranBar = aggregate_and_rename_ranBar(
            data2_cleaned.iloc[63:73], 2021)
        total_df5_ranBar = aggregate_and_rename_ranBar(
            data2_cleaned.iloc[82:92], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_ranBar = total_df1_ranBar
        for df in [total_df2_ranBar, total_df3_ranBar, total_df4_ranBar, total_df5_ranBar]:
            total_merged_ranBar = pd.merge(
                total_merged_ranBar, df, on='Kesatuan', how='outer')

        # Menghitung total bus per kesatuan untuk setiap rentang baris dan tahun
        total_df1_bus = aggregate_and_rename_bus(
            data2_cleaned.iloc[6:16], 2018)
        total_df2_bus = aggregate_and_rename_bus(
            data2_cleaned.iloc[25:35], 2019)
        total_df3_bus = aggregate_and_rename_bus(
            data2_cleaned.iloc[44:54], 2020)
        total_df4_bus = aggregate_and_rename_bus(
            data2_cleaned.iloc[63:73], 2021)
        total_df5_bus = aggregate_and_rename_bus(
            data2_cleaned.iloc[82:92], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_bus = total_df1_bus
        for df in [total_df2_bus, total_df3_bus, total_df4_bus, total_df5_bus]:
            total_merged_bus = pd.merge(
                total_merged_bus, df, on='Kesatuan', how='outer')

        # Menghitung total ran khusus per kesatuan untuk setiap rentang baris dan tahun
        total_df1_ranKhus = aggregate_and_rename_ranKhus(
            data2_cleaned.iloc[6:16], 2018)
        total_df2_ranKhus = aggregate_and_rename_ranKhus(
            data2_cleaned.iloc[25:35], 2019)
        total_df3_ranKhus = aggregate_and_rename_ranKhus(
            data2_cleaned.iloc[44:54], 2020)
        total_df4_ranKhus = aggregate_and_rename_ranKhus(
            data2_cleaned.iloc[63:73], 2021)
        total_df5_ranKhus = aggregate_and_rename_ranKhus(
            data2_cleaned.iloc[82:92], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_ranKhus = total_df1_ranKhus
        for df in [total_df2_ranKhus, total_df3_ranKhus, total_df4_ranKhus, total_df5_ranKhus]:
            total_merged_ranKhus = pd.merge(
                total_merged_ranKhus, df, on='Kesatuan', how='outer')

        # Menggabungkan data 'Sepeda Mototr', 'Ran Penumpang', 'Ran Barang', 'Bus' dan 'Ran Khusus' untuk setiap tahun
        total_merged_vehicle_1 = pd.merge(
            total_merged_spd, total_merged_ranPen, on='Kesatuan', how='outer')
        total_merged_vehicle_1 = pd.DataFrame(total_merged_vehicle_1)
        total_vehicle = total_merged_vehicle_1
        for df in [total_merged_ranBar, total_merged_bus, total_merged_ranKhus]:
            total_vehicle = pd.merge(
                total_vehicle, df, on='Kesatuan', how='outer')
        # print(total_vehicle)

        # Menghitung total usia 0-9 per kesatuan untuk setiap rentang baris dan tahun
        total_df1_09 = aggregate_and_rename_0_9(data3_cleaned.iloc[6:16], 2018)
        total_df2_09 = aggregate_and_rename_0_9(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_09 = aggregate_and_rename_0_9(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_09 = aggregate_and_rename_0_9(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_09 = aggregate_and_rename_0_9(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_09 = total_df1_09
        for df in [total_df2_09, total_df3_09, total_df4_09, total_df5_09]:
            total_merged_09 = pd.merge(
                total_merged_09, df, on='Kesatuan', how='outer')

        # Menghitung total usia 10-15 per kesatuan untuk setiap rentang baris dan tahun
        total_df1_10 = aggregate_and_rename_10_15(
            data3_cleaned.iloc[6:16], 2018)
        total_df2_10 = aggregate_and_rename_10_15(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_10 = aggregate_and_rename_10_15(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_10 = aggregate_and_rename_10_15(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_10 = aggregate_and_rename_10_15(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_10_15 = total_df1_10
        for df in [total_df2_10, total_df3_10, total_df4_10, total_df5_10]:
            total_merged_10_15 = pd.merge(
                total_merged_10_15, df, on='Kesatuan', how='outer')

        # Menghitung total usia 16-30 per kesatuan untuk setiap rentang baris dan tahun
        total_df1_30 = aggregate_and_rename_16_30(
            data3_cleaned.iloc[6:16], 2018)
        total_df2_30 = aggregate_and_rename_16_30(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_30 = aggregate_and_rename_16_30(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_30 = aggregate_and_rename_16_30(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_30 = aggregate_and_rename_16_30(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_16_30 = total_df1_30
        for df in [total_df2_30, total_df3_30, total_df4_30, total_df5_30]:
            total_merged_16_30 = pd.merge(
                total_merged_16_30, df, on='Kesatuan', how='outer')

        # Menghitung total usia 31-40 per kesatuan untuk setiap rentang baris dan tahun
        total_df1_40 = aggregate_and_rename_31_40(
            data3_cleaned.iloc[6:16], 2018)
        total_df2_40 = aggregate_and_rename_31_40(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_40 = aggregate_and_rename_31_40(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_40 = aggregate_and_rename_31_40(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_40 = aggregate_and_rename_31_40(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_31_40 = total_df1_40
        for df in [total_df2_40, total_df3_40, total_df4_40, total_df5_40]:
            total_merged_31_40 = pd.merge(
                total_merged_31_40, df, on='Kesatuan', how='outer')

        # Menghitung total usia 41-50 per kesatuan untuk setiap rentang baris dan tahun
        total_df1_50 = aggregate_and_rename_41_50(
            data3_cleaned.iloc[6:16], 2018)
        total_df2_50 = aggregate_and_rename_41_50(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_50 = aggregate_and_rename_41_50(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_50 = aggregate_and_rename_41_50(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_50 = aggregate_and_rename_41_50(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_41_50 = total_df1_50
        for df in [total_df2_50, total_df3_50, total_df4_50, total_df5_50]:
            total_merged_41_50 = pd.merge(
                total_merged_41_50, df, on='Kesatuan', how='outer')

        # Menghitung total 50 keatas per kesatuan untuk setiap rentang baris dan tahun
        total_df1_50up = aggregate_and_rename_50up(
            data3_cleaned.iloc[6:16], 2018)
        total_df2_50up = aggregate_and_rename_50up(
            data3_cleaned.iloc[25:35], 2019)
        total_df3_50up = aggregate_and_rename_50up(
            data3_cleaned.iloc[43:53], 2020)
        total_df4_50up = aggregate_and_rename_50up(
            data3_cleaned.iloc[61:71], 2021)
        total_df5_50up = aggregate_and_rename_50up(
            data3_cleaned.iloc[79:89], 2022)

        # Menggabungkan total dari masing-masing DataFrame
        total_merged_50up = total_df1_50up
        for df in [total_df2_50up, total_df3_50up, total_df4_50up, total_df5_50up]:
            total_merged_50up = pd.merge(
                total_merged_50up, df, on='Kesatuan', how='outer')

        # Menggabungkan data usia '0-9','10-15', '16-30', 31-40','41-50' dan '50 keatas' untuk setiap tahun
        total_victims = total_merged_09
        for df in [total_merged_10_15, total_merged_16_30, total_merged_31_40, total_merged_41_50, total_merged_50up]:
            total_victims = pd.merge(
                total_victims, df, on='Kesatuan', how='outer')
        # print(total_victims)

        # Menjumlahkan tiap-tiap atribut
        total_merged['Jumlah Kecelakaan'] = total_merged.loc[:, ['Jumlah Kecelakaan_2018', 'Jumlah Kecelakaan_2019',
                                                                 'Jumlah Kecelakaan_2020', 'Jumlah Kecelakaan_2021', 'Jumlah Kecelakaan_2022']].sum(axis=1)
        dataset1_prep = total_merged[['Kesatuan', 'Jumlah Kecelakaan']]
        dataset1_prep = pd.DataFrame(dataset1_prep)
        # print(dataset1_prep)

        total_merged['Kerugian Material'] = total_merged.loc[:, ['Kerugian Material_2018', 'Kerugian Material_2019',
                                                                 'Kerugian Material_2020', 'Kerugian Material_2021', 'Kerugian Material_2022']].sum(axis=1)
        dataset1_prep = total_merged[['Kesatuan',
                                      'Jumlah Kecelakaan', 'Kerugian Material']]
        dataset1_prep = pd.DataFrame(dataset1_prep)
        # print(dataset1_prep)

        total_merged['Jumlah Kendaraan'] = total_vehicle.loc[:, ['Sepeda Motor_2018', 'Sepeda Motor_2019', 'Sepeda Motor_2020', 'Sepeda Motor_2021', 'Sepeda Motor_2022', 'Ran Penumpang_2018', 'Ran Penumpang_2019', 'Ran Penumpang_2020', 'Ran Penumpang_2021', 'Ran Penumpang_2022',
                                                                 'Ran Barang_2018', 'Ran Barang_2019', 'Ran Barang_2020', 'Ran Barang_2021', 'Ran Barang_2022', 'Bus_2018', 'Bus_2019', 'Bus_2020', 'Bus_2021', 'Bus_2022', 'Ran Khusus_2018', 'Ran Khusus_2019', 'Ran Khusus_2020', 'Ran Khusus_2021', 'Ran Khusus_2022']].sum(axis=1)
        dataset1_prep = total_merged[[
            'Kesatuan', 'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Kerugian Material']]
        dataset1_prep = pd.DataFrame(dataset1_prep)
        # print(dataset1_prep)

        total_merged['Jumlah Korban'] = total_victims.loc[:, ['0 - 9_2018', '0 - 9_2019', '0 - 9_2020', '0 - 9_2021', '0 - 9_2022', '10 - 15_2018', '10 - 15_2019', '10 - 15_2020', '10 - 15_2021', '10 - 15_2022', '16 - 30_2018', '16 - 30_2019', '16 - 30_2020', '16 - 30_2021',
                                                              '16 - 30_2022', '31 - 40_2018', '31 - 40_2019', '31 - 40_2020', '31 - 40_2021', '31 - 40_2022', '41 - 50_2018', '41 - 50_2019', '41 - 50_2020', '41 - 50_2021', '41 - 50_2022', '51 KEATAS_2018', '51 KEATAS_2019', '51 KEATAS_2020', '51 KEATAS_2021', '51 KEATAS_2022']].sum(axis=1)
        dataset1_prep = total_merged[['Kesatuan', 'Jumlah Kecelakaan',
                                      'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']]
        dataset1_prep = pd.DataFrame(dataset1_prep)
        dataset1_prep_num = dataset1_prep[[
            'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']]
        dataset1_prep_num = pd.DataFrame(dataset1_prep_num)
        print(dataset1_prep)
        print(type(dataset1_prep))
        print(dataset1_prep_num)
        # dataset siap digunakan untuk preprocessing
        print(type(dataset1_prep_num))
        self.data = dataset1_prep
        # Kembali ke proses penggabungan data dan lainnya seperti dalam kode Anda
        # ...

    def get_data(self):
        return self.data


class Preparation_dataset2:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        self.data = pd.read_excel(self.file_path)
        return self.data

# menjumlahkan data kecelakaan (sorting)
    def aggregate_data2(self):
        self.data = self.data['Street'].value_counts().reset_index()
        self.data.columns = ['Street', 'Sum of Accident']
        self.data = pd.DataFrame(self.data)

    def get_data(self):
        return self.data
