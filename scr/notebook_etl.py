import pandas as pd 
import numpy as np
from pathlib import Path

CarpetaData = Path("./data")

precios = pd.read_csv(CarpetaData/"precios_todos.csv", index_col="Date", parse_dates=True)

print(precios.shape)
print(precios.head())

print(precios.info())
print("Valores nulos por activo:")
print(precios.isnull().sum())

precios = precios.dropna(how="all")
print(f"Filas despues de limpieza: {len(precios)}")

precios= precios.ffill()
print("Valores Nulos restante:")
print(precios.isnull().sum())

precios.to_csv(CarpetaData/"precios_limpios.csv")
print("precios_limpios.csv guardado correctamente")