# Algerian Forest Fires Analysis

Proyecto de análisis exploratorio de datos y clustering aplicado a información meteorológica relacionada con incendios forestales en Argelia.

## Descripción del Proyecto

Este proyecto analiza información meteorológica e índices del sistema **Fire Weather Index (FWI)** con el objetivo de identificar patrones presentes en condiciones relacionadas con incendios forestales.

El análisis utiliza datos registrados en dos regiones de Argelia y combina técnicas de limpieza de datos, análisis exploratorio, visualización y aprendizaje no supervisado.

Como parte del proyecto se implementa un modelo de clustering mediante **K-Means**, permitiendo agrupar observaciones con características similares sin utilizar la variable de clasificación del dataset durante el proceso de agrupamiento.

El proyecto también utiliza **Principal Component Analysis (PCA)** para representar visualmente los clusters obtenidos en un espacio bidimensional.

---

## Descripción del Dataset

El conjunto de datos contiene observaciones meteorológicas registradas entre junio y septiembre de 2012 en dos regiones de Argelia:

* Bejaia.
* Sidi Bel-Abbès.

El dataset contiene información meteorológica e índices relacionados con el sistema Fire Weather Index.

### Variables del Dataset

| Variable      | Descripción                        |
| ------------- | ---------------------------------- |
| `day`         | Día de la observación              |
| `month`       | Mes de la observación              |
| `year`        | Año de la observación              |
| `Temperature` | Temperatura máxima al mediodía     |
| `RH`          | Humedad relativa                   |
| `Ws`          | Velocidad del viento               |
| `Rain`        | Cantidad de lluvia diaria          |
| `FFMC`        | Fine Fuel Moisture Code            |
| `DMC`         | Duff Moisture Code                 |
| `DC`          | Drought Code                       |
| `ISI`         | Initial Spread Index               |
| `BUI`         | Buildup Index                      |
| `FWI`         | Fire Weather Index                 |
| `Classes`     | Clasificación Fire o Not Fire      |
| `Region`      | Región de procedencia del registro |

El dataset original contiene 244 observaciones correspondientes a las dos regiones estudiadas.

---

## Flujo del Proyecto

```text
Dataset de incendios forestales
              ↓
Carga de datos
              ↓
Limpieza y preparación
              ↓
Análisis exploratorio
              ↓
Selección de variables numéricas
              ↓
StandardScaler
              ↓
Método del codo
              ↓
Silhouette Score
              ↓
K-Means
              ↓
Asignación de clusters
              ↓
PCA
              ↓
Visualización y almacenamiento
```

---

## Análisis Exploratorio de Datos

La etapa de EDA permite estudiar las características generales del conjunto de datos.

Durante esta fase se analizan:

* Distribución de variables meteorológicas.
* Temperatura.
* Humedad relativa.
* Velocidad del viento.
* Precipitación.
* Índices del sistema FWI.
* Diferencias entre observaciones.
* Relación entre variables.
* Comportamiento de registros asociados con incendios.

Los notebooks y componentes de análisis se encuentran dentro de:

`PROYECTO/EDA`

---

## Clustering

El proyecto implementa el algoritmo **K-Means** para identificar grupos de observaciones con características similares.

El proceso se encuentra implementado en:

`PROYECTO/CLUSTERING/PROCESO_CLUSTER.py`

### Preparación de Variables

Antes de aplicar clustering se excluyen:

* `day`
* `month`
* `year`
* `Classes`

La variable `Classes` no se utiliza para formar los clusters debido a que K-Means es un algoritmo de aprendizaje no supervisado.

Posteriormente se mantienen únicamente las variables numéricas.

Los valores faltantes son tratados mediante la mediana de cada variable.

---

## Escalamiento de Datos

Las variables utilizadas presentan diferentes escalas.

Por esta razón se utiliza:

`StandardScaler`

El escalamiento transforma las variables para que puedan ser comparadas de forma adecuada durante el cálculo de distancias utilizado por K-Means.

El flujo de preparación es:

```text
Variables numéricas
        ↓
Tratamiento de valores faltantes
        ↓
StandardScaler
        ↓
Datos escalados
```

---

## Selección del Número de Clusters

El proyecto utiliza dos métodos para evaluar diferentes valores de `k`.

### Método del Codo

Se calcula la inercia para valores de `k` entre 1 y 9.

El gráfico generado permite observar cómo disminuye la inercia al aumentar el número de clusters.

El resultado se almacena en:

`PROYECTO/RESULTADOS/metodo_codo.png`

### Silhouette Score

Se calcula el Silhouette Score para valores de `k` entre 2 y 9.

Esta métrica analiza la cohesión interna de los clusters y la separación entre los grupos.

El script selecciona automáticamente el valor de `k` con el mayor Silhouette Score.

Los resultados se almacenan en:

```text
PROYECTO/RESULTADOS/
├── resultados_silhouette.csv
└── silhouette_score.png
```

---

## Modelo K-Means

Después de seleccionar el mejor número de clusters se entrena el modelo final.

```text
Datos escalados
      ↓
K-Means
      ↓
Cluster asignado
```

Cada registro recibe una nueva variable:

`Cluster`

El dataset resultante se almacena en:

