import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Leer los datos del archivo CSV con los nombres de los departamentos
df = pd.read_csv('InfoVis/Covid19Casos.csv')

# Crear un diccionario para almacenar los conteos de casos por departamento
casos_por_departamento = {}

# Crear un objeto geocodificador
geolocator = Nominatim(user_agent="my_geocoder")

# Función auxiliar para geocodificar el departamento y obtener sus coordenadas
def geocode_departamento(departamento):
    max_attempts = 3
    attempt = 1
    while attempt <= max_attempts:
        try:
            location = geolocator.geocode(departamento)
            if location is not None:
                # Verificar si las coordenadas están dentro de Argentina
                if location.latitude > -55 and location.latitude < -21 and location.longitude > -76 and location.longitude < -53:
                    return location.latitude, location.longitude
            return None, None
        except (GeocoderTimedOut, GeocoderUnavailable):
            attempt += 1
    return None, None

# Iterar sobre los departamentos en el DataFrame
for index, row in df.iterrows():
    departamento = row['residencia_departamento_nombre']
    if departamento not in casos_por_departamento:
        casos_por_departamento[departamento] = 1
    else:
        casos_por_departamento[departamento] += 1

# Crear un diccionario para almacenar las coordenadas de los departamentos
coordenadas_departamentos = {}

# Obtener las coordenadas de los departamentos
for departamento in casos_por_departamento:
    latitud, longitud = geocode_departamento(departamento)
    coordenadas_departamentos[departamento] = (latitud, longitud)

# Obtener las listas de datos para el gráfico 3D
departamentos = []
casos = []
latitudes = []
longitudes = []

# Filtrar los departamentos y sus coordenadas dentro de Argentina
for departamento, coordenadas in coordenadas_departamentos.items():
    if coordenadas[0] is not None and coordenadas[1] is not None:
        departamentos.append(departamento)
        casos.append(casos_por_departamento[departamento])
        latitudes.append(coordenadas[0])
        longitudes.append(coordenadas[1])

# Crear la figura y el eje 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Configurar los ejes
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
ax.set_zlabel('Cantidad de Casos')

# Crear el gráfico 3D de dispersión
ax.scatter(longitudes, latitudes, casos)

# Guardar el gráfico en un archivo
fig.savefig('InfoVis/grafico_3D.png')

# Mostrar el gráfico
plt.show()
