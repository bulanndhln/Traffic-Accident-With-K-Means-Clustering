import pandas as pd
import io
import streamlit as st
from preparation import Preparation_dataset1
from preparation import Preparation_dataset2
from preprocessing import Preprocessing_Dataset1
from preprocessing import Preprocessing_Dataset2
from Model import ModelImplementation_dataset1
from Model import ModelImplementation_dataset2
from DBI import DBIEvaluator

st.set_page_config(
    page_title="Klasterisasi",
    page_icon="",


)


class MainWindow:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def main(self):
        col, logo2,  col = st.columns([1, 1, 1])
        with logo2:
            st.image('logo.png', width=250)

        st.markdown("<h1 style='text-align: center'>Klasterisasi Data Kecelakaan Lalu Lintas Jalan Raya di Provinsi Jambi Menggunakan Metode K-Means</h1>", unsafe_allow_html=True)

        # Mengecek apakah tombol sudah ditekan
        if 'button_data_clicked' not in st.session_state:
            st.session_state['button_data_clicked'] = False
        if 'button_locate_clicked' not in st.session_state:
            st.session_state['button_locate_clicked'] = False
        # Now your columns and buttons
        col, col_button1, col_button2, col = st.columns([1, 1, 1, 1])

        with col_button1:
            st.write("")  # Spacer kosong untuk alignment
            if st.button("Klasterisasi Data Kecelakaan", key="data_button"):
                st.session_state['button_locate_clicked'] = False
                st.session_state['button_data_clicked'] = True
        with col_button2:
            st.write("")  # Spacer kosong untuk alignment
            if st.button("Klasterisasi Lokasi Kejadian", key="location_button"):
                st.session_state['button_locate_clicked'] = True
                st.session_state['button_data_clicked'] = False

        if st.session_state['button_data_clicked']:
            st.markdown(
                "<h3 style='text-align: center'>Unggah File Data Kecelakaan</h3>", unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Pilih File", type=['xlsx'], key="file_uploader")

            # ==========================================================================================

            if uploaded_file is not None:
                try:
                    if uploaded_file.name != 'DATA KECELAKAAN LALU LINTAS 2018-2022.xlsx':
                        raise ValueError(
                            "Dataset Tidak Sesuai. Harap unggah file 'DATA KECELAKAAN LALU LINTAS 2018-2022.xlsx'")
                    else:
                        means = st.slider('Tentukan Jumlah Klaster',
                                          2, 7, key="data_slider_key")
                        file_container = io.BytesIO(uploaded_file.getvalue())
                        result_data, member_category, visual_data, DBIndex_data = st.tabs(
                            ["Hasil Klasterisasi", "Anggota dan Kategori", "Chart", "Davies-Bouldin Index"])

                        with result_data:
                            prep1 = Preparation_dataset1(uploaded_file)
                            prep1.load_data()
                            prep1.preparation_data1()
                            prep_data1 = prep1.get_data()  # Pastikan ini mengembalikan data yang diharapkan

                            # Jika prep_data adalah None atau bukan DataFrame, perlu diperbaiki
                            if prep_data1 is None or not isinstance(prep_data1, pd.DataFrame):
                                raise ValueError(
                                    "Preparation data is not valid")

                            preprocessing_instance1 = Preprocessing_Dataset1()
                            normalized_data1 = preprocessing_instance1.normalized_dataset1(
                                prep_data1)
                            model_instance1 = ModelImplementation_dataset1(prep_data1,
                                                                           normalized_data1)
                            clusters1 = model_instance1.perform_clustering(
                                means)

                            st.dataframe(clusters1)
                        with member_category:
                            cluster_info1 = model_instance1.cluster_members()
                            num_cols1_per_row = 3
                            num_rows1 = (len(cluster_info1) +
                                         num_cols1_per_row - 1) // num_cols1_per_row
                            cluster_iter1 = iter(cluster_info1)

                            for _ in range(num_rows1):
                                cols1 = st.columns(num_cols1_per_row)
                                for col in cols1:
                                    try:
                                        cluster_label1, df_display1 = next(
                                            cluster_iter1)
                                        with col:
                                            st.markdown(cluster_label1)
                                            st.write(df_display1)
                                    except StopIteration:
                                        break

                            min_max_kategori1 = model_instance1.category()
                            st.markdown(
                                "<h5 style='text-align: center'>Kategori Klasterisasi</h5>", unsafe_allow_html=True)
                            # Mengatur tampilan klaster

                            # Pastikan kategori_klaster adalah list dari dictionaries
                            if isinstance(min_max_kategori1, list) and all(isinstance(item, dict) for item in min_max_kategori1):
                                for cluster_info_minmax1 in min_max_kategori1:
                                    cluster_html1 = f"""
                                    <div style="text-align: center;">
                                        <h6><br>Klaster {cluster_info_minmax1['cluster']} : {cluster_info_minmax1['kategori']}</h6>
                                        <table style="margin-left: auto; margin-right: auto;">
                                        <tr><th>Nilai Minimal:</th><th style='padding-left:50px;'>Nilai Maksimal:</th></tr>
                                        <tr><td>
                                        Jumlah Kecelakaan: {cluster_info_minmax1['min_values']['Jumlah Kecelakaan']}<br>
                                        Jumlah Kendaraan: {cluster_info_minmax1['min_values']['Jumlah Kendaraan']}<br>
                                        Jumlah Korban: {cluster_info_minmax1['min_values']['Jumlah Korban']}<br>
                                        Kerugian Material: Rp{cluster_info_minmax1['min_values']['Kerugian Material']}</td>
                                        <td style='padding-left:50px;'>
                                        Jumlah Kecelakaan: {cluster_info_minmax1['max_values']['Jumlah Kecelakaan']}<br>
                                        Jumlah Kendaraan: {cluster_info_minmax1['max_values']['Jumlah Kendaraan']}<br>
                                        Jumlah Korban: {cluster_info_minmax1['max_values']['Jumlah Korban']}<br>
                                        Kerugian Material: Rp{cluster_info_minmax1['max_values']['Kerugian Material']}</td>
                                        </tr></table>
                                    </div>
                                    """
                                    st.markdown(
                                        cluster_html1, unsafe_allow_html=True)

                            else:
                                st.error(
                                    "Format data kategori_klaster tidak valid.")

                        with visual_data:
                            plots1 = model_instance1.plot_clusters()
                            for plot1 in plots1:
                                st.plotly_chart(
                                    plot1, theme="streamlit", use_container_width=True)
                            plots2 = model_instance1.cluster_members_histogram()
                            for fig in plots2:
                                st.plotly_chart(fig)
                        with DBIndex_data:
                            dbi_evaluator1 = DBIEvaluator(
                                normalized_data1.drop(columns=['Kesatuan']), model_instance1.kmeans)  # Hapus kolom 'Kesatuan'

                            # Menghitung DBI
                            try:
                                dbi_score1 = dbi_evaluator1.calculate_dbi1()  # Tidak perlu parameter tambahan
                                st.success(
                                    f"Davies-Bouldin Index : {dbi_score1}")
                            except ValueError as e:
                                st.write("Error:", e)

                        st.markdown(
                            "<div style='height: 2px; background-color: black; margin-top: 40px; margin-bottom: 40px;'></div>",
                            unsafe_allow_html=True
                        )

                        try:
                            if uploaded_file.name.endswith('.xlsx'):
                                xls = pd.ExcelFile(
                                    file_container, engine='openpyxl')
                                sheet_names = xls.sheet_names
                                sheet_option = st.selectbox(
                                    f"Pilih Lembar Kerja dari {uploaded_file.name}", sheet_names, key="sheet_selector")
                                df = pd.read_excel(
                                    file_container, sheet_name=sheet_option, engine='openpyxl')

                                st.write(
                                    f"Pertinjauan dari file {uploaded_file.name}:")
                                st.dataframe(df)
                                st.markdown(
                                    "<h3 style='text-align: center'>Data Preparation</h3>", unsafe_allow_html=True)

                                prep = Preparation_dataset1(uploaded_file)
                                prep.load_data()
                                prep.preparation_data1()
                                st.session_state['prep_data'] = prep.get_data()
                                st.write("Pertinjauan Dataset:")
                                st.dataframe(st.session_state['prep_data'])
                                st.markdown(
                                    "<h3 style='text-align: center'>Data Preprocessing</h3>", unsafe_allow_html=True)
                                # Jika prep_data adalah None atau bukan DataFrame, perlu diperbaiki
                                if not isinstance(st.session_state['prep_data'], pd.DataFrame):
                                    st.error(
                                        "Data tidak valid untuk dinormalisasikan")
                                else:
                                    preprocessing_instance = Preprocessing_Dataset1(
                                    )
                                    normalized_data = preprocessing_instance.normalized_dataset1(st.session_state['prep_data']
                                                                                                 )

                                    st.write("Data setelah di normalisasikan:")
                                    st.dataframe(normalized_data)

                                    st.markdown(
                                        "<h3 style='text-align: center'>Hasil Klasterisasi</h3>", unsafe_allow_html=True)

                                    st.dataframe(clusters1)

                                    # Asumsikan model_instance adalah instance dari kelas yang memiliki fungsi cluster_members
                                    num_cols1_per_row = 3
                                    num_rows1 = (len(cluster_info1) +
                                                 num_cols1_per_row - 1) // num_cols1_per_row
                                    cluster_iter1 = iter(cluster_info1)

                                    for _ in range(num_rows1):
                                        cols1 = st.columns(num_cols1_per_row)
                                        for col in cols1:
                                            try:
                                                cluster_label1, df_display1 = next(
                                                    cluster_iter1)
                                                with col:
                                                    st.markdown(cluster_label1)
                                                    st.write(df_display1)
                                            except StopIteration:
                                                break

                                    st.markdown(
                                        "<h5 style='text-align: center'>Kategori Klasterisasi</h5>", unsafe_allow_html=True)
                                    # Mengatur tampilan klaster

                                    # Pastikan kategori_klaster adalah list dari dictionaries
                                    if isinstance(min_max_kategori1, list) and all(isinstance(item, dict) for item in min_max_kategori1):
                                        for cluster_info_minmax1 in min_max_kategori1:
                                            cluster_html1 = f"""
                                            <div style="text-align: center;">
                                                <h6><br>Klaster {cluster_info_minmax1['cluster']} : {cluster_info_minmax1['kategori']}</h6>
                                                <table style="margin-left: auto; margin-right: auto;">
                                                <tr><th>Nilai Minimal:</th><th style='padding-left:50px;'>Nilai Maksimal:</th></tr>
                                                <tr><td>
                                                Jumlah Kecelakaan: {cluster_info_minmax1['min_values']['Jumlah Kecelakaan']}<br>
                                                Jumlah Kendaraan: {cluster_info_minmax1['min_values']['Jumlah Kendaraan']}<br>
                                                Jumlah Korban: {cluster_info_minmax1['min_values']['Jumlah Korban']}<br>
                                                Kerugian Material: Rp{cluster_info_minmax1['min_values']['Kerugian Material']}</td>
                                                <td style='padding-left:50px;'>
                                                Jumlah Kecelakaan: {cluster_info_minmax1['max_values']['Jumlah Kecelakaan']}<br>
                                                Jumlah Kendaraan: {cluster_info_minmax1['max_values']['Jumlah Kendaraan']}<br>
                                                Jumlah Korban: {cluster_info_minmax1['max_values']['Jumlah Korban']}<br>
                                                Kerugian Material: Rp{cluster_info_minmax1['max_values']['Kerugian Material']}</td>
                                                </tr></table>
                                            </div>
                                            """
                                            st.markdown(
                                                cluster_html1, unsafe_allow_html=True)

                                    else:
                                        st.error(
                                            "Format data kategori_klaster tidak valid.")

                                    st.markdown(
                                        "<h3 style='text-align: center'><br><br>Visualisasi Hasil Klasterisasi</h3>", unsafe_allow_html=True)

                                    for plot1 in plots1:
                                        st.plotly_chart(
                                            plot1, theme="streamlit", use_container_width=True)
                                    for fig in plots2:
                                        st.plotly_chart(fig)
                                    # DBI Evaluation
                                    st.markdown(
                                        "<h3 style='text-align: center'><br><br>Davies-Bouldin Index</h3>", unsafe_allow_html=True)

                                    # Menghitung DBI
                                    try:
                                        st.success(
                                            f"Davies-Bouldin Index : {dbi_score1}")
                                    except ValueError as e:
                                        st.write("Error:", e)
                        except Exception as e:
                            st.error(
                                f"Terjadi kesalahan saat membaca file: {e}")
                except ValueError as ve:
                    # Tangani kesalahan spesifik, seperti format file yang salah
                    st.error(f"Terjadi kesalahan: {ve}")
                except Exception as e:
                    # Tangani kesalahan umum saat membaca file
                    st.error(f"Terjadi kesalahan saat membaca file: {e}")
        elif st.session_state['button_locate_clicked']:
            st.markdown(
                "<h3 style='text-align: center'>Unggah File Data Lokasi Kejadian</h3>", unsafe_allow_html=True)

            uploaded_file = st.file_uploader(
                "Pilih File", type=['xlsx'], key="Upload_file")

            if uploaded_file is not None:
                try:
                    if uploaded_file.name != 'Data Lokasi Kejadian.xlsx':
                        raise ValueError(
                            "Dataset Tidak Sesuai. Harap unggah file 'Data Lokasi Kejadian.xlsx")
                    else:
                        means_locate = st.slider(
                            'Tentukan Jumlah Klaster', 2, 7, key='locate_slider_key')
                        file_container = io.BytesIO(uploaded_file.getvalue())
                        result, members, visual, DBIndex = st.tabs(
                            ["Hasil Klasterisasi", "Anggota dan Kategori", "Chart", "Davies-Bouldin Index"])
                        # UNCOMMENT JIKA INGIN MENGETEST
                        # membuat objek preparation dan memanggil metode
                        preparation = Preparation_dataset2(uploaded_file)
                        preparation.load_data()
                        preparation.aggregate_data2()
                        preparation_data = preparation.get_data()
                        # membuat objek preprocessing dan memanggil metode
                        preproc = Preprocessing_Dataset2(preparation_data)
                        normalized_dataset2 = preproc.normalized_dataset2()

                        # Model Implementation
                        with result:
                            model2 = ModelImplementation_dataset2(
                                normalized_dataset2)
                            cluster2 = model2.perform_clustering_data2(
                                means_locate, target_column='Normalization')
                            st.dataframe(cluster2, width=700)
                        with members:
                            cluster_2 = model2.cluster_member_data2()
                            num_cols2_per_row = 2
                            num_rows2 = (len(cluster_2) +
                                         num_cols2_per_row - 1) // num_cols2_per_row
                            cluster_iter2 = iter(cluster_2)

                            for _ in range(num_rows2):
                                cols2 = st.columns(num_cols2_per_row)
                                for col in cols2:
                                    try:
                                        cluster_label2, df_display2 = next(
                                            cluster_iter2)
                                        with col:
                                            st.markdown(cluster_label2)
                                            st.write(df_display2)
                                    except StopIteration:
                                        break
                            minmax_dataset2 = model2.category()
                            st.markdown(
                                "<h5 style='text-align: center'>Kategori Klasterisasi</h5>", unsafe_allow_html=True)
                            # Mengatur tampilan klaster

                            # Pastikan kategori_klaster adalah list dari dictionaries
                            if isinstance(minmax_dataset2, list) and all(isinstance(item, dict) for item in minmax_dataset2):
                                for cluster_minmax in minmax_dataset2:
                                    cluster_html_minmax = f"""
                                    <div style="text-align: center;">
                                        <h6><br>Klaster {cluster_minmax['cluster']} : {cluster_minmax['kategori']}</h6>
                                        <table style="margin-left: auto; margin-right: auto;">
                                        <tr><th>Nilai Minimal:</th><th style='padding-left:50px;'>Nilai Maksimal:</th></tr>
                                        <tr><td>
                                        Jumlah Kecelakaan: {cluster_minmax['sum_accident_min']}</td>
                                        <td style='padding-left:50px;'>
                                        Jumlah Kecelakaan: {cluster_minmax['sum_accident_max']}</td>
                                        </tr></table>
                                    </div>
                                    """
                                    st.markdown(
                                        cluster_html_minmax, unsafe_allow_html=True)

                            else:
                                st.error(
                                    "Format data kategori_klaster tidak valid.")
                        with visual:
                            plot_dataset2 = model2.visualize_clusters()
                            for plot2_data in plot_dataset2:
                                st.plotly_chart(
                                    plot2_data, theme="streamlit", use_container_width=True)
                            histogram_fig = model2.plot_cluster_histogram()
                            st.plotly_chart(
                                histogram_fig, theme="streamlit", use_container_width=True)
                        # DBI Evaluation
                        with DBIndex:
                            dbi_evaluator2 = DBIEvaluator(
                                normalized_dataset2, model2)
                            try:
                                dbi_score_dataset2 = dbi_evaluator2.compute_dbi2(
                                    'Normalization')
                                st.success(
                                    f"Davies-Bouldin Index : {dbi_score_dataset2}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                        st.markdown(
                            "<div style='height: 2px; background-color: black; margin-top: 40px; margin-bottom: 40px;'></div>",
                            unsafe_allow_html=True
                        )
                        try:
                            if uploaded_file.name.endswith('.xlsx'):
                                xls = pd.ExcelFile(
                                    file_container, engine='openpyxl')
                                df = pd.read_excel(
                                    file_container, engine='openpyxl')

                                st.write(
                                    f"Pertinjauan dari file {uploaded_file.name}:")
                                st.markdown(
                                    """
                                <style>
                                .dataframe th, .dataframe td {
                                    white-space: nowrap;
                                    min-width: 100px;  /* or whatever width you deem fit */
                                }
                                </style>
                                """,
                                    unsafe_allow_html=True
                                )
                                st.dataframe(df, width=1500)
                                st.markdown(
                                    "<h3 style='text-align: center'>Data Preparation</h3>", unsafe_allow_html=True)
                                prep_data2 = Preparation_dataset2(
                                    uploaded_file)
                                prep_data2.load_data()
                                prep_data2.aggregate_data2()
                                st.session_state['prep_data2'] = prep_data2.get_data(
                                )
                                st.write("Pertinjauan Dataset:")
                                st.dataframe(
                                    st.session_state['prep_data2'], width=700)

                                st.markdown(
                                    "<h3 style='text-align: center'>Data Preprocessing</h3>", unsafe_allow_html=True)
                                # Jika prep_data2 adalah None atau bukan DataFrame, perlu diperbaiki
                                if not isinstance(st.session_state['prep_data2'], pd.DataFrame):
                                    st.error(
                                        "Data tidak valid untuk dinormalisasikan")
                                else:
                                    preprocessing_data2 = Preprocessing_Dataset2(st.session_state['prep_data2']

                                                                                 )
                                    normalized_data2 = preprocessing_data2.normalized_dataset2()

                                    st.write("Data setelah di normalisasikan:")
                                    st.dataframe(normalized_data2, width=700)
                                    st.markdown(
                                        "<h3 style='text-align: center'>Hasil Klasterisasi</h3>", unsafe_allow_html=True)
                                    st.dataframe(cluster2, width=700)

                                    # Asumsikan model_instance adalah instance dari kelas yang memiliki fungsi cluster_members
                                    num_cols2_per_row = 2
                                    num_rows2 = (len(cluster_2) +
                                                 num_cols2_per_row - 1) // num_cols2_per_row
                                    cluster_iter2 = iter(cluster_2)

                                    for _ in range(num_rows2):
                                        cols2 = st.columns(num_cols2_per_row)
                                        for col in cols2:
                                            try:
                                                cluster_label2, df_display2 = next(
                                                    cluster_iter2)
                                                with col:
                                                    st.markdown(cluster_label2)
                                                    st.write(df_display2)
                                            except StopIteration:
                                                break
                                    st.markdown(
                                        "<h5 style='text-align: center'>Kategori Klasterisasi</h5>", unsafe_allow_html=True)
                                    # Mengatur tampilan klaster

                                    # Pastikan kategori_klaster adalah list dari dictionaries
                                    if isinstance(minmax_dataset2, list) and all(isinstance(item, dict) for item in minmax_dataset2):
                                        for cluster_minmax in minmax_dataset2:
                                            cluster_html_minmax = f"""
                                            <div style="text-align: center;">
                                                <h6><br>Klaster {cluster_minmax['cluster']} : {cluster_minmax['kategori']}</h6>
                                                <table style="margin-left: auto; margin-right: auto;">
                                                <tr><th>Nilai Minimal:</th><th style='padding-left:50px;'>Nilai Maksimal:</th></tr>
                                                <tr><td>
                                                Jumlah Kecelakaan: {cluster_minmax['sum_accident_min']}</td>
                                                <td style='padding-left:50px;'>
                                                Jumlah Kecelakaan: {cluster_minmax['sum_accident_max']}</td>
                                                </tr></table>
                                            </div>
                                            """
                                            st.markdown(
                                                cluster_html_minmax, unsafe_allow_html=True)

                                    else:
                                        st.error(
                                            "Format data kategori_klaster tidak valid.")
                                    st.markdown(
                                        "<h3 style='text-align: center'><br><br>Visualisasi Hasil Klasterisasi</h3>", unsafe_allow_html=True)

                                    for plot2_data in plot_dataset2:
                                        st.plotly_chart(
                                            plot2_data, theme="streamlit", use_container_width=True)
                                    st.plotly_chart(
                                        histogram_fig, theme="streamlit", use_container_width=True)
                                    st.markdown(
                                        "<h3 style='text-align: center'><br><br>Davies-Bouldin Index</h3>", unsafe_allow_html=True)
                                    # DBI Evaluation
                                    try:
                                        st.success(
                                            f"Davies-Bouldin Index : {dbi_score_dataset2}")
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                        except Exception as e:
                            st.error(
                                f"Terjadi kesalahan saat membaca file: {e}")
                except ValueError as ve:
                    # Tangani kesalahan spesifik, seperti format file yang salah
                    st.error(f"Terjadi kesalahan: {ve}")
                except Exception as e:
                    # Tangani kesalahan umum saat membaca file
                    st.error(f"Terjadi kesalahan saat membaca file: {e}")




if __name__ == '__main__':
    # Membuat objek dari kelas MainWindow
    main_window = MainWindow()
    main_window.main()
