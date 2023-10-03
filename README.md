# Proyecto Individual  ML

## Introduccion
Este es un proyecto de recomendación de películas para una start-up que provee servicios de agregación de plataformas de streaming. Este proyecto implica la creación de un sistema de recomendación y una API para acceder a los datos de la empresa.Los datos han sido procesados y transformados para ser utilizados en el modelo de recomendación(ETL),
se llevo acabo un analisis exploratorio de los datos para examinar las relaciones entre las diferentes variables.

## Metas
- ***Transformacion***
Aplique los métodos de extracción, transformación y carga (ETL) para preparar y borrar el conjunto de Nulos y Desanidar Los Campos blongs_to_collection, production_companies y otros.

- Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

- Los valores nulos del campo release date deben eliminarse.

- De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

- Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.
  
- Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,vote_count,poster_path y homepage.


- ***Analisis Exploratorio***
Realice un análisis de investigación de datos (EDA) para obtener información sobre películas, como el encabezado, la descripción general y los géneros.
Realice un Grafico de valores faltantes,Saque el porcentaje de valores faltantes y Pude observar mas a fondo el dataframe. Todo esto fue posible con python,pandas y matplotlib
![](https://www.addkw.com/wp-content/uploads/2018/11/Etapas-del-analisis-de-datos.png)



- ***Desarrollo de la API***
Diseñe e implemente una serie de funciones y API integradas sin ningún problema con el sistema recomendado basado en el contenido,Verificando que este Disponible para el cliente.
Link De la API: emilioo-project.onrender.com/docs
- ***Deployment***
Para lograr el deploy tuve que usar render y subirlo para que pueda ser utilizada por la web

## Librerias Utilizadas
- Pandas
- Fastapi
- Render
- Numpy
- Scikit-Learn



