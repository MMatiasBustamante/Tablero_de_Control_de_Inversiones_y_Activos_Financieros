import yfinance as yf
import pandas as pd
from pathlib import Path

FechaInicio = "2020-01-01"
FechaFin = "2026-01-01"
CarpetaData = Path("./data")

ACTIVOS = {
    "ETFs": {
        "SPY":  "SPDR S&P 500 ETF",
        "QQQ":  "Invesco Nasdaq-100 ETF",
        "DIA":  "SPDR Dow Jones ETF",
        "EEM":  "iShares Mercados Emergentes ETF",
    },
    "Acciones_USA": {
        "AAPL":  "Apple",
        "MSFT":  "Microsoft",
        "GOOGL": "Alphabet (Google)",
        "AMZN":  "Amazon",
        "NVDA":  "NVIDIA",
    },
    "Acciones_ARG": {
        # Acciones argentinas que cotizan en NYSE como ADRs
        "GGAL": "Grupo Financiero Galicia",
        "YPF":  "YPF S.A.",
        "PAM":  "Pampa Energía",
        "BBAR": "BBVA Argentina",
        "BMA": "Banco Macro"
    }
}
PORTAFOLIO = {
    "SPY":   5,
    "QQQ":   8,
    "DIA":   4,
    "EEM":  15,
    "AAPL": 10,
    "MSFT":  7,
    "GOOGL": 3,
    "AMZN":  4,
    "NVDA":  6,
    "GGAL": 50,
    "YPF":  30,
    "PAM":  25,
    "BMA":  20,
    "BBAR": 40,
}

def descargar_precios(tickers: list, inicio: str, fin: str) -> pd.DataFrame:
    print(f"Descargando {tickers}...")
    df = yf.download(tickers, start = inicio, end = fin, auto_adjust = True, progress = False)
    return df["Close"]

def guardar_csv(df: pd.DataFrame, nombre: str):
    route = CarpetaData / nombre
    df.to_csv(route)
    print(f"Csv Guardado: {route} ({df.shape[0]} fila x {df.shape[1]} columnas)")

def construir_portafolio(precios: pd.DataFrame, portafolio: dict) -> pd.DataFrame:
    """
    Estilo de tabla
    - precio de cierre por activo
    - valor de posición (precio x cantidad)
    - valor total del portafolio por día
    """
    cantidades = pd.Series(portafolio)
    valor_posiciones = precios.multiply(cantidades, axis="columns")
    valor_posiciones["Total_portafolio"] = valor_posiciones.sum(axis=1)
    return valor_posiciones

def main():
    CarpetaData.mkdir(exist_ok=True)

    todosLosTickers= [t for grupo in ACTIVOS.values() for t in grupo]

    print("\n1. Descargando precios historiocos...")
    precios = descargar_precios(todosLosTickers, FechaInicio, FechaFin)

    print("\n2.Guardando archivos por categoria...")
    for categoria, activos in ACTIVOS.items():
        tickers = list(activos.keys())
        df_categoria = precios[tickers].dropna(how = "all")
        guardar_csv(df_categoria, f"precios_{categoria.lower()}.csv")

    print("\n3. Guardando precios completos...")
    guardar_csv(precios, "precios_todos.csv")

    print("\n4. Construccion de tabla de valor del portafolio...")
    preciosLimpios = precios.dropna()
    df_portafolio = construir_portafolio(preciosLimpios, PORTAFOLIO)
    guardar_csv(df_portafolio, "valor_portafolio.csv")

    print("\n5. Generando tabla de referencia de activos...")
    filas = []
    for categoria, activos in ACTIVOS.items():
        for ticker, nombre in activos.items():
            filas.append({
                "ticker":    ticker,
                "nombre":    nombre,
                "categoria": categoria,
                "cantidad":  PORTAFOLIO.get(ticker, 0),
                })
            
    df_referencia = pd.DataFrame(filas)
    guardar_csv(df_referencia, "referencia_activos.csv")

    print("\n Descarga completa. Archivos generados en /data:")
    for archivo in sorted(CarpetaData.glob("*.csv")):
        print(f"   - {archivo.name}")
 
 
if __name__ == "__main__":
    main()