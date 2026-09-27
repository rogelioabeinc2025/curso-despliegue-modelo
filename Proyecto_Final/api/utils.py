import joblib
import pandas as pd

def cargar_modelo(path_model):
    return joblib.load(path_model)

def predecir_ventas(presupuesto: dict, modelo, bundle: dict) -> dict:
    X_nuevo = pd.DataFrame([presupuesto])[bundle["columnas"]]
    prediccion = modelo.predict(X_nuevo)
    return {"ventas": float(prediccion[0])}