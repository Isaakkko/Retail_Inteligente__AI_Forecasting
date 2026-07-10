from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# CONFIGURACIÓN
# ============================================================

RANDOM_STATE = 42
TEST_SIZE = 0.20

COLUMNAS_MODELO = [
    "Price",
    "Units Ordered",
    "Inventory Level",
    "Discount",
    "Holiday/Promotion",
    "Competitor Pricing",
]

COLUMNA_VENTAS = "Units Sold"
COLUMNA_OBJETIVO = "alta_demanda"


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

# El archivo está ubicado en:
# Fases/Fase7ProyectoBigData/modelo_clasificacion_demanda.py

FASE_7_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"
MODELOS_DIR = PROJECT_ROOT / "MODELOS"
RESULTADOS_DIR = PROJECT_ROOT / "RESULTADOS"

DATASET_PATH = DATA_DIR / "retail_store_inventory.csv"
MODELO_PATH = MODELOS_DIR / "modelo_clasificacion_demanda.joblib"
METRICAS_PATH = RESULTADOS_DIR / "metricas_clasificacion.txt"
PREDICCIONES_PATH = RESULTADOS_DIR / "predicciones_demanda.csv"

MODELOS_DIR.mkdir(parents=True, exist_ok=True)
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CARGA DE DATOS
# ============================================================

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        "No se encontró el dataset.\n"
        f"Ruta esperada: {DATASET_PATH}\n\n"
        "Cree una carpeta DATA en la raíz del proyecto y coloque allí "
        "el archivo retail_store_inventory.csv."
    )

df = pd.read_csv(DATASET_PATH)

# Limpiar espacios en los nombres de las columnas.
df.columns = df.columns.str.strip()

print("=" * 60)
print("DATASET CARGADO CORRECTAMENTE")
print("=" * 60)
print(f"Filas: {df.shape[0]}")
print(f"Columnas: {df.shape[1]}")
print()


# ============================================================
# VALIDACIÓN DE COLUMNAS
# ============================================================

columnas_requeridas = COLUMNAS_MODELO + [COLUMNA_VENTAS]

columnas_faltantes = [
    columna
    for columna in columnas_requeridas
    if columna not in df.columns
]

if columnas_faltantes:
    raise ValueError(
        "Faltan las siguientes columnas en el dataset: "
        + ", ".join(columnas_faltantes)
    )


# ============================================================
# LIMPIEZA DE VARIABLES
# ============================================================

# Convertir las variables utilizadas a formato numérico.
# Los valores que no puedan convertirse pasan a NaN y serán
# imputados posteriormente dentro del pipeline.

for columna in columnas_requeridas:
    df[columna] = pd.to_numeric(
        df[columna],
        errors="coerce",
    )

# Eliminar registros donde no existe información de ventas,
# porque esa variable se utiliza para crear el objetivo.

df = df.dropna(
    subset=[COLUMNA_VENTAS]
).copy()

if df.empty:
    raise ValueError(
        "No quedaron registros válidos después de limpiar Units Sold."
    )


# ============================================================
# CREACIÓN DE LA VARIABLE OBJETIVO
# ============================================================

# Se utiliza la mediana en lugar de la media para reducir el impacto
# de valores extremos y obtener clases más equilibradas.

umbral_alta_demanda = df[COLUMNA_VENTAS].median()

df[COLUMNA_OBJETIVO] = (
    df[COLUMNA_VENTAS] > umbral_alta_demanda
).astype(int)

print("=" * 60)
print("VARIABLE OBJETIVO")
print("=" * 60)
print(f"Umbral de alta demanda: {umbral_alta_demanda:.2f}")
print()
print("Distribución de clases:")
print(df[COLUMNA_OBJETIVO].value_counts().sort_index())
print()


# ============================================================
# VARIABLES DE ENTRADA Y OBJETIVO
# ============================================================

X = df[COLUMNAS_MODELO].copy()
y = df[COLUMNA_OBJETIVO].copy()

if y.nunique() < 2:
    raise ValueError(
        "La variable objetivo contiene una sola clase. "
        "No es posible entrenar un clasificador."
    )


# ============================================================
# DIVISIÓN DE DATOS
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y,
)


# ============================================================
# PIPELINE DE PREPROCESAMIENTO Y MODELO
# ============================================================

