import pandas as pd
from sklearn.preprocessing import MinMaxScaler


class Preprocessing_Dataset1:
    def __init__(self, data):
        self.data = data
        self.scaler = MinMaxScaler()

    def normalize_data(self):
        # Inisialisasi MinMaxScaler
        scaler = MinMaxScaler()
        # Kolom untuk dinormalisasi
        kolom_untuk_normalisasi = [
            'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']

        # Terapkan normalisasi pada kolom-kolom tertentu di aggregated_data_sorted
        normalized_data = self.data.copy()
        normalized_data[kolom_untuk_normalisasi] = scaler.fit_transform(
            self.data[kolom_untuk_normalisasi])

        return normalized_data


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
        self.data.insert(0, 'No', range(1, len(self.data)+1))

        self.data = pd.DataFrame(self.data)
        self.data = self.data.set_index('No')
        return self.data
