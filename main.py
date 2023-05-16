from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import datetime as dt
import locale
import ast
import numpy as np
import time
import asyncio


#Funcion para el usario ingrese el mes y dia en español
app = FastAPI(
    title = "Bienvenido  a Los datos e informacion de la empresa sobre peliculas, series y productoras",
    description = "Datos",
    )

df = pd.read_csv('clean_movies_dataset.csv')
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_day'] = df['release_date'].dt.day_name()

def traductor_mes():
    meses = {
        "enero": "january",
        "febrero": "february",
        "marzo": "march",
        "abril": "april",
        "mayo": "may",
        "junio": "june",
        "julio": "july",
        "agosto": "august",
        "septiembre": "september",
        "octubre": "october",
        "noviembre": "november",
        "diciembre": "december"}
    
    df['release_month'] = df['release_month'].map(meses)
traductor_mes()
def traductor_dia():
    dias = {'Monday':'Lunes', 'Tuesday':'Martes', 'Wednesday':'Miercoles', 'Thursday':'Jueves', 'Friday':'Viernes', 'Saturday':'Sabado', 'Sunday':'Domingo'}
    df['release_day'] = df['release_day'].map(dias)
traductor_dia()

df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_year'] = df['release_year'].astype(str)

#se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes
@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    df_mes = df[df['release_month'] == mes]
    cantidad = len(df_mes)
    return {'mes':mes, 'cantidad':cantidad}

#Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia
@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
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
    pelis=df[['title','budget','revenue','return','release_year']].dropna()
    pelis['title']=pelis['title'].map(str.lower)
    pelis=pelis[pelis['title']==str(pelicula).lower()]
    inver=pelis['budget'].iloc[0]
    gan=pelis['revenue'].iloc[0]
    ret=pelis['return'].iloc[0]
    an=pelis['release_year'].iloc[0]
    return {'pelicula':pelicula, 'inversion':inver, 'ganacia':gan,'retorno':ret, 'anio':an}
 
#ML                                        
@app.get("/ml_movie/{pelicula}")
def ml_movie(selected_title):
    df = pd.read_csv('clean_movies_dataset.csv')
    print(df['title'].head())
    df['tagline'] = df['tagline'].fillna('')
   
    df = df.dropna(subset=['overview', 'tagline', 'genre_names', 'title', 'id'])

    generos_df = df['genre_names'].str.join(sep='|').str.get_dummies()
    
    selected_genres = df.loc[df['title'] == selected_title]['genre_names'].values
    if len(selected_genres) == 0:
        return "No se encontró la película " + selected_title
    selected_genres = ast.literal_eval(selected_genres[0])
    df['genre_similarity'] = df['genre_names'].apply(lambda x: len(set(selected_genres) & set(ast.literal_eval(x))) / len(set(selected_genres) | set(ast.literal_eval(x))))
   
    df['same_series'] = df['title'].apply(lambda x: 1 if selected_title.lower() in x.lower() else 0)

    features_df = pd.concat([generos_df, df['vote_average'], df['genre_similarity'], df['same_series']], axis=1)

    k = 6
    knn = NearestNeighbors(n_neighbors=k+1, algorithm='auto')
    knn.fit(features_df)
    indices = knn.kneighbors(features_df.loc[df['title'] == selected_title])[1].flatten()
    recommended_movies = list(df.iloc[indices]['title'])


    selected_score = df.loc[df['title'] == selected_title]['vote_average'].values[0]
    recommended_movies = sorted(recommended_movies, key=lambda x: (df.loc[df['title'] == x]['same_series'].values[0], df.loc[df['title'] == x]['vote_average'].values[0], df.loc[df['title'] == x]['genre_similarity'].values[0]), reverse=True)
    recommended_movies = [movie for movie in recommended_movies if movie != selected_title]

 
    if len(recommended_movies) == 0:
        return "No se encontraron películas similares a " + selected_title
    else:
        respuesta = f"Película seleccionada: {selected_title} ({selected_score}):\n\nPelículas Recomendadas:\n"
        for i, pelicula in enumerate(recommended_movies[:5]):
            score = df.loc[df['title'] == pelicula]['vote_average'].values[0]
            genres = df.loc[df['title'] == pelicula]['genre_names'].values[0]
            gen_str = ', '.join(ast.literal_eval(genres))

            respuesta += f"-{pelicula}  | Géneros: {gen_str} | Puntaje: {score} |\n"
            if i == 4:
                break
        return respuesta                 
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                        
