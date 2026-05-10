# Análisis de Riesgo y Eficiencia de Portafolios de Inversión

> ¿Cómo puede un analista evaluar la eficiencia riesgo/retorno de un portafolio diversificado para identificar activos que destruyen valor y generar criterios de rebalanceo basados en datos?

---

## 📌 Contexto y problema de negocio

Uno de los principales desafíos en la gestión de inversiones —tanto para usuarios individuales como para plataformas fintech— es distinguir qué activos dentro de un portafolio realmente aportan retorno ajustado al riesgo y cuáles lo deterioran sin que el inversor lo note.

El problema no es la falta de datos: los precios históricos son públicos y accesibles. El problema es la falta de un sistema que los procese, calcule métricas de riesgo estándar de la industria y los presente de forma que habiliten decisiones concretas: **¿qué activo conviene mantener, cuál rebalancear y cuál salir?**

Este proyecto construye ese sistema de principio a fin: desde la extracción automatizada de datos históricos hasta un dashboard interactivo que responde esas preguntas para un portafolio de 14 activos financieros (ETFs americanos, acciones de EE.UU. y acciones argentinas).

---

## 💡 Principales hallazgos

El análisis revela tres patrones accionables sobre el portafolio:

1. **Eficiencia riesgo/retorno desigual**: el gráfico Sharpe vs. Volatilidad (Página 3) permite identificar rápidamente qué activos ofrecen buen retorno ajustado al riesgo y cuáles asumen alta volatilidad con bajo retorno —los candidatos prioritarios a revisión o salida.

2. **Exposición asimétrica por mercado**: los activos argentinos (GGAL, YPF, PAM, BBAR, BMA) muestran patrones de volatilidad y drawdown notablemente distintos a los activos estadounidenses, lo que refleja el riesgo sistémico del mercado local y su impacto en la composición del portafolio.

3. **Maximum Drawdown como señal de alerta**: algunos activos presentan caídas históricas desde su pico que superan umbrales razonables de tolerancia al riesgo, lo que justifica una política automática de alerta o rebalanceo.

> **Decisión que habilita este análisis**: un equipo de producto o de inversiones podría usar estas métricas para definir reglas automáticas de alerta —por ejemplo, notificar a un usuario cuando un activo cae por debajo de un Sharpe mínimo o supera un umbral de drawdown— mejorando la retención y la confianza en la plataforma.

---

## 📊 Dashboard — Power BI

El dashboard está dividido en cuatro páginas, cada una orientada a responder una pregunta de negocio específica.

### Página 1 — Resumen del portafolio

Vista ejecutiva del portafolio. Muestra el valor total, el activo con mejor Sharpe Ratio, el de mayor retorno anual y el de peor drawdown. Diseñada para una lectura rápida del estado general: **¿el portafolio está funcionando bien en términos agregados?**

> 📷 ![Página 1](img/pagina1.png)

### Página 2 — Análisis por activo

Comparación detallada entre activos. Incluye un gráfico de barras con el retorno anual por ticker, una tabla completa con todas las métricas y un segmentador para filtrar por categoría (ETFs, acciones USA, acciones ARG). Responde: **¿qué activos lideran el retorno y cuáles quedan rezagados?**

> 📷 ![Página 2](img/Pagina2.png)

### Página 3 — Análisis de riesgo

La página central del análisis estratégico. El gráfico de dispersión Sharpe vs. Volatilidad permite identificar los activos más eficientes: los ubicados arriba a la izquierda tienen buen retorno ajustado al riesgo con baja volatilidad; los ubicados abajo a la derecha asumen mucho riesgo con poco retorno. Complementado con un gráfico de barras de Maximum Drawdown por activo. Responde: **¿qué activos conviene mantener y cuáles representan riesgo injustificado?**

> 📷 ![Página 3](img/pagina3.png)

### Página 4 — Evolución histórica

Gráfico de líneas con los precios históricos, filtrable por ticker. Permite analizar el comportamiento de cada activo a lo largo del tiempo y detectar patrones de recuperación tras caídas. Responde: **¿cómo reaccionó cada activo ante distintos contextos de mercado?**

> 📷 ![Página 4](img/pagina4.png)

