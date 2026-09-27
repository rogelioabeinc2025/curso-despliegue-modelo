# para validar que el bundle esta cargado
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from api.esquema import Prediccion, Presupuesto
from api.utils import cargar_modelo, predecir_ventas

NOMBRE_BUNDLE = "models/modelo_bundle_medios.pkl"
estado_servicio = {"bundle": None}

@asynccontextmanager
async def lifespan(app:FastAPI):
    estado_servicio["bundle"] = cargar_modelo(NOMBRE_BUNDLE) 
    print("Bundle cargado correctamente")
    # yield se usa en ciclos y funciones,
    # hace una pausa y el API sigue activa, hasta que  bajamos el servidor 
    yield
    estado_servicio["bundle"]  = None

# inicializacion del API
app = FastAPI(
    title="API de Prediccion de Ventas",
    description="Recibe datos de presupuesto por Medio de Publicidad y Predice las ventas",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def estado():
    return {
        "servicio":"API de prediccion de Ventas segun presupuesto a medios",
        "modelo_cargado": estado_servicio["bundle"] is not None        
    }

@app.post("/predecir", response_model=Prediccion)
def predecir(presupuesto: Presupuesto):
    #validar el modelo
    bundle = estado_servicio["bundle"]
    if bundle is None:
        raise HTTPException(status_code=503, detail="El modelo aun no esta cargado")
    fila = presupuesto.model_dump()    #genera un diccionario

    resultado = predecir_ventas(fila, bundle['modelo_ventas'], bundle)
    return resultado

    
    

