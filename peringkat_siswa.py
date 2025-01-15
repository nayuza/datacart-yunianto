import streamlit as st
import pandas as pd
from io import BytesIO

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="Peringkat Siswa SMP", page_icon="🎓", layout="wide")

# Header aplikasi
st.title("🎓 Aplikasi Penentuan Peringkat Siswa SMP")
st.write("Unggah file Excel berisi data siswa untuk menghitung peringkat berdasarkan nilai rata-rata dan pramuka.")

# Fungsi untuk mengolah data
def proses_peringkat(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        
        # Menambahkan kolom ANGKA_PRAMUKA
        df['ANGKA_PRAMUKA'] = df['PRAMUKA'].map({'A': 2, 'B': 1})
        
        # Mengurutkan data dan menambahkan kolom Peringkat
        sorted_df = df.sort_values(['RERATA', 'ANGKA_PRAMUKA'], ascending=False)
        final_df = pd.concat([sorted_df.reset_index(), 
                              pd.DataFrame({'Peringkat': [i + 1 for i in range(len(sorted_df))]})], axis=1).sort_values('index').reset_index()
        final_df = final_df.drop(['level_0', 'index', 'ANGKA_PRAMUKA'], axis=1)
        
        return final_df
    except Exception as e:
        st.error("Terjadi kesalahan saat memproses file. Pastikan format file sesuai.")
        return None

# Unggah file Excel
uploaded_file = st.file_uploader("Unggah file Excel berisi data siswa", type=["xlsx"])

if uploaded_file:
    st.write("📂 File berhasil diunggah!")
    
    # Tampilkan data awal
    st.subheader("📋 Data Awal")
    df = pd.read_excel(uploaded_file)
    st.dataframe(df)
    
    # Proses data
    hasil_df = proses_peringkat(uploaded_file)
    
    if hasil_df is not None:
        # Tampilkan hasil peringkat
        st.subheader("🏆 Hasil Peringkat")
        st.dataframe(hasil_df)

        # Simpan hasil ke buffer BytesIO
        excel_buffer = BytesIO()
        hasil_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        
        # Tambahkan tombol unduh
        st.download_button(
            label="Unduh File Excel",
            data=excel_buffer,
            file_name="peringkat_siswa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# Footer
st.write("By **Datacart**")