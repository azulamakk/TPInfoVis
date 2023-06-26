import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Leer los datos del archivo CSV
df = pd.read_csv('InfoVis/Covid19Casos_con_lat_long.csv')

# Filtrar los datos sin valores NaN en latitud y longitud
df = df.dropna(subset=['Latitud', 'Longitud'])

# Obtener los valores de latitud, longitud y cantidad de casos
latitudes = df['Latitud']
longitudes = df['Longitud']
casos = df['Cantidad de Casos']

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurar los ejes
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_zlabel('Cantidad de Casos')

# Crear el gráfico 3D de dispersión
ax.scatter(longitudes, latitudes, casos, c=casos, cmap='RdYlGn')

# Mostrar el gráfico
plt.show()
