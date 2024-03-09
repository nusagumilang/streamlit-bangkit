import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

sns.set(style='dark')

# Helper functions
def create_month_group(df):
    month_group = df[['mnth', 'cnt']].groupby('mnth').sum().sort_values('cnt', ascending = False)
    return month_group

def create_workingday_group(df):
    workingday_group = df[['workingday', 'cnt']].groupby('workingday').mean().sort_values('cnt', ascending = False)
    return workingday_group

def create_season_group(df):
    season_group = df[['season', 'cnt']].groupby('season').mean().sort_values('cnt', ascending = False)
    return season_group

def create_year_group(df):
    year_group = df[['yr', 'cnt']].groupby('yr').mean()
    return year_group

def create_hour_group(df):
    hour_group = df[['hr', 'cnt']].groupby('hr').mean().sort_values('cnt', ascending = False)
    return hour_group

# Load cleaned data
day = pd.read_csv("day_cleaned.csv")
hour = pd.read_csv("hour_cleaned.csv")

# Mengubah tipe data
day['dteday'] = pd.to_datetime(day['dteday'])

hour['dteday'] = pd.to_datetime(hour['dteday'])

# Filter data
min_date = day["dteday"].min()
max_date = day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/nusagumilang/keperluanbangkit/blob/main/logo.png?raw=true")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label = 'Rentang Waktu', min_value = min_date,
        max_value = max_date,
        value = [min_date, max_date]
    )

main_day = day[(day["dteday"] >= str(start_date)) & 
                (day["dteday"] <= str(end_date))]
main_hour = hour[(hour["dteday"] >= str(start_date)) & 
                (hour["dteday"] <= str(end_date))]

# Mempersiapkan dataframe kebutuhan
grouped_month = create_month_group(main_day)
grouped_workingday = create_workingday_group(main_day)
grouped_season = create_season_group(main_day)
grouped_year = create_year_group(main_day)
grouped_hour = create_hour_group(main_hour)

# Judul
st.title('Dashboard The Bike Sharing Company')

# Pendefinisian tab
tab_interactive, tab_static, tab_data = st.tabs(["Penyewa Sepeda", "Analisis", "Data"])

with tab_interactive:
    st.header("Jumlah Penyewa Sepeda Berdasarkan Waktu")
    fig_timeseries = px.line(main_day,
                  x = "dteday",
                  y = "cnt",
                  title = "Grafik Jumlah Penyewa Sepeda").update_layout(
                    xaxis_title="Tanggal", yaxis_title="Jumlah Penyewa Sepeda")
    st.plotly_chart(fig_timeseries)

with tab_static:
    st.header("Analisis Data")
    
    # Plot bulan
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Bulan")
    fig_bulan, ax_bulan = plt.subplots(figsize=(16, 8))
    sns.barplot(data = grouped_month, x = grouped_month.index, y = grouped_month['cnt'], order = grouped_month.index)
    ax_bulan.set(xlabel='Bulan',
                  ylabel='Rata-Rata Jumlah Penyewaan Sepeda',
                  title='Grafik Rata-Rata Jumlah Penyewaan Sepeda Berdasarkan Bulan')
    st.pyplot(fig_bulan)
    
    # Plot libur
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Hari Libur")
    fig_libur, ax_libur = plt.subplots(figsize=(16, 8))
    sns.barplot(data = grouped_workingday, x = grouped_workingday.index, y = 'cnt')
    ax_libur.set(xlabel='Hari',
                  ylabel='Rata-Rata Jumlah Penyewaan Sepeda',
                  title='Grafik Rata-Rata Jumlah Penyewaan Sepeda Berdasarkan Hari Libur')
    st.pyplot(fig_libur)

    # Plot musim
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Musim")
    fig_musim, ax_musim = plt.subplots(figsize=(16, 8))
    sns.barplot(data = grouped_season, x = grouped_season.index, y = 'cnt')
    ax_musim.set(xlabel='Musim',
                  ylabel='Rata-Rata Jumlah Penyewaan Sepeda',
                  title='Grafik Rata-Rata Jumlah Penyewaan Sepeda Berdasarkan Musim')
    st.pyplot(fig_musim)

    # Plot tahun
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Tahun")
    fig_tahun, ax_tahun = plt.subplots(figsize=(16, 8))
    sns.barplot(data = grouped_year, x = grouped_year.index, y = 'cnt', order = grouped_year.index)
    ax_tahun.set(xlabel='Tahun',
                  ylabel='Rata-Rata Jumlah Penyewaan Sepeda',
                  title='Grafik Rata-Rata Jumlah Penyewaan Sepeda Berdasarkan Tahun')
    st.pyplot(fig_tahun)

    # Plot hour
    st.subheader("Jumlah Penyewa Sepeda Berdasarkan Jam")
    fig_jam, ax_jam = plt.subplots(figsize=(16, 8))
    sns.barplot(data = grouped_hour, x = grouped_hour.index, y = 'cnt', order = grouped_hour.index)
    ax_jam.set(xlabel='Jam',
                  ylabel='Rata-Rata Jumlah Penyewaan Sepeda',
                  title='Grafik Rata-Rata Jumlah Penyewaan Sepeda Berdasarkan Jam')
    st.pyplot(fig_jam)

with tab_data:
    st.header('Data Lengkap')

    # Data day
    st.subheader('Data Harian')
    with st.container():
        st.dataframe(data = main_day)

    # Data jam
    st.subheader('Data Jam-an')
    with st.container():
        st.dataframe(data = main_hour)
