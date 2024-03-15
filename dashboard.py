import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import datetime

sns.set(style='white')

st.write('Nama : Bimantyoso H')
st.write('bimantyosohamdikatam@gmail.com')
st.write('Dataset : air quality_PRSA 2013-2017')

all_data_cleaned = pd.read_csv('all_data_clean.csv')

# Konversi kolom tanggal ke tipe datetime
all_data_cleaned['datetime'] = pd.to_datetime(all_data_cleaned[['year', 'month', 'day']])

# Tanggal default awal dan akhir
start_date_default = pd.Timestamp(2013, 3, 1)
end_date_default = pd.Timestamp(2013, 3, 31)

# Sidebar untuk memilih rentang waktu
st.sidebar.header('Pilih Rentang Waktu')
start_date = st.sidebar.date_input("Tanggal Awal", min_value=all_data_cleaned['datetime'].min().date(), max_value=all_data_cleaned['datetime'].max().date(), value=start_date_default)
end_date = st.sidebar.date_input("Tanggal Akhir", min_value=all_data_cleaned['datetime'].min().date(), max_value=all_data_cleaned['datetime'].max().date(), value=end_date_default)

# Batasi rentang waktu maksimal hingga 31 hari
if (end_date - start_date).days > 31:
    st.warning('Rentang waktu tidak boleh lebih dari 31 hari.')
    end_date = start_date + pd.Timedelta(days=31)

# Konversi tanggal yang dipilih menjadi datetime
start_datetime = pd.to_datetime(start_date)
end_datetime = pd.to_datetime(end_date)

# Filter data berdasarkan rentang waktu
filtered_data = all_data_cleaned[(all_data_cleaned['datetime'] >= start_datetime) & (all_data_cleaned['datetime'] <= end_datetime)]
# Hitung total polutan PM2.5 dan PM10
total_pm25 = filtered_data['PM2.5'].sum()
total_pm10 = filtered_data['PM10'].sum()

# Hitung total polutan PM2.5 dan PM10
mean_pm25 = filtered_data['PM2.5'].mean()
mean_pm10 = filtered_data['PM10'].mean()

# Tampilkan scorecard
st.sidebar.markdown('---')
st.sidebar.header('_Total_ _Polutan_')
st.sidebar.markdown(f'**PM2.5:** <span style="color:red">{int(total_pm25)} ug/m^3</span>', unsafe_allow_html=True)
st.sidebar.markdown(f'**PM10:** <span style="color:red">{int(total_pm10)} ug/m^3</span>', unsafe_allow_html=True)
st.sidebar.header('_Average_ _Polutan_')
st.sidebar.markdown(f'**PM2.5:** <span style="color:red">{int(total_pm25)} ug/m^3</span>', unsafe_allow_html=True)
st.sidebar.markdown(f'**PM10:** <span style="color:red">{int(total_pm10)} ug/m^3</span>', unsafe_allow_html=True)
st.sidebar.markdown('---')

# Plot tren polutan PM2.5 berdasarkan tanggal yang dipilih menggunakan Seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x='datetime', y='PM2.5', hue='station', marker='o')
plt.title('Tren Konsentrasi PM2.5 Berdasarkan Tanggal', fontsize=16)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Konsentrasi PM2.5 (ug/m^3)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Stasiun')
plt.tight_layout()