preprocesamiento = ColumnTransformer(
    transformers=[
        (
            "variables_numericas",
            Pipeline(
                steps=[
                    (
                        "imputacion",
                        SimpleImputer(strategy="median"),
                    ),
                    (
                        "escalamiento",
                        StandardScaler(),
                    ),
                ]
            ),
            COLUMNAS_MODELO,
        )
    ],
    remainder="drop",
)

modelo = Pipeline(
    steps=[
        (
            "preprocesamiento",
            preprocesamiento,
        ),
        (
            "clasificador",
            LogisticRegression(
                max_iter=2000,
                random_state=RANDOM_STATE,
                class_weight="balanced",
            ),
        ),
    ]
)


# ============================================================
# ENTRENAMIENTO
# ============================================================

modelo.fit(
    X_train,
    y_train,
)


# ============================================================
# PREDICCIONES
# ============================================================

predicciones = modelo.predict(
    X_test
)

probabilidades = modelo.predict_proba(
    X_test
)[:, 1]


# ============================================================
# EVALUACIÓN
# ============================================================

accuracy = accuracy_score(
    y_test,
    predicciones,
)

matriz = confusion_matrix(
    y_test,
    predicciones,
)

reporte = classification_report(
    y_test,
    predicciones,
    target_names=[
        "Demanda normal",
        "Alta demanda",
    ],
    zero_division=0,
)

print("=" * 60)
print("RESULTADOS DEL MODELO")
print("=" * 60)
print(f"Accuracy de prueba: {accuracy:.4f}")
print()

print("Matriz de confusión:")
print(matriz)
print()

print("Reporte de clasificación:")
print(reporte)


# ============================================================
# GUARDAR PREDICCIONES
# ============================================================

df_predicciones = X_test.copy()

df_predicciones["valor_real"] = y_test.values
df_predicciones["prediccion"] = predicciones
df_predicciones["probabilidad_alta_demanda"] = probabilidades

df_predicciones["clasificacion_real"] = (
    df_predicciones["valor_real"]
    .map(
        {
            0: "Demanda normal",
            1: "Alta demanda",
        }
    )
)

df_predicciones["clasificacion_predicha"] = (
    df_predicciones["prediccion"]
    .map(
        {
            0: "Demanda normal",
            1: "Alta demanda",
        }
    )
)

df_predicciones.to_csv(
    PREDICCIONES_PATH,
    index=False,
)


# ============================================================
# GUARDAR MODELO
# ============================================================

artefacto_modelo = {
    "modelo": modelo,
    "columnas": COLUMNAS_MODELO,
    "umbral_alta_demanda": umbral_alta_demanda,
    "clases": {
        0: "Demanda normal",
        1: "Alta demanda",
    },
}

joblib.dump(
    artefacto_modelo,
    MODELO_PATH,
)


# ============================================================
# GUARDAR MÉTRICAS
# ============================================================

contenido_metricas = (
    "MODELO DE CLASIFICACIÓN DE DEMANDA\n"
    "===================================\n\n"
    f"Total de registros: {len(df)}\n"
    f"Registros de entrenamiento: {len(X_train)}\n"
    f"Registros de prueba: {len(X_test)}\n"
    f"Umbral de alta demanda: {umbral_alta_demanda:.2f}\n"
    f"Accuracy de prueba: {accuracy:.4f}\n\n"
    "Matriz de confusión:\n"
    f"{matriz}\n\n"
    "Reporte de clasificación:\n"
    f"{reporte}\n"
)

METRICAS_PATH.write_text(
    contenido_metricas,
    encoding="utf-8",
)


# ============================================================
# RESUMEN FINAL
# ============================================================

print("=" * 60)
print("PROCESO FINALIZADO CORRECTAMENTE")
print("=" * 60)

print(f"Total de registros utilizados: {len(df)}")
print(f"Registros de entrenamiento: {len(X_train)}")
print(f"Registros de prueba: {len(X_test)}")
print(f"Accuracy de prueba: {accuracy:.4f}")
print()

print("Archivos generados:")
print(f"- Modelo:\n  {MODELO_PATH}")
print(f"- Predicciones:\n  {PREDICCIONES_PATH}")
print(f"- Métricas:\n  {METRICAS_PATH}")