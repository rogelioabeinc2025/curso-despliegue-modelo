from fastapi import FastAPI

app = FastAPI(title='Mi Primer API')

@app.get("/")
def root():
    return {"message":"Mi primer API esta funcionando"}

@app.get("/saludo/{nombre}")
def saludo(nombre):
    return{'saludo':f"Hola {nombre}, como estas ?"}
