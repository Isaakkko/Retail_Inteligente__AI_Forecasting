# Retail Inteligente — AI Forecasting

Proyecto de Big Data, análisis de datos y Machine Learning orientado al análisis y clasificación de la demanda en el sector retail.

## Institución

**Colegio Universitario de Cartago — Costa Rica**

## Integrantes

* Isaac Ulloa Calvo
* Jeffrey Jiménez Cordero

---

## Descripción del Proyecto

Retail Inteligente es un proyecto orientado al análisis de información de ventas, inventario y demanda dentro del sector retail.

El proyecto integra diferentes conceptos de Big Data, ingeniería de datos y Machine Learning mediante un flujo dividido en siete fases progresivas.

Durante el desarrollo se implementan procesos de planificación, almacenamiento de datos, análisis exploratorio, construcción de un Data Warehouse, consultas analíticas, procesamiento mediante MapReduce y un modelo de clasificación de demanda.

El objetivo principal es transformar información histórica de ventas e inventario en resultados que permitan analizar el comportamiento de la demanda y apoyar la toma de decisiones relacionadas con inventario, pedidos y estrategias comerciales.

---

## Descripción del Dataset

El proyecto utiliza el **Retail Store Inventory Forecasting Dataset**.

El conjunto de datos contiene aproximadamente 73 000 registros relacionados con ventas, inventario, precios y diferentes condiciones comerciales.

### Variables principales

| Variable             | Descripción                      |
| -------------------- | -------------------------------- |
| `Date`               | Fecha del registro               |
| `Store ID`           | Identificador de la tienda       |
| `Product ID`         | Identificador del producto       |
| `Category`           | Categoría del producto           |
| `Region`             | Región geográfica                |
| `Inventory Level`    | Nivel de inventario              |
| `Units Sold`         | Unidades vendidas                |
| `Units Ordered`      | Unidades solicitadas             |
| `Demand Forecast`    | Pronóstico de demanda            |
| `Price`              | Precio del producto              |
| `Discount`           | Descuento aplicado               |
| `Weather Condition`  | Condición climática              |
| `Holiday/Promotion`  | Indicador de festivo o promoción |
| `Competitor Pricing` | Precio de la competencia         |
| `Seasonality`        | Temporada del año                |

---

## Flujo General del Proyecto

```text
Dataset Retail
      ↓
Planificación del proyecto
      ↓
Data Warehouse
      ↓
Análisis exploratorio
      ↓
Vistas analíticas
      ↓
Procesamiento MapReduce
      ↓
Clasificación de demanda
      ↓
Evaluación y almacenamiento del modelo
```

---

## Fases del Proyecto

### Fase 1 — Planificación

Se define el alcance general del proyecto, los objetivos y los requerimientos relacionados con el análisis de información retail.

Esta fase establece la base para el desarrollo de las siguientes etapas.

### Fase 2 — Data Warehouse

Se diseña una arquitectura de almacenamiento basada en un esquema estrella utilizando SQL Server.

El modelo permite organizar la información de ventas e inventario mediante una tabla de hechos y diferentes dimensiones.

### Fase 3 — Análisis Exploratorio de Datos

Se realiza un análisis exploratorio del dataset utilizando Python y Jupyter Notebook.

El análisis permite estudiar:

* Distribución de las variables.
* Comportamiento de las ventas.
* Niveles de inventario.
* Relación entre precios y ventas.
* Comportamiento de las categorías.
* Variables comerciales relacionadas con la demanda.

El notebook principal se encuentra en:

`Fases/Fase3ProyectoBigData/EDA.ipynb`

### Fase 4 — Vistas Analíticas

Se desarrollan vistas SQL orientadas al análisis de negocio.

Entre las vistas implementadas se encuentran:

* Ventas por mes.
* Ventas por categoría.
* Ventas por región.
* Ventas según condiciones climáticas.
* Comparación entre demanda estimada y ventas reales.

Estas vistas permiten simplificar las consultas sobre el Data Warehouse.

### Fase 5 — Procesamiento de Información

Esta fase estudia el procesamiento y consulta de información relacionada con las operaciones retail.

Se utilizan los datos almacenados para analizar el comportamiento de ventas e inventario.

### Fase 6 — MapReduce

Se implementa el patrón:

`Map → Shuffle → Reduce`

mediante Python.

El proceso analiza las ventas utilizando la siguiente operación:

`Monto de Venta = Units Sold × Price`

### Etapa Map

Se generan pares clave-valor para:

* Región y monto de venta.
* Categoría y monto de venta.

### Etapa Shuffle

Los valores se agrupan utilizando la región o categoría como clave.

### Etapa Reduce

Los montos agrupados se suman para calcular:

* Ventas totales por región.
* Ventas totales por categoría.

El script utilizado es:

`Fases/Fase6ProyectoBigData/map_reduce_ventas.py`

Los resultados se almacenan en:

```text
RESULTADOS/MAP_REDUCE/
├── ventas_por_region.csv
└── ventas_por_categoria.csv
```

---

## Fase 7 — Clasificación de Demanda

La fase final implementa un modelo de Machine Learning utilizando **Regresión Logística**.

El objetivo es clasificar los registros en:

* Demanda normal.
* Alta demanda.

### Creación de la variable objetivo

La variable `alta_demanda` se genera utilizando las unidades vendidas.

Se calcula la mediana de:

`Units Sold`

Los registros superiores al umbral se clasifican como alta demanda.

```text
Units Sold > Mediana → Alta demanda
Units Sold <= Mediana → Demanda normal
```

