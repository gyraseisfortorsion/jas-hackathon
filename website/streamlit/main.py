import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from prophet.diagnostics import cross_validation
from prophet.plot import plot_cross_validation_metric
import base64


# Hide footer
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    footer {
        visibility: hidden;
    }
    footer:after {
        content:''; 
        visibility: visible;
        display: block;
        position: relative;
        #background-color: red;
        padding: 5px;
        top: 2px;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# add sidebar menu
st.sidebar.title('📈 Прогнозирование активности')

st.title('📈 Cистема прогнозирования покупательской активности')

"""
### Инструкция по использованию
В данной вкладке вы можете видеть предсказывать временные ряды покупок за каждый блок и скачать его в формате 'csv'. Для этого выберите горизонт предсказания. Имейте ввиду что точность прогноза уменьшается с увеличением горизонта прогноза. Также вы можете выбрать сектор, для которого хотите построить прогноз. После нажмите на кнопку 'Прогнозировать'.
"""

periods_input = st.number_input(
    'Горизонт предсказания (в днях)',
    min_value = 1, max_value = 365
)

# select sector
sector = st.selectbox(
    'Выберите сектор',
    ('Сектор 1', 'Сектор 2', 'Сектор 3', 'Сектор 4', 'Сектор 5', 'Сектор 6',)
)
sector_number = sector.split(' ')[1]

if sector:
    data = pd.read_csv(f'data/sector{sector_number}.csv')
    data['ds'] = pd.to_datetime(data['ds'],errors='coerce')

    # rename columns
    data_presentation = data.rename(columns={'ds': 'Дата', 'y': 'Количество людей'})
    st.dataframe(data_presentation, use_container_width=True)

    max_date = data['ds'].max()

    if st.button('Прогнозировать'):

        m = Prophet()
        m.fit(data)

        """
        ### Визуализация прогноза
        Графики ниже показывают прогнозируемые значения. "yhat" - это прогнозируемое значение, а верхняя и нижняя границы - это (по умолчанию) доверительные интервалы в 80%.
        """

        future = m.make_future_dataframe(periods=periods_input)
        
        forecast = m.predict(future)
        fcst = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

        fcst_filtered =  fcst[fcst['ds'] > max_date]
        fcst_filtered = fcst_filtered.rename(columns={
            'ds': 'Дата', 'yhat': 'Количество людей', 'yhat_lower': 'Нижняя граница', 'yhat_upper': 'Верхняя граница'
        })
        st.dataframe(fcst_filtered, use_container_width=True)
        
        """
        Следующая визуализация показывает прогнозируемые значения (синие точки) и истинные значения (черные точки).
        """
        fig1 = m.plot(forecast)
        st.write(fig1)

        """
        Следующие несколько визуализаций показывают тенденции прогнозируемых значений, тенденции дня недели и годовые тенденции (если набор данных содержит несколько лет). Синяя затененная область представляет верхние и нижние доверительные интервалы.
        """
        fig2 = m.plot_components(forecast)
        st.write(fig2)


        """
        ### Скачать прогноз
        По ссылке ниже вы можете скачать прогноз в формате 'csv'. После скачивания файла, вы можете открыть его в Excel и проанализировать.
        """
        csv_exp = fcst_filtered.to_csv(index=False)
        # When no file name is given, pandas returns the CSV as a string, nice.
        b64 = base64.b64encode(csv_exp.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a>'
        st.markdown(href, unsafe_allow_html=True)