`PROYECTO/RESULTADOS/Algerian_forest_fires_con_clusters.csv`

Esto permite analizar posteriormente las características de cada grupo.

---

## Análisis de Centroides

Los centroides representan el punto central de cada cluster.

Después del entrenamiento, los centroides se transforman nuevamente a la escala original mediante:

`inverse_transform`

Esto permite interpretar los valores utilizando las unidades originales de las variables.

Los centroides se almacenan en:

`PROYECTO/RESULTADOS/centroides_clusters.csv`

El análisis de centroides permite comparar las características promedio representativas de cada cluster.

---

## Visualización con PCA

K-Means utiliza múltiples variables simultáneamente.

Por esta razón, representar los clusters utilizando únicamente dos variables originales puede generar una visualización incompleta.

El proyecto utiliza **Principal Component Analysis (PCA)** para reducir los datos escalados a dos componentes principales.

```text
Datos multidimensionales
          ↓
PCA
          ↓
2 componentes principales
          ↓
Visualización bidimensional
```

La gráfica PCA permite observar la distribución de los clusters en un espacio de dos dimensiones.

El gráfico se almacena en:

`PROYECTO/RESULTADOS/visualizacion_clusters_pca.png`

Los datos transformados mediante PCA también se guardan en:

`PROYECTO/RESULTADOS/datos_clusters_pca.csv`

---

## Persistencia de Modelos

Los componentes utilizados durante el proceso de clustering se almacenan utilizando `joblib`.

Se guardan:

* Modelo K-Means.
* StandardScaler.
* Modelo PCA.
* Lista de columnas utilizadas durante el entrenamiento.

Los archivos permiten reutilizar el proceso sin entrenar nuevamente todos los componentes.

Los modelos se almacenan en:

```text
PROYECTO/MODELOS/
├── modelo_kmeans.pkl
├── scaler_clustering.pkl
├── modelo_pca.pkl
└── columnas_clustering.pkl
```

---

## Estructura del Proyecto

```text
Algerian_forest_fires/
│
├── PROYECTO/
│   ├── CLUSTERING/
│   │   ├── PROCESO_CLUSTER.py
│   │   └── Proceso_Cluster.ipynb
│   │
│   ├── DATA/
│   │   └── Algerian_forest_fires_dataset_CLEANED.csv
│   │
│   ├── EDA/
│   │
│   ├── MODELOS/
│   │   ├── modelo_kmeans.pkl
│   │   ├── scaler_clustering.pkl
│   │   ├── modelo_pca.pkl
│   │   └── columnas_clustering.pkl
│   │
│   └── RESULTADOS/
│       ├── Algerian_forest_fires_con_clusters.csv
│       ├── centroides_clusters.csv
│       ├── resultados_silhouette.csv
│       ├── datos_clusters_pca.csv
│       ├── metodo_codo.png
│       ├── silhouette_score.png
│       └── visualizacion_clusters_pca.png
│
├── README.md
└── presentacion_Algerian_forest_fires.html
```

---

## Funcionamiento del Proyecto

El proyecto sigue un flujo de análisis no supervisado.

Primero se carga el dataset procesado y se validan las variables requeridas.

Posteriormente se seleccionan las variables numéricas y se realiza el tratamiento de valores faltantes.

Los datos se escalan utilizando StandardScaler para mantener escalas comparables.

Después se analizan diferentes valores de `k` mediante el método del codo y Silhouette Score.

El mejor valor de `k` identificado mediante Silhouette Score se utiliza para entrenar el modelo final K-Means.

Cada observación recibe un cluster y los centroides se transforman nuevamente a su escala original.

Finalmente, PCA reduce los datos a dos componentes principales para generar una representación visual de los grupos.

Los resultados, métricas, gráficos y modelos se almacenan en carpetas independientes.

---

## Funcionalidades

* Carga y validación del dataset.
* Selección automática de variables numéricas.
* Tratamiento de valores faltantes.
* Escalamiento mediante StandardScaler.
* Evaluación de diferentes números de clusters.
* Aplicación del método del codo.
* Cálculo del Silhouette Score.
* Selección automática del mejor valor de `k`.
* Entrenamiento de K-Means.
* Asignación de clusters.
* Análisis de centroides.
* Reducción dimensional mediante PCA.
* Visualización bidimensional de clusters.
* Exportación de resultados en CSV.
* Generación de gráficos.
* Persistencia de modelos mediante joblib.

---

## Tecnologías Utilizadas

* Python
* pandas
* Matplotlib
* scikit-learn
* Jupyter Notebook
* joblib
* pathlib

---

## Colaboradores

* Isaac Ulloa Calvo
* Tiffany Méndez Quirós
* Edward Vindas Rivera
* Jean Carlo Ramírez Carranza

---

## Notas Finales

Este proyecto integra análisis exploratorio de datos y aprendizaje no supervisado para estudiar información meteorológica relacionada con incendios forestales.

La implementación de K-Means permite identificar grupos de observaciones con características similares, mientras que PCA facilita la representación visual de información multidimensional.

El proyecto tiene un enfoque académico y los clusters obtenidos representan agrupaciones estadísticas basadas en las variables utilizadas. No deben interpretarse como un sistema oficial de predicción o alerta de incendios forestales.