# Header dan caption
st.header('Visualisasi Tren Konsentrasi PM2.5')
st.subheader('Rentang Waktu: {} sampai {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
st.write('Grafik di bawah ini menunjukkan tren konsentrasi PM2.5 di berbagai stasiun udara selama rentang waktu yang dipilih.')

# Tampilkan grafik
st.pyplot(plt)

# Plot tren polutan PM2.5 berdasarkan tanggal yang dipilih menggunakan Seaborn
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x='datetime', y='PM10', hue='station', marker='o')
plt.title('Tren Konsentrasi PM2.5 Berdasarkan Tanggal', fontsize=16)
plt.xlabel('Tanggal', fontsize=12)
plt.ylabel('Konsentrasi PM10 (ug/m^3)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.legend(title='Stasiun')
plt.tight_layout()

# Header dan caption
st.header('Visualisasi Tren Konsentrasi PM10')
st.subheader('Rentang Waktu: {} sampai {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
st.write('Grafik di bawah ini menunjukkan tren konsentrasi PM10 di berbagai stasiun udara selama rentang waktu yang dipilih.')

# Tampilkan grafik
st.pyplot(plt)

# Plot bar chart perbandingan rata-rata polusi pada ketiga stasiun
plt.figure(figsize=(10, 6))
sns.barplot(data=filtered_data.groupby('station').mean().reset_index(), x='station', y='PM2.5', palette=['blue', 'red', 'blue'])
plt.title('Perbandingan Rata-Rata Polusi PM2.5 pada Ketiga Stasiun', fontsize=16)
plt.xlabel('Stasiun', fontsize=12)
plt.ylabel('Rata-Rata PM2.5 (ug/m^3)', fontsize=12)
plt.grid(axis='y')
plt.tight_layout()

# Header dan caption
st.header('Perbandingan Rata-Rata Polusi PM2.5 pada Ketiga Stasiun')
st.subheader('Rentang Waktu: {} sampai {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
st.write('Diagram batang di bawah ini menunjukkan perbandingan rata-rata polusi PM2.5 pada ketiga stasiun udara selama rentang waktu yang dipilih. Bar chart berwarna merah menunjukkan nilai tertinggi.')
plt.xticks(rotation=45)

# Tampilkan grafik
st.pyplot(plt)

# Plot bar chart perbandingan rata-rata polusi pada ketiga stasiun
plt.figure(figsize=(10, 6))
sns.barplot(data=filtered_data.groupby('station').mean().reset_index(), x='station', y='PM10', palette=['blue', 'red', 'blue'])
plt.title('Perbandingan Rata-Rata Polusi PM10 pada Ketiga Stasiun', fontsize=16)
plt.xlabel('Stasiun', fontsize=12)
plt.ylabel('Rata-Rata PM10 (ug/m^3)', fontsize=12)
plt.grid(axis='y')
plt.tight_layout()

# Header dan caption
st.header('Perbandingan Rata-Rata Polusi PM10 pada Ketiga Stasiun')
st.subheader('Rentang Waktu: {} sampai {}'.format(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
st.write('Diagram batang di bawah ini menunjukkan perbandingan rata-rata polusi PM10 pada ketiga stasiun udara selama rentang waktu yang dipilih. Bar chart berwarna merah menunjukkan nilai tertinggi.')
plt.xticks(rotation=45)

# Tampilkan grafik
st.pyplot(plt)

# Definisikan fungsi untuk membuat heatmap
def create_heatmap(year):
    # Filter data berdasarkan tahun dan lokasi
    heatmap_data = all_data_cleaned[(all_data_cleaned['station'].isin(['Aotizhongxin', 'Tiantan', 'Shunyi'])) &
                                (all_data_cleaned['datetime'].dt.year == year)]
    
    # Pivot data untuk membuat heatmap
    heatmap_data = heatmap_data.pivot_table(index='month', columns='station', values='PM2.5', aggfunc='mean')
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".1f", linewidths=.5, ax=ax)
    ax.set_title(f'Heatmap Konsentrasi PM2.5 di Lokasi Aotizhongxin, Tiantan, dan Shunyi ({year})')
    ax.set_xlabel('Lokasi')
    ax.set_ylabel('Bulan')
    st.pyplot(fig)

# Sidebar untuk memilih tahun
selected_year = st.sidebar.selectbox('Pilih Tahun:', sorted(all_data_cleaned['datetime'].dt.year.unique()))

# Panggil fungsi untuk membuat heatmap
create_heatmap(selected_year)
