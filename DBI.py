from sklearn.metrics import davies_bouldin_score
import numpy as np


class DBIEvaluator:
    def __init__(self, data, model):
        self.data = data
        self.model = model

    def calculate_dbi1(self):
        # Pastikan model sudah dilatih
        if hasattr(self.model, 'labels_'):
            dbi = davies_bouldin_score(self.data, self.model.labels_)
            return dbi
        else:
            raise ValueError(
                "Model belum dilatih. Pastikan model sudah melalui proses fitting.")

    def compute_dbi2(self, target_column):
        # Ensure target_column is a string
        if not isinstance(target_column, str):
            raise TypeError(
                f"target_column should be a string, got {type(target_column)} instead.")

        labels = np.zeros(len(self.data))
        for cluster_idx, cluster in enumerate(self.model.clusters):
            for idx in cluster:
                labels[idx] = cluster_idx

        # Ensure the data is correctly formatted for davies_bouldin_score
        data_subset = self.data[target_column].to_numpy().reshape(-1, 1)
        dbi_score = davies_bouldin_score(data_subset, labels)
        return dbi_score
