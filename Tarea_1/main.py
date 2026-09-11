# main.py para Tarea_1
from contextlib import asynccontextmanager
#from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

# Estructura de datos que recibimos y que regresamos desde el API
from pydantic import BaseModel, Field

#from Proyecto_2.inferencia import pronosticar
from Tarea_1.esquema import DataParaPronostico

NOMBRE_BUNDLE = "Tarea_1/modelo_churn.pkl"
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
    title="API de Servicio de Prevenir Cancelacion de Suscripciones",
    description="Pronostico de Cancelacion de Suscripciones para un Forecast",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def estado():
    return {
        "servicio": "API - Servicio de Pronostico de Demanda",
        "modelo_cargado": estado_servicio["bundle"] is not None
    }

@app.post("/predecir", summary='Evalua cancelacion de suscripcion del cliente')
# Ahora usaremos el esquema definido en esquema.py
def predecir(datos : DataParaPronostico):
    antiguedad_meses = datos.antiguedad_meses
    gasto_mensual = datos.gasto_mensual
    visitas_ultimo_mes = datos.visitas_ultimo_mes
    dias_desde_ultima_visita = datos.dias_desde_ultima_visita
    tickets_soporte = datos.tickets_soporte
    plan = datos.plan
    metodo_pago = datos.metodo_pago
    descuento_activo = datos.descuento_activo

    fila = {
        "antiguedad_meses": antiguedad_meses,
        "gasto_mensual": gasto_mensual,
        "visitas_ultimo_mes": visitas_ultimo_mes,
        "dias_desde_ultima_visita": dias_desde_ultima_visita,
        "tickets_soporte": tickets_soporte,
        "descuento_activo": descuento_activo,
        "plan": plan,
        "metodo_pago": metodo_pago        
        }

    bundle = estado_servicio["bundle"]
    umbral = bundle["umbral"]

    cliente_nuevo = pd.DataFrame([fila])[bundle['columnas']]
 
    probabilidad = bundle["pipeline"].predict_proba(cliente_nuevo)[0, 1]

    nivel_riesgo= ''
    if probabilidad < umbral:
        nivel_riesgo = "Bajo"
        #dictamen = "Cliente Estable. Mantener comunicación estándar."
        #alerta_cancelacion = 0
    elif umbral <= probabilidad < 0.50:
        nivel_riesgo = "Medio"
        #dictamen = "Riesgo Moderado. Enviar campaña preventiva o encuesta."
        #alerta_cancelacion = 1  # Ya superó el umbral mínimo de seguridad del 81% de Recall
    else: # >= 0.50
        nivel_riesgo = "Alto"
        #dictamen = "Riesgo Inminente (Certeza >82%). Aplicar protocolo de retención."
        #alerta_cancelacion = 1

    cancelo_predicho = 1 if probabilidad >= umbral else 0
    prediccion = "Cancela suscripcion" if cancelo_predicho == 1 else "Continua con suscripcion"

    return{
 "analisis_churn": {
            "probabilidad_cancelacion": round(float(probabilidad), 4),
            "prediccion": prediccion,
            "nivel_riesto": nivel_riesgo,            
            "configuracion_umbrales": {
                "umbral_deteccion_temprana": umbral,
                "umbral_alta_certeza": 0.50
            }
        }
    }

