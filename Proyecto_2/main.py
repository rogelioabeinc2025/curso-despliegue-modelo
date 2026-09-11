# para validar que el bundle esta cargado
from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
# Estructura de datos que recibimos y que regresamos desde el API
from pydantic import BaseModel, Field

#from Proyecto_2.inferencia import pronosticar
#from Proyecto_2.esquema import SolicitudPronostico

from inferencia import pronosticar
from esquema import SolicitudPronostico


#NOMBRE_BUNDLE = "Proyecto_2/modelo_demanda.joblib"
NOMBRE_BUNDLE = "modelo_demanda.joblib"
estado_servicio = {"bundle": None}

# decorador. Forma de dar un ciclo de vida a la funcion que definimos para nuestro proyecto
@asynccontextmanager
async def lifespan(app:FastAPI):
    estado_servicio["bundle"] = joblib.load(NOMBRE_BUNDLE)
    print("Bundle cargado correctamente")
    # yield se usa en ciclos y funciones,
    # hace una pausa y el API sigue activa, hasta que  bajamos el servidor 
    yield
    estado_servicio["bundle"]  = None

# inicializacion del API
app = FastAPI(
    title="API de Servicio de Pronostico de Demanda",
    description="Pronostico de Demanda para un Forecast",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def estado():
    return {
        "servicio": "API - Servicio de Pronostico de Demanda",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }

@app.post("/predecir")
# Antes de usar el diccionario, ahora usaremos el esquema definido en esquema.py
#def predecir(datos : dict):
def predecir(datos : SolicitudPronostico):
    #Antes de usuar SolicitudPronostico
    #store = datos["store"]
    #item = datos["item"]
    #horizonte = datos["horizonte"]
    #registros = datos["historial"]

    store = datos.store
    item = datos.item
    horizonte = datos.horizonte
    registros = datos.historial

    #Antes de usuar SolicitudPronostico
    #historial = pd.DataFrame(
        #{
        #    "date": pd.to_datetime([r["fecha"] for r in registros]),
        #    "store": store,
        #    "item": item,
        #    "sales": [r["unidades"] for r in registros]
        #}

    historial = pd.DataFrame(
        {
            "date": pd.to_datetime([r.fecha for r in registros]),
            "store": store,
            "item": item,
            "sales": [r.unidades for r in registros]
        }
    )

    bundle = estado_servicio["bundle"]

    pronostico = pronosticar(bundle, historial, horizonte)

    return{
        "store": store,
        "item": item,
        "pronostico": pronostico
    }

