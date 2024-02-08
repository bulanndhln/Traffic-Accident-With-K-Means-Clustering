import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px


class ModelImplementation_dataset1:
    def __init__(self, data, normalized_data):
        self.data = data
        self.normalized_data = normalized_data
        self.kmeans = None
        self.data_scaled_df = None
        self.min_max_values = []

    def perform_clustering(self, n_cluster):
        if not isinstance(self.normalized_data, pd.DataFrame):
            raise ValueError(
                "self.normalized_data harus berupa pandas DataFrame")
        if not isinstance(self.data, pd.DataFrame):
            raise ValueError("self.data harus berupa pandas DataFrame")

        expected_columns = [
            'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']
        missing_cols = [
            col for col in expected_columns if col not in self.normalized_data.columns]
        if missing_cols:
            raise ValueError(
                f"Kolom berikut tidak ditemukan dalam normalized_data: {missing_cols}")

        # Gunakan nilai random_state yang tetap untuk reproduktibilitas
        self.kmeans = KMeans(n_clusters=n_cluster, init='k-means++',
                             max_iter=300, n_init='auto', random_state=42)
        self.data_scaled_df = self.normalized_data.copy()
        self.data_scaled_df['Cluster'] = self.kmeans.fit_predict(
            self.normalized_data[expected_columns])

        # Tambahkan kolom 'Cluster' ke DataFrame yang sudah ada
        self.data['Cluster'] = self.data_scaled_df['Cluster']

        return self.data

    def cluster_members(self):
        cluster_info = []

        for cluster_num in range(self.kmeans.n_clusters):
            # Mendapatkan anggota klaster
            cluster_members = self.data_scaled_df[self.data_scaled_df['Cluster'] == cluster_num]

            # Menyimpan jumlah anggota dan DataFrame anggota klaster
            member_count = len(cluster_members)
            members_df = pd.DataFrame(
                {'': cluster_members['Kesatuan']})

            cluster_info.append(
                (f"Anggota Klaster {cluster_num}: {member_count} Anggota", members_df))

        return cluster_info

    def category(self):
        # Menghitung ambang batas untuk kategori
        batas_sangat_rawan = np.percentile(
            self.data[['Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']], 50)
        batas_rawan = np.percentile(self.data[[
                                    'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']], 25)
        batas_tidak_rawan = np.percentile(
            self.data[['Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']], 25)

        # Inisialisasi list untuk menyimpan informasi klaster
        min_max_values_list = []

        # Pastikan model K-Means sudah dilatih
        if self.kmeans is None:
            raise ValueError("Model K-Means belum dilatih")

        # Iterasi melalui setiap klaster untuk mendapatkan nilai minimal dan maksimal dari data asli
        for cluster_num in range(self.kmeans.n_clusters):
            cluster_members = self.data[self.data['Cluster'] == cluster_num]
            min_values = cluster_members[[
                'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']].min()
            max_values = cluster_members[[
                'Jumlah Kecelakaan', 'Jumlah Kendaraan', 'Jumlah Korban', 'Kerugian Material']].max()

            # Menentukan kategori berdasarkan nilai maksimal 'Jumlah Kecelakaan' dari data asli
            kategori = 'Tidak Rawan'
            if max_values['Jumlah Kecelakaan'] >= batas_rawan:
                kategori = 'Rawan'
            if max_values['Jumlah Kecelakaan'] >= batas_sangat_rawan:
                kategori = 'Sangat Rawan'

            min_max_values_list.append({
                'cluster': cluster_num,
                'min_values': min_values.to_dict(),
                'max_values': max_values.to_dict(),
                'kategori': kategori
            })

        # Mengonversi list menjadi DataFrame
        # self.min_max_values = pd.DataFrame(min_max_values_list)
        return min_max_values_list

    def cluster_members_histogram(self):
        figure = []
        # Menghitung total 'Jumlah Kecelakaan' untuk setiap klaster
        cluster_total_incidents = self.data.groupby(
            'Kesatuan')['Jumlah Kecelakaan'].sum()

        # Membuat DataFrame untuk histogram
        histogram_data = pd.DataFrame({
            'Kesatuan': cluster_total_incidents.index,
            'Total Kecelakaan': cluster_total_incidents.values
        })
        histogram_data = histogram_data.sort_values(
            'Total Kecelakaan', ascending=False).head(10)
        # Menentukan warna untuk setiap klaster menggunakan palet warna Plotly
        colors = px.colors.qualitative.Plotly

        # Membuat histogram horizontal
        fig = px.bar(
            histogram_data,
            y='Kesatuan',
            x='Total Kecelakaan',
            title='Total Kecelakaan teratas Berdasarkan Kesatuan',
            color='Kesatuan',
            orientation='h',
            color_discrete_sequence=colors
        )

        # Menambahkan detail ke layout
        fig.update_layout(
            yaxis_title='Kesatuan',
            xaxis_title='Total Kecelakaan',
            yaxis={'type': 'category'},
            xaxis=dict(type='linear'),
            bargap=0.2
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})

        figure.append(fig)

        # ===============================================
        total_korban = self.data.groupby(
            'Kesatuan')['Jumlah Korban'].sum()

        # Membuat DataFrame untuk histogram
        histogram_data = pd.DataFrame({
            'Kesatuan': total_korban.index,
            'Total Korban': cluster_total_incidents.values
        })
        histogram_data = histogram_data.sort_values(
            'Total Korban', ascending=False).head(10)
        # Menentukan warna untuk setiap klaster menggunakan palet warna Plotly
        colors = px.colors.qualitative.Plotly

        # Membuat histogram horizontal
        fig = px.bar(
            histogram_data,
            y='Kesatuan',
            x='Total Korban',
            title='Total Korban teratas Berdasarkan Kesatuan',
            color='Kesatuan',
            orientation='h',
            color_discrete_sequence=colors
        )

        # Menambahkan detail ke layout
        fig.update_layout(
            yaxis_title='Kesatuan',
            xaxis_title='Total Korban',
            yaxis={'type': 'category'},
            xaxis=dict(type='linear'),
            bargap=0.2
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        figure.append(fig)
        # ============================================================
        cluster_total_incidents = self.data.groupby(
            'Kesatuan')['Jumlah Kendaraan'].sum()

        # Membuat DataFrame untuk histogram
        histogram_data = pd.DataFrame({
            'Kesatuan': cluster_total_incidents.index,
            'Total Kendaraan': cluster_total_incidents.values
        })
        histogram_data = histogram_data.sort_values(
            'Total Kendaraan', ascending=False).head(10)
        # Menentukan warna untuk setiap klaster menggunakan palet warna Plotly
        colors = px.colors.qualitative.Plotly

        # Membuat histogram horizontal
        fig = px.bar(
            histogram_data,
            y='Kesatuan',
            x='Total Kendaraan',
            title='Total Kendaraan teratas Berdasarkan Kesatuan',
            color='Kesatuan',
            orientation='h',
            color_discrete_sequence=colors
        )

        # Menambahkan detail ke layout
        fig.update_layout(
            yaxis_title='Kesatuan',
            xaxis_title='Total Kendaraan',
            yaxis={'type': 'category'},
            xaxis=dict(type='linear'),
            bargap=0.2
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})

        figure.append(fig)

        # ===============================================
        total_korban = self.data.groupby(
            'Kesatuan')['Kerugian Material'].sum()

        # Membuat DataFrame untuk histogram
        histogram_data = pd.DataFrame({
            'Kesatuan': total_korban.index,
            'Kerugian Material': cluster_total_incidents.values
        })
        histogram_data = histogram_data.sort_values(
            'Kerugian Material', ascending=False).head(10)
        # Menentukan warna untuk setiap klaster menggunakan palet warna Plotly
        colors = px.colors.qualitative.Plotly

        # Membuat histogram horizontal
        fig = px.bar(
            histogram_data,
            y='Kesatuan',
            x='Kerugian Material',
            title='Kerugian Material teratas Berdasarkan Kesatuan',
            color='Kesatuan',
            orientation='h',
            color_discrete_sequence=colors
        )

        # Menambahkan detail ke layout
        fig.update_layout(
            yaxis_title='Kesatuan',
            xaxis_title='Kerugian Material',
            yaxis={'type': 'category'},
            xaxis=dict(type='linear'),
            bargap=0.2
        )
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})

        figure.append(fig)
        return figure

    def plot_clusters(self):
        figures = []
        # Pastikan bahwa 'Cluster' ada di self.data
        if 'Cluster' not in self.data:
            raise ValueError(
                "Kolom 'Cluster' tidak ditemukan. Pastikan model K-Means sudah dilatih dan label klaster telah ditambahkan.")

        # Mendefinisikan skala warna kustom dari merah ke hijau
        colors = px.colors.qualitative.Plotly
        # Plot 1: Clustering berdasarkan Jumlah Kecelakaan
        fig = px.scatter(
            self.data,
            x='Kesatuan',
            y='Jumlah Kecelakaan',
            color='Cluster',
            title='Klasterisasi Kecelakaan Berdasarkan Jumlah Kecelakaan',
            color_continuous_scale=colors
        )
        fig.update_xaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey')
        fig.update_yaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey', gridwidth=1.3)
        fig.update_yaxes(zeroline=True, zerolinewidth=0.5,
                         zerolinecolor='grey')
        # Mengubah warna teks sumbu x
        fig.update_xaxes(title_text='Kesatuan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))

        # Mengubah warna teks sumbu y
        fig.update_yaxes(title_text='Jumlah Kecelakaan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))
        fig.update_traces(marker=dict(size=12),
                          selector=dict(mode='markers'))

        figures.append(fig)

        # Plot 2: Clustering berdasarkan Jumlah Korban
        fig = px.scatter(
            self.data,
            x='Kesatuan',
            y='Jumlah Korban',
            color='Cluster',
            title='Klasterisasi Kecelakaan Berdasarkan Jumlah Korban',
            color_continuous_scale=colors
        )
        fig.update_xaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey')
        fig.update_yaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey', gridwidth=1.3)
        fig.update_yaxes(zeroline=True, zerolinewidth=0.5,
                         zerolinecolor='grey')
        # Mengubah warna teks sumbu x
        fig.update_xaxes(title_text='Kesatuan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))

        # Mengubah warna teks sumbu y
        fig.update_yaxes(title_text='Jumlah Korban', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))
        fig.update_traces(marker=dict(size=12),
                          selector=dict(mode='markers'))
        figures.append(fig)

        # Plot 4: Clustering berdasarkan Jumlah Kendaraan
        fig = px.scatter(
            self.data,
            x='Kesatuan',
            y='Jumlah Kendaraan',
            color='Cluster',
            title='Klasterisasi Kecelakaan Berdasarkan Jumlah Kendaraan',
            color_continuous_scale=colors
        )

        fig.update_xaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey')
        fig.update_yaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey', gridwidth=1.3)
        fig.update_yaxes(zeroline=True, zerolinewidth=0.5,
                         zerolinecolor='grey')
        # Mengubah warna teks sumbu x
        fig.update_xaxes(title_text='Kesatuan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))

        # Mengubah warna teks sumbu y
        fig.update_yaxes(title_text='Jumlah Kendaraan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))
        fig.update_traces(marker=dict(size=12),
                          selector=dict(mode='markers'))
        figures.append(fig)

        # Plot 1: Clustering berdasarkan Kerugian Material
        fig = px.scatter(
            self.data,
            x='Kesatuan',
            y='Kerugian Material',
            color='Cluster',
            title='Klasterisasi Kecelakaan Berdasarkan Kerugian Material',
            color_continuous_scale=colors
        )
        fig.update_xaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey')
        fig.update_yaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey', gridwidth=1.3)
        fig.update_yaxes(zeroline=True, zerolinewidth=0.5,
                         zerolinecolor='grey')
        # Mengubah warna teks sumbu x
        fig.update_xaxes(title_text='Kesatuan', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))

        # Mengubah warna teks sumbu y
        fig.update_yaxes(title_text='Kerugian Material', title_font=dict(color='Black'),
                         tickfont=dict(color='Black'))
        fig.update_traces(marker=dict(size=12),
                          selector=dict(mode='markers'))
        figures.append(fig)

        return figures


class ModelImplementation_dataset2:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.results = None

    @staticmethod
    def euclidean_distance(x1, x2):
        return np.sqrt(np.sum((x1 - x2)**2))

    # Inisialisasi centroid awal dengan K-Means++
    def kmeans_plus_plus(self, n_clusters, target_column):
        # np.random.seed(0)  # Menetapkan seed acak yang tetap
        centers = [
            self.data[target_column].iloc[np.random.randint(len(self.data))]]
        while len(centers) < n_clusters:
            dist_sq = np.array([min([np.inner(c - x, c - x) for c in centers])
                               for x in self.data[target_column]])
            probs = dist_sq / dist_sq.sum()
            cumulative_probs = probs.cumsum()
            r = np.random.rand()
            for j, p in enumerate(cumulative_probs):
                if r < p:
                    i = j
                    break
            centers.append(self.data[target_column].iloc[i])
        return np.array(centers).reshape(-1, 1)

    def kmeans(self, n_clusters, max_iters=100, target_column='Normalization', random_state=None):
        np.random.seed(random_state)
        centroids = self.kmeans_plus_plus(n_clusters, target_column)
        print("Centroid awal: ", centroids)
        for _ in range(max_iters):
            clusters = [[] for _ in range(n_clusters)]

            for idx, point in enumerate(self.data[target_column]):
                distances = [self.euclidean_distance(
                    point, centroid) for centroid in centroids]
                cluster_idx = np.argmin(distances)
                clusters[cluster_idx].append(idx)

            old_centroids = centroids.copy()

            for cluster_idx, cluster in enumerate(clusters):
                if len(cluster) > 0:
                    cluster_points = self.data.iloc[cluster][target_column]
                    centroids[cluster_idx] = np.array([cluster_points.mean()])

            # Menggunakan norm untuk mengecek konvergensi
            if np.linalg.norm(centroids - old_centroids) < 1e-6:
                break

        self.centroids = centroids
        self.clusters = clusters
        return clusters

    def perform_clustering_data2(self, n_cluster, target_column, max_iters=300):
        self.n_clusters = n_cluster
        cluster = self.kmeans(n_clusters=n_cluster,
                              target_column=target_column, max_iters=max_iters, random_state=0)
        # Inisialisasi array label cluster
        cluster_labels = np.zeros(len(self.data))
        cluster_labels = np.round(cluster_labels).astype(int)
        # Mengisi array dengan label cluster yang sesuai
        for cluster_idx, sample_indices in enumerate(cluster):
            for sample_idx in sample_indices:
                cluster_labels[sample_idx] = cluster_idx
                self.data['Cluster'] = cluster_labels
        self.data['Street'] = self.data['Street']
        self.data = pd.DataFrame(self.data)
        return self.data

    def cluster_member_data2(self):
        cluster_info = []
        for cluster_num in range(self.n_clusters):
            cluster_members = self.data[self.data['Cluster'] == cluster_num]
            # Menyimpan jumlah anggota dan DataFrame anggota klaster
            member_count = len(cluster_members)

            # Pilih hanya kolom yang ingin Anda sertakan dalam output
            members_df = pd.DataFrame({'Street': cluster_members['Street']})

            cluster_info.append(
                (f"Anggota Klaster {cluster_num}: {member_count} Anggota", members_df))

        return cluster_info

    def category(self):
        # Menghitung ambang batas untuk kategori
        batas_sangat_rawan = 0.4
        batas_rawan = 0.27
        # batas_tidak_rawan = np.percentile(self.data[['Normalization']], 25)

        # Pastikan model K-Means sudah dilatih
        if self.kmeans is None:
            raise ValueError("Model K-Means belum dilatih")
        # Inisialisasi list untuk menyimpan informasi klaster
        min_max_values_list = []
        # Iterasi melalui setiap klaster untuk mendapatkan nilai minimal dan maksimal dari data asli
        for cluster_num in range(self.n_clusters):
            cluster_members = self.data[self.data['Cluster']
                                        == cluster_num]

            # Find indices of min and max normalization values
            idx_min = cluster_members['Normalization'].idxmin()
            idx_max = cluster_members['Normalization'].idxmax()

            # Use these indices to find the corresponding sum of accidents
            sum_accidents_min = cluster_members.loc[idx_min, 'Sum of Accident']
            sum_accidents_max = cluster_members.loc[idx_max, 'Sum of Accident']

            # Extract actual scalar values for comparison
            min_normalization_value = cluster_members.loc[idx_min,
                                                          'Normalization']
            max_normalization_value = cluster_members.loc[idx_max,
                                                          'Normalization']

            # Logical comparison for determining the category
            if min_normalization_value < batas_rawan and max_normalization_value < batas_rawan:
                kategori = 'Tidak Rawan'
            elif max_normalization_value > batas_rawan and max_normalization_value < batas_sangat_rawan:
                kategori = 'Rawan'
            else:
                kategori = 'Sangat Rawan'

            min_max_values_list.append({
                'cluster': cluster_num,
                'min_values': {'Normalization': min_normalization_value},
                'max_values': {'Normalization': max_normalization_value},
                'sum_accident_min': sum_accidents_min,
                'sum_accident_max': sum_accidents_max,
                'kategori': kategori
            })
        # Mengonversi list menjadi DataFrame
        # self.min_max_values = pd.DataFrame(min_max_values_list)
        return min_max_values_list

    def visualize_clusters(self):
        # Pastikan bahwa 'Cluster' ada di self.data
        if 'Cluster' not in self.data:
            raise ValueError(
                "Kolom 'Cluster' tidak ditemukan. Pastikan model K-Means sudah dilatih dan label klaster telah ditambahkan.")
        colors = px.colors.qualitative.Plotly

        # Plot data menggunakan Plotly Express dengan semua titik berwarna merah
        fig = px.scatter(
            self.data,
            x='Street',
            y='Normalization',
            color='Cluster',
            labels={'Street': 'Street', 'Normalization': 'Normalization'},
            title='Klasterisasi Kecelakaan Berdasarkan Jumlah Kecelakaan',
            # Mengatur semua titik menjadi merah
            color_continuous_scale=colors
        )

        # Mengupdate detail visualisasi lainnya
        fig.update_xaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey')
        fig.update_yaxes(showline=True, linewidth=2,
                         linecolor='Black', gridcolor='Grey', gridwidth=1.3)
        fig.update_yaxes(zeroline=True, zerolinewidth=0.5,
                         zerolinecolor='grey')
        fig.update_xaxes(title_text='Street', title_font=dict(
            color='Black'), tickfont=dict(color='Black'))
        fig.update_yaxes(title_text='Sum of Accident', title_font=dict(
            color='Black'), tickfont=dict(color='Black'))
        fig.update_traces(marker=dict(size=8), selector=dict(mode='markers'))

        return [fig]

    def plot_cluster_histogram(self):
        # Mengurutkan data berdasarkan 'Number of Incidents' dan memilih 20 teratas
        top_streets = self.data.sort_values(
            'Sum of Accident', ascending=False).head(10)
        colors = px.colors.qualitative.Plotly

        # Membuat grafik batang horizontal dengan Plotly Express
        fig = px.bar(top_streets, y='Street', x='Sum of Accident', orientation='h',
                     title='Lokasi kejadian teratas berdasarkan jumlah kecelakaan (Sum of Accident)', color_discrete_sequence=colors)

        # Mengatur urutan kategori di sumbu y berdasarkan 'Number of Incidents'
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})

        return fig