---

## 🗂️ Estructura del proyecto

```
├── data/               # Datos crudos y procesados (.csv)
├── notebooks/          # Jupyter Notebooks (ETL y EDA)
├── scr/                # Scripts Python del pipeline
│   ├── 01_descarga_de_datos.py
│   ├── 02_notebook_etl.py
│   ├── 03_transform.py
│   └── 04_load.py
├── sql/                # Schema y queries analíticas
├── powerbi/            # Archivo .pbix del dashboard
├── img/                # Capturas del dashboard
└── README.md
```

---

## ⚙️ Pipeline de datos

El proyecto corre en cuatro scripts secuenciales que cubren el ciclo completo de datos: extracción, limpieza, transformación y carga.

### `01_descarga_de_datos.py`
Conecta a la API de yfinance y descarga los precios históricos de los 14 activos. Construye la tabla del portafolio con la composición de activos y genera la tabla de referencia con la categoría de cada ticker (ETF, acción USA, acción ARG). Guarda los resultados en archivos CSV en la carpeta `/data`.

### `02_notebook_etl.py`
Limpieza y normalización de los datos crudos. Maneja valores faltantes, verifica la consistencia de fechas y genera el archivo `precios_limpios.csv` listo para el análisis.

### `03_transform.py`
Calcula las métricas de riesgo a partir de los precios limpios:

| Métrica | Definición |
|---|---|
| Retorno anual | Retorno diario promedio × 252 días hábiles |
| Volatilidad anual | Desvío estándar de retornos diarios × √252 |
| Sharpe Ratio | Retorno ajustado al riesgo (tasa libre de riesgo: 5%) |
| Maximum Drawdown | Máxima caída porcentual desde el pico histórico |

Guarda los resultados en `metricas_riesgo.csv`.

### `04_load.py`
Carga todas las tablas CSV a PostgreSQL usando SQLAlchemy. Reemplaza las tablas existentes en cada ejecución para mantener los datos actualizados.

---

## 🛠️ Stack utilizado

| Herramienta | Rol en el proyecto |
|---|---|
| Python (Pandas, NumPy) | Extracción, limpieza y cálculo de métricas de riesgo |
| yfinance | API para descarga de precios históricos |
| PostgreSQL | Almacenamiento estructurado y consultas analíticas |
| SQLAlchemy | Conexión entre Python y PostgreSQL |
| Power BI | Dashboard interactivo final |

---

## 📈 Activos analizados

| Ticker | Tipo | Mercado |
|--------|------|---------|
| SPY | ETF | USA |
| QQQ | ETF | USA |
| DIA | ETF | USA |
| EEM | ETF | USA |
| AAPL | Acción | USA |
| MSFT | Acción | USA |
| GOOGL | Acción | USA |
| AMZN | Acción | USA |
| NVDA | Acción | USA |
| GGAL | Acción | ARG |
| YPF | Acción | ARG |
| PAM | Acción | ARG |
| BBAR | Acción | ARG |
| BMA | Acción | ARG |

---

## 🚀 Cómo ejecutar el proyecto

### Requisitos

- Python 3.10+
- PostgreSQL
- Power BI Desktop

### Instalación

```bash
git clone https://github.com/MMatiasBustamante/Proyecto-Tablero-de-Control-de-Inversiones-y-Activos-Financieros
cd Proyecto-Tablero-de-Control-de-Inversiones-y-Activos-Financieros
pip install -r requirements.txt
```

### Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_base
```

### Ejecutar el pipeline

```bash
python scr/01_descarga_de_datos.py
python scr/02_notebook_etl.py
python scr/03_transform.py
python scr/04_load.py
```

Luego abrir el archivo `powerbi/tablero.pbix` y actualizar los datos desde Power BI Desktop.

---

## 👤 Autor

Desarrollado por **Matías Bustamante**  
Analista de Datos | Estudiante de Programación  
Diplomatura en Gestión y Análisis de Datos — UBA

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Conectar-blue)](https://www.linkedin.com/in/matias-bustamante-252307266/)
[![GitHub](https://img.shields.io/badge/GitHub-Perfil-black)](https://github.com/MMatiasBustamante)
