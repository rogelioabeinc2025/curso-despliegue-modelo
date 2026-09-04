# para validar que el bundle esta cargado
from contextlib import asynccontextmanager
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
# Estructura de datos que recibimos y que regresamos desde el API
from pydantic import BaseModel, Field

#NOMBRE_BUNDLE = "Proyecto_1/modelo_bundle_e_cardiaca.pkl"
#Para su despliegue quitamos Proyecto_1/
NOMBRE_BUNDLE = "modelo_bundle_e_cardiaca.pkl"
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
    title="API de Prediccion de Enfermedad Cardiaca",
    description="Recibe datos clinicos de Paciente y Predice el riesto de cardiopatica coronaria",
    version="1.0.0",
    lifespan=lifespan
)

# Estructura de datos para la entrada de datos
class PacienteInput(BaseModel):
    # validaciones de los datos de entrada
    sbp: int = Field(...,description="Presion Arterial Sistolica"),
    Tabaco: float = Field(...,description="Tabaco acumulado (kgs)"),
    ldl: float = Field(..., description="Colesterol LDL"),
    Adiposidad: float = Field(...,description="Adiposidad"),
    Familia: Literal['Presente','Ausente'] = Field(..., description="Antecedentes Familidares de Enermedad Cardiaca"),
    Tipo: int = Field(...,description="Comportamiento Tipo-A"), 
    Obesidad: float = Field(...,description="Obesidad"),
    Alcohol: float = Field(...,description="Consumo actual de Alcohol"),
    Edad: int = Field(...,description="Edad")

# Estructura de datos para la salida de datos
# BaseModel nos permite hacer validaciones de los datos de entrada contra lo definido en la clase
class PacienteOutput(BaseModel):
    chd_predicho: int
    probabilidad: float
    riesgo: str

@app.get("/")
def estado():
    # siempre retornamos un diccionario
    return {
        "servicio":"API de prediccion de enfermedad cardiaca",
        "modelo_cargado": estado_servicio["bundle"] is not None        
    }

#endpoint para predecir
# POST enviamos datos y recibimos una respuesta
# GET enviamos filtros para una consulta
@app.post("/predecir", response_model = PacienteOutput)
def predecir(paciente: PacienteInput):
    #validar el modelo
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="El modelo aun no esta cargado")
    fila = paciente.model_dump()    #genera un diccionario

    fila["Familia"] = bundle["mapeo_familia"][fila["Familia"]]
    X_nuevo = pd.DataFrame([fila])[bundle['columnas']]

    prediccion = bundle["pipeline"].predict(X_nuevo)[0]
    probabilidad = bundle["pipeline"].predict_proba(X_nuevo)[0,1]

    #Devolver resultado
    return PacienteOutput(
        chd_predicho = prediccion,
        probabilidad= round(probabilidad,4),
        riesgo = "alto" if prediccion ==1 else "bajo"
    )
    

