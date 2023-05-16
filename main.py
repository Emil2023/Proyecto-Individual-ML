from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pandas as pd
import datetime as dt
import locale
import ast
import numpy as np

app = FastAPI()

meses_esp = {
    'January': 'enero',
    'February': 'febrero',
    'March': 'marzo',
    'April': 'abril',
    'May': 'mayo',
    'June': 'junio',
    'July': 'julio',
    'August': 'agosto',
    'September': 'septiembre',
    'October': 'octubre',
    'November': 'noviembre',
    'December': 'diciembre'
}

dias_semana = {
    'Monday': 'Lunes',
    'Tuesday': 'Martes',
    'Wednesday': 'Miércoles',
    'Thursday': 'Jueves',
    'Friday': 'Viernes',
    'Saturday': 'Sábado',
    'Sunday': 'Domingo'
}

df=pd.read_csv(r"C:\Users\WINDOW 10\Desktop\Labs\Datasets\clean_movies_dataset.csv")

df['release_date'] = pd.to_datetime(df['release_date'])
df['release_month'] = df['release_date'].dt.month_name()
df['release_day'] = df['release_date'].dt.day_name()
df['release_year'] = df['release_year'].astype(str)

@app.get("/peliculas_mes/{mes}")
def peliculas_mes(mes):
    fechas=pd.to_datetime(df['release_date'],format='%Y-%m-%d')
    nmes=fechas[fechas.dt.month_name(locale='es_CO')==mes.capitalize()]
    respuesta=nmes.shape[0]
    return {'mes':mes, 'cantidad':respuesta}


@app.get("/peliculas_dia/{dia}")
def peliculas_dia(dia):
    fechas=pd.to_datetime(df['release_date'],format='%Y-%m-%d')
    ndia=fechas[fechas.dt.day_name(locale='es_CO')==dia.capitalize()]
    respuesta=ndia.shape[0]
    return {'dia':dia, 'cantidad':respuesta}

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