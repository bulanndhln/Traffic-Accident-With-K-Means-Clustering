import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class Preprocessing_Dataset1:
    def __init__(self):
        self.scaler = MinMaxScaler()

    def normalized_dataset1(self, data):

        # Menentukan kolom yang akan dinormalisasi
        columns_to_normalize = [
            'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']

        # Melakukan normalisasi data
        # Gunakan 'self.scaler' yang telah diinisialisasi
        scaled_data = self.scaler.fit_transform(data[columns_to_normalize])

        # Membuat DataFrame dari data yang dinormalisasi
        scaled_df = pd.DataFrame(scaled_data, columns=[
            col + ' Scaled' for col in columns_to_normalize])
        scaled_df['Kesatuan'] = data['Kesatuan']
        scaled_df = scaled_df[['Kesatuan', 'Jumlah Kecelakaan Scaled',
                               'Jumlah Kendaraan Scaled', 'Jumlah Korban Scaled', 'Kerugian Material Scaled']]

        print(scaled_df)
        return scaled_df


class Preprocessing_Dataset2:
    def __init__(self, data):
        self.data = data

    def normalized_dataset2(self):
        self.data = self.data[['Street', 'Sum of Accident']
                              ].value_counts().reset_index()
        self.data.columns = ['Street', 'Sum of Accident', 'Normalization']
        normalization_dataset2 = (self.data['Sum of Accident'] - (self.data['Sum of Accident'].min()))/(
            (self.data['Sum of Accident'].max())-(self.data['Sum of Accident'].min()))

        self.data['Normalization'] = normalization_dataset2

        self.data = pd.DataFrame(self.data)

        return self.data

