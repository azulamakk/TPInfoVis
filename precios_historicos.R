# librerias
library(dplyr)
library(ggplot2)
library(readr)
library(scales)

setwd("/Users/martinavives/Desktop")
preciosHistoricos <- read_csv("precios-historicos.csv") 
# --------------------------------------------

# "precio" 
summary(preciosHistoricos$precio) 
boxplot(preciosHistoricos$precio, main= "Distribución de precios")
preciosHistoricos <- preciosHistoricos %>%  filter(precio != 2430000) # 4 registros

#"fecha_vigencia"
preciosHistoricos$fecha_vigencia <- as.POSIXct(preciosHistoricos$fecha_vigencia, format = "%d/%m/%Y %H:%M")

summary(preciosHistoricos$fecha_vigencia)
length(c(unique(format(preciosHistoricos$fecha_vigencia,"%d"))))
length(c(unique(format(preciosHistoricos$fecha_vigencia,"%m"))))
unique(format(preciosHistoricos$fecha_vigencia,"%Y")) 

# "producto"
preciosHistoricos$producto <- as.factor(preciosHistoricos$producto)

# --------------------------------------------
# selecciono un dataset menor con las cols que necesito
precios <- preciosHistoricos %>% 
  select(fecha_vigencia ,producto, precio) 

precios <- precios %>% 
  filter(format(fecha_vigencia,"%Y") > "2000")

precios <- precios %>%
  filter(format(fecha_vigencia, "%Y") < "2023" | 
           (format(fecha_vigencia, "%Y") == "2023" & 
              format(fecha_vigencia, "%m") < "06")) 

precios %>%  
  group_by(year = format(fecha_vigencia,"%Y")) %>% 
    summarise(cant = n()) %>% arrange(year)

# como la cantidad de registros desde el 2001 hasta 2016 son muy escasos,
# se decide realizar el analisis luego de ese periodo

precios <- precios %>% 
  filter(format(fecha_vigencia, "%Y") > "2016") 

precios$yearMonth <- format(precios$fecha_vigencia, "%Y/%m")

# --------------------------------------------

# PREGUNTA A CONTESTAR: 
# ¿Cuál es la evolución del precio promedio de los productos  a lo largo del tiempo?

prom_producto <- precios %>% 
  group_by(yearMonth, producto) %>% 
  summarise(prom_precio = mean(precio)) 
  
prom_producto$yearMonth <- as.Date(paste(prom_producto$yearMonth,"01",sep="/"))

# grafico 1
ggplot(prom_producto, aes(x = yearMonth, y = prom_precio, color = producto)) +
  geom_point() +
  labs(x = "Fecha", y = "Precio promedio", color = "Producto") +
  theme_minimal() +
  scale_x_date(labels = date_format("%Y"))


# grafico 2
ggplot(data = prom_producto, aes(x = producto, y = prom_precio, fill = producto)) +
  geom_boxplot() +
  labs(x = "Producto", y = "Precio promedio", fill = "Producto") +
  theme_minimal()





