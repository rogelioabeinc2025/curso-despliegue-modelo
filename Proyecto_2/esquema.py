# El esquema es la estructura de como debemos ingresar la informacion
from pydantic import BaseModel, Field
from datetime import date

class RegistroHistorico(BaseModel):
    fecha: date

    unidades: float = Field(ge=0, description='Unidades vendidas ese dia')


class SolicitudPronostico(BaseModel):
    store: int = Field(ge=1, le=10, description='El numero de tiendas, del 1 al 10')

    item: int = Field(ge=1, le=50, description='El numero de producto, del 1 al 50')

    historial: list[RegistroHistorico] = Field(min_length=28, max_length=365, description='Historico reciente de la serie. Minimo 28 registros')

    horizonte: int = Field(default=14, ge=1, le=28, description='Dias a pronosticar de 1 - 28')



