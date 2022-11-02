import streamlit as st
import sqlite3
import pandas as pd

con = sqlite3.connect("Db.db")

df = pd.read_sql_query("Select * From Vehiculos", con)
df1 = pd.read_sql_query("Select * From Precios", con)

dataframe = df.merge(df1, left_on='Version', right_on='Version')
st.title('¿Querés comprarte un auto? Nosotros te ayudamos')
with st.expander('Este es un listado de los autos que te pueden aparecer como opcion final'):
    st.dataframe(dataframe)
st.header('Selecciona lo que consideres mas importante para tu futuro vehículo')
st.subheader('Elegir prioridad en orden ascendente')
select_consumo = st.selectbox('Bajo Consumo', [1,2,3,4,5])
select_potencia = st.selectbox('Potencia', [1,2,3,4,5])
select_seguridad = st.selectbox('Seguridad', [1,2,3,4,5])
marca = st.multiselect('Marca del vehículo', sorted(dataframe['Marca'].unique().tolist()))
precio_max = st.number_input('Precio en miles de pesos, el máximo es de $10.000',min_value=0, max_value=10000)
filtrado = dataframe[(dataframe['Marca'].isin(marca)) & (dataframe['Precio'] < precio_max)]
filtrado['Puntuacion'] = (filtrado['C'] * (1 - select_consumo) + 10) + \
                          (filtrado['P'] * select_potencia + 10) + (filtrado['S'] * select_seguridad)

with st.expander('Los resultados son...'):
    st._arrow_table(
        filtrado.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                               ascending=False),
    )



con.close()
