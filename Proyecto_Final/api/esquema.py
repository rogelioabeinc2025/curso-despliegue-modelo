from pydantic import BaseModel, Field

class Presupuesto(BaseModel):
    inversion_tv: float = Field(ge=1, le=1000, description='inversion en television')
    inversion_radio: float = Field(ge=1, le=500, description='inversion en radio')
    inversion_redes_sociales: float = Field(ge=1, le=1000, description='inversion en redes sociales')
    inversion_periodico: float = Field(ge=0, le=300, description='inversion en periodico')

class Prediccion(BaseModel):
    ventas: float = Field(description="ventas estimadas por el modelo")
