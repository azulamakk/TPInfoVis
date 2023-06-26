import altair as alt
import pandas as pd
from datetime import datetime


df = pd.read_csv('/Users/azulmakk/Downloads/precios-historicos (2).csv')

df = df.filter(items=['fecha_vigencia', 'precio'])
df['fecha_vigencia'] = df['fecha_vigencia'].map(lambda x: x.split(' ')[0])

df = df[df['fecha_vigencia'].str.fullmatch(r'\d{2}/\d{2}/\d{4}')]

df['fecha_vigencia'] = pd.to_datetime(df['fecha_vigencia'], format='%d/%m/%Y', errors='coerce')
df = df[df['fecha_vigencia'].notnull()]
df = df[df['fecha_vigencia'] > datetime(2000, 12, 31)]
df = df[df['fecha_vigencia'] <= datetime.now()]
df['precio'] = pd.to_numeric(df['precio'], errors='coerce')
df = df[df['precio'].notnull()]
df = df[df['precio'] < 500]



alt.data_transformers.disable_max_rows()

alt.Chart(df).mark_rect().encode(
    alt.X('yearmonth(fecha_vigencia):O'),
    alt.Y('precio:Q', bin=alt.Bin(maxbins=30)),
    alt.Color('count():Q', scale=alt.Scale(scheme='greenblue'))
).properties(width = 1000).show()

#.save('grafico_precio_por_fecha.html')