La mediana permite reducir el impacto de valores extremos y obtener una separación más equilibrada entre las clases.

### Variables utilizadas por el modelo

El modelo utiliza:

* `Price`
* `Units Ordered`
* `Inventory Level`
* `Discount`
* `Holiday/Promotion`
* `Competitor Pricing`

### División de datos

El conjunto de datos se divide en:

* 80 % para entrenamiento.
* 20 % para prueba.

La división utiliza estratificación para conservar la distribución de las clases.

### Pipeline de Machine Learning

El modelo utiliza un pipeline que integra:

```text
Datos
  ↓
Imputación de valores faltantes
  ↓
StandardScaler
  ↓
Regresión Logística
  ↓
Clasificación de demanda
```

Los valores faltantes se reemplazan mediante la mediana.

Posteriormente, `StandardScaler` transforma las variables para mantener escalas comparables.

Finalmente, se utiliza `LogisticRegression` para realizar la clasificación.

### Evaluación del Modelo

El modelo se evalúa utilizando datos que no fueron utilizados durante el entrenamiento.

Las métricas utilizadas incluyen:

* Accuracy.
* Matriz de confusión.
* Precision.
* Recall.
* F1-score.

Esto permite obtener una evaluación más representativa del rendimiento del clasificador.

El resultado exacto puede variar según el conjunto de prueba utilizado y los datos disponibles.

### Persistencia del Modelo

El modelo entrenado se guarda utilizando `joblib`.

El archivo generado es:

`MODELOS/modelo_clasificacion_demanda.joblib`

El artefacto almacena:

* Pipeline de preprocesamiento.
* Modelo de Regresión Logística.
* Variables utilizadas.
* Umbral de alta demanda.
* Etiquetas de clasificación.

Esto permite reutilizar el modelo sin realizar nuevamente todo el entrenamiento.

---

## Estructura del Proyecto

```text
Retail_Inteligente__AI_Forecasting/
│
├── DATA/
│   └── retail_store_inventory.csv
│
├── Fases/
│   ├── Fase1ProyectoBigData/
│   ├── Fase2ProyectoBigData/
│   ├── Fase3ProyectoBigData/
│   │   └── EDA.ipynb
│   │
│   ├── Fase4ProyectoBigData/
│   ├── Fase5ProyectoBigData/
│   │
│   ├── Fase6ProyectoBigData/
│   │   └── map_reduce_ventas.py
│   │
│   └── Fase7ProyectoBigData/
│       └── modelo_clasificacion_demanda.py
│
├── MODELOS/
│   └── modelo_clasificacion_demanda.joblib
│
├── RESULTADOS/
│   ├── MAP_REDUCE/
│   │   ├── ventas_por_region.csv
│   │   └── ventas_por_categoria.csv
│   │
│   ├── metricas_clasificacion.txt
│   └── predicciones_demanda.csv
│
├── .gitignore
├── requirements.txt
├── Dashboard.pdf
├── Documentacion_escrita.pdf
├── Retail_Inteligente__AI_Forecasting.html
└── README.md
```

---

## Tecnologías Utilizadas

* Python
* SQL Server
* pandas
* NumPy
* scikit-learn
* Jupyter Notebook
* Matplotlib
* Seaborn
* joblib
* Power BI

---

## Instalación

Se recomienda utilizar Python 3.10 o superior.

Crear un entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

---

## Ejecución de MapReduce

Desde la raíz del proyecto:

```bash
python "Fases/Fase6ProyectoBigData/map_reduce_ventas.py"
```

El proceso genera los resultados de ventas por región y categoría.

---

## Ejecución del Modelo de Clasificación

Desde la raíz del proyecto:

```bash
python "Fases/Fase7ProyectoBigData/modelo_clasificacion_demanda.py"
```

El proceso:

1. Carga el dataset.
2. Valida las columnas.
3. Limpia las variables.
4. Crea la variable objetivo.
5. Divide los datos.
6. Entrena el modelo.
7. Genera predicciones.
8. Calcula métricas.
9. Guarda los resultados.
10. Almacena el modelo entrenado.

---

## Resultados Generados

El proyecto genera diferentes archivos para facilitar el análisis de resultados.

### MapReduce

* `ventas_por_region.csv`
* `ventas_por_categoria.csv`

### Machine Learning

* `metricas_clasificacion.txt`
* `predicciones_demanda.csv`
* `modelo_clasificacion_demanda.joblib`

---

## Funcionalidades

* Análisis de información retail.
* Gestión de datos mediante Data Warehouse.
* Análisis exploratorio de datos.
* Consultas analíticas mediante vistas SQL.
* Procesamiento MapReduce.
* Cálculo de ventas por región.
* Cálculo de ventas por categoría.
* Clasificación de demanda.
* Evaluación del modelo con datos de prueba.
* Generación de probabilidades de alta demanda.
* Exportación de predicciones.
* Persistencia del modelo entrenado.

---

## Mejoras Futuras

* Comparar Regresión Logística con Random Forest y Gradient Boosting.
* Implementar validación cruzada.
* Analizar la importancia de las variables.
* Crear una API para consumir el modelo.
* Integrar el modelo con un dashboard.
* Automatizar el flujo de actualización de datos.
* Incorporar modelos de forecasting de series temporales.
* Implementar monitoreo del rendimiento del modelo.

---

## Uso Académico

Este proyecto fue desarrollado con fines académicos para aplicar conceptos de Big Data, ingeniería de datos, procesamiento distribuido y Machine Learning en un escenario relacionado con el sector retail.

Los resultados del modelo deben interpretarse como parte de un ejercicio académico de clasificación de demanda.
