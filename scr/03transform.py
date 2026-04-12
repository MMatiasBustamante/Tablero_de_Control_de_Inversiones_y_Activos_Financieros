import numpy as np
import pandas as pd
from pathlib import Path

CarpetaData = Path("./data")

precios = pd.read_csv("../data/precios_limpios.csv", index_col="Date", parse_dates=True)
retornos = precios.pct_change().dropna()

print(retornos.head())

retornos_acumulados = (1 + retornos).cumprod() - 1
print(retornos_acumulados.tail()) #tail()muestra las ultimas 5 filas

volatilidad = retornos.std() * np.sqrt(252)
print("Volatilidad anual por activo:")
print(volatilidad.sort_values(ascending= False).round(4))

tasa_libre_riego = 0.05 # 5% anual, referencia bonos del tesoro USA

retorno_anual = retornos.mean() * 252
sharpe = (retorno_anual - tasa_libre_riego) / volatilidad

print("Sharpe Ratio por activo:")
print(sharpe.sort_values(ascending=False).round(4))

def max_drawdown(serie):
    acumulado = (1 + serie).cumprod()
    maximo_historico = acumulado.cummax()
    drawdown = (acumulado - maximo_historico) / maximo_historico
    return drawdown.min()

drawdown = retornos.apply(max_drawdown)

print("Drawdown maximo por activo:")
print(drawdown.sort_values().round(4))


metricas = pd.DataFrame({
    "volatilidad_anual": volatilidad,
    "retorno_anual":     retorno_anual,
    "sharpe_ratio":      sharpe,
    "max_drawdown":      drawdown,
}).round(4)

metricas.to_csv(CarpetaData / "metricas_riesgo.csv", decimal=",")
print(metricas)
print("metricas_riesgo.csv guardado correctamente")