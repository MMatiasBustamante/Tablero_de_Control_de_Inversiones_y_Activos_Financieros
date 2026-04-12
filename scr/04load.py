from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DB_URL)

with engine.connect() as conn:
    print("Conexión exitosa a PostgreSQL")

import pandas as pd
from pathlib import Path

DATA = Path("./data")

# Archivos a cargar y nombre de tabla en PostgreSQL
tablas = {
    "precios_limpios.csv":    "precios_limpios",
    "metricas_riesgo.csv":    "metricas_riesgo",
    "valor_portafolio.csv":   "valor_portafolio",
    "referencia_activos.csv": "referencia_activos",
}

for archivo, nombre_tabla in tablas.items():
    df = pd.read_csv(DATA / archivo, index_col=0, parse_dates=True, date_format="ISO8601")
    df.to_sql(nombre_tabla, engine, if_exists="replace", index=True)
    print(f"Tabla '{nombre_tabla}' cargada ({len(df)} filas)")