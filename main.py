from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import datetime as dt
import locale
import ast
import numpy as np

app = FastAPI()

#Diccionario para el usario ingrese el mes y dia en español
dias = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miércoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sábado': 'Saturday',
        'domingo': 'Sunday'
    }

meses = {
        'enero': 'January',
        'febrero': 'February',
        'marzo': 'March',
        'abril': 'April',
        'mayo': 'May',
        'junio': 'June',
        'julio': 'July',
        'agosto': 'August',
        'septiembre': 'September',
        'octubre': 'October',
        'noviembre': 'November',
        'diciembre': 'December'
    }

#Cargamos nuestro dataset limpio
df=pd.read_csv("clean_movies_dataset.csv")
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_year'] = df['release_year'].astype(str)

#'Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes
@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    df['release_date'] = pd.to_datetime(df['release_date'], format='%Y-%m-%d')
    df_mes = df['release_date'][df['release_date'].dt.strftime('%B').str.capitalize() == meses[str(mes).lower()]]
    cantidad = len(df_mes)
    return {'mes': mes.lower(), 'cantidad': cantidad}

#Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
    df['release_day'] = df['release_date'].dt.day_name()                                   
    df_dia = df[df['release_day'] == dia]
    cantidad = len(df_dia)
    return {'dia':dia, 'cantidad':cantidad}
                                        
#Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio
@app.get("/franquicia/{franquicia}")
def franquicia(franquicia):
    df_franquicia = df[df['collection_name'] == franquicia]
    cantidad = len(df_franquicia)
    ganancia_total = df_franquicia['revenue'].sum()
    ganancia_promedio = df_franquicia['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}    
                                                                                                                       
#Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais):
    df_pais = df[df['country'] == pais]
    cantidad = len(df_pais)
    return {'pais':pais, 'cantidad':cantidad}
#Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron
@app.get("/productoras/{productora}")
def productoras(productora):
    df_productora = df[df['production_companies_names'].str.contains(productora)]
    cantidad = len(df_productora)
    ganancia_total = df_productora['revenue'].sum()
    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad}
                                        
#Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo
@app.get("/retorno/{pelicula}")
def retorno(pelicula):
    df_pelicula = df[df['title'] == pelicula]
    inversion = df_pelicula['budget'].sum()
    ganancia = df_pelicula['revenue'].sum()-df_pelicula['budget'].sum()
    retorno = df_pelicula['return'].sum()
    anio = df_pelicula['release_year'].values[0]
    return {'pelicula':pelicula, 'inversion':inversion, 'ganacia':ganancia,'retorno':retorno, 'año':anio}
 
#ML                                        
@app.get("/peliculas_recomendadas/{pelicula}")
def ml_movie(selected_title):
    df = pd.read_csv('clean_movies_dataset.csv') 
    k = 6
    generos_df = pd.read_csv('genre_binario.csv', index_col=0).astype('float32')

    selected_genres = df.loc[df['title'] == selected_title]['genre_names'].values[0]
    df['genre_similarity'] = df['genre_names'].apply(lambda x: len(set(selected_genres) & set(x)) / len(set(selected_genres) | set(x)))
    df['same_series'] = df['title'].apply(lambda x: 1 if 'Batman' in x else 0)
    features_df = pd.concat([generos_df, df['vote_average'], df['genre_similarity'], df['same_series']], axis=1)
    knn = NearestNeighbors(n_neighbors=k+1, algorithm='auto')
    knn.fit(features_df)
    indices = knn.kneighbors(features_df.loc[df['title'] == selected_title])[1].flatten()
    movies = list(df.iloc[indices]['title'])
    movies = sorted(movies, key=lambda x: (df.loc[df['title'] == x]['same_series'].values[0], df.loc[df['title'] == x]['vote_average'].values[0], df.loc[df['title'] == x]['genre_similarity'].values[0]), reverse=True)
    movies = [movie for movie in movies if movie != selected_title]
    return movies[0:5]                                      
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
