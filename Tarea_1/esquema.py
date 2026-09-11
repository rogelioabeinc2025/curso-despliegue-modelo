from pydantic import BaseModel, Field
from typing import Literal

class DataParaPronostico(BaseModel):
    antiguedad_meses: int = Field(ge=1, le=90, description='meses que lleva como cliente')
    gasto_mensual: float = Field(ge=5, le=50, description='su pago mensual')
    visitas_ultimo_mes: int = Field(ge=0, le=50, description='visitas en el ultimo mes')
    dias_desde_ultima_visita: int = Field(ge=0, le=100, description='dias desde su ultima visita')
    tickets_soporte: int = Field(ge=0, le=50, description='reclamos abiertos en el ultimo mes')
    plan: Literal['basico', 'estandar', 'premium'] = Field(..., description='tipo de plan contratado')
    metodo_pago: Literal['tarjeta','transferencia','efectivo'] = Field(..., description='Metodo de pago utilizado')
    descuento_activo: Literal[0,1] = Field(..., description='tiene un descuento aplicado (0=No, 1=Si)')