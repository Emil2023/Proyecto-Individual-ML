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

df['release_month'] = df['release_date'].dt.month_name()
df['release_year'] = df['release_year'].astype(str)

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    df['release_date'] = pd.to_datetime(df['release_date']')
    df_m = df['release_date'][df['release_date'].dt.strftime('%B').str.capitalize() == meses[str(mes).lower()]]
    cantidad = len(df_m)
    return {'mes': mes.lower(), 'cantidad': cantidad}


@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
    df['release_day'] = df['release_date'].dt.day_name()                                   
    df_dia = df[df['release_day'] == dia]
    cantidad = len(df_dia)
    return {'dia':dia, 'cantidad':cantidad}

@app.get("/franquicia/{franquicia}")
def franquicia(franquicia):
    df_franquicia = df[df['collection_name'] == franquicia]
    cantidad = len(df_franquicia)
    ganancia_total = df_franquicia['revenue'].sum()
    ganancia_promedio = df_franquicia['revenue'].mean()
    return {'franquicia':franquicia, 'cantidad':cantidad, 'ganancia_total':ganancia_total, 'ganancia_promedio':ganancia_promedio}

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais):
    df_pais = df[df['country'] == pais]
    cantidad = len(df_pais)
    return {'pais':pais, 'cantidad':cantidad}

@app.get("/productoras/{productora}")
def productoras(productora):
    df_productora = df[df['production_companies_names'].str.contains(productora)]
    cantidad = len(df_productora)
    ganancia_total = df_productora['revenue'].sum()
    return {'productora':productora, 'ganancia_total':ganancia_total, 'cantidad':cantidad}

@app.get("/retorno/{pelicula}")
def retorno(pelicula):
    df_pelicula = df[df['title'] == pelicula]
    inversion = df_pelicula['budget'].sum()
    ganancia = df_pelicula['revenue'].sum()-df_pelicula['budget'].sum()
    retorno = df_pelicula['return'].sum()
    anio = df_pelicula['release_year'].values[0]
    return {'pelicula':pelicula, 'inversion':inversion, 'ganacia':ganancia,'retorno':retorno, 'año':anio}
