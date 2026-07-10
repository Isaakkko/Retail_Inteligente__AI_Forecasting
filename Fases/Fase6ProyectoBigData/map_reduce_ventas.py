from collections import defaultdict
from pathlib import Path

import pandas as pd


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

# El archivo está ubicado en:
# Fases/Fase6ProyectoBigData/map_reduce_ventas.py

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "DATA"
RESULTADOS_DIR = PROJECT_ROOT / "RESULTADOS" / "MAP_REDUCE"

DATASET_PATH = DATA_DIR / "retail_store_inventory.csv"

RESULTADO_REGION_PATH = (
    RESULTADOS_DIR
    / "ventas_por_region.csv"
)

RESULTADO_CATEGORIA_PATH = (
    RESULTADOS_DIR
    / "ventas_por_categoria.csv"
)

RESULTADOS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# FUNCIONES
# ============================================================

def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Carga y valida el archivo CSV utilizado por MapReduce."""

    if not ruta.exists():
        raise FileNotFoundError(
            "No se encontró el dataset.\n"
            f"Ruta esperada: {ruta}"
        )

    dataframe = pd.read_csv(ruta)

    # Eliminar espacios adicionales en los nombres de columnas.
    dataframe.columns = dataframe.columns.str.strip()

    columnas_requeridas = [
        "Region",
        "Category",
        "Units Sold",
        "Price",
    ]

    columnas_faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in dataframe.columns
    ]

    if columnas_faltantes:
        raise ValueError(
            "Faltan las siguientes columnas en el dataset: "
            + ", ".join(columnas_faltantes)
        )

    return dataframe


def limpiar_datos(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepara las variables necesarias para calcular las ventas."""

    resultado = dataframe[
        [
            "Region",
            "Category",
            "Units Sold",
            "Price",
        ]
    ].copy()

    resultado["Region"] = (
        resultado["Region"]
        .astype("string")
        .str.strip()
    )

    resultado["Category"] = (
        resultado["Category"]
        .astype("string")
        .str.strip()
    )

    resultado["Units Sold"] = pd.to_numeric(
        resultado["Units Sold"],
        errors="coerce",
    )

    resultado["Price"] = pd.to_numeric(
        resultado["Price"],
        errors="coerce",
    )

    resultado = resultado.dropna(
        subset=[
            "Region",
            "Category",
            "Units Sold",
            "Price",
        ]
    )

    resultado = resultado[
        (resultado["Units Sold"] > 0)
        & (resultado["Price"] > 0)
    ].copy()

    resultado["Monto Venta"] = (
        resultado["Units Sold"]
        * resultado["Price"]
    )

    return resultado


def mapear_ventas(dataframe: pd.DataFrame):
    """
    Etapa Map.

    Genera pares clave-valor:

    - Región → monto de venta.
    - Categoría → monto de venta.
    """

    mapped_region = []
    mapped_category = []

    for fila in dataframe.itertuples(index=False):
        region = fila.Region
        categoria = fila.Category
        monto = fila._4

        mapped_region.append(
            (region, monto)
        )

        mapped_category.append(
            (categoria, monto)
        )

    return mapped_region, mapped_category


def agrupar_datos(mapped_data):
    """
    Etapa Shuffle.

    Agrupa todos los montos asociados con la misma clave.
    """

    grupos = defaultdict(list)

    for clave, valor in mapped_data:
        grupos[clave].append(valor)

    return grupos


def reducir_datos(grupos):
    """
    Etapa Reduce.

    Suma los montos agrupados para cada clave.
    """

    return {
        clave: sum(valores)
        for clave, valores in grupos.items()
    }


def convertir_resultados_dataframe(
    resultados: dict,
    nombre_clave: str,
) -> pd.DataFrame:
    """Convierte el diccionario final en un DataFrame ordenado."""

    dataframe = pd.DataFrame(
        resultados.items(),
        columns=[
            nombre_clave,
            "Ventas Totales",
        ],
    )

    dataframe = dataframe.sort_values(
        by="Ventas Totales",
        ascending=False,
    )

    dataframe["Ventas Totales"] = (
        dataframe["Ventas Totales"]
        .round(2)
    )

    return dataframe


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================

def main():
    print("=" * 60)
    print("PROCESO MAPREDUCE DE VENTAS")
    print("=" * 60)

    df = cargar_datos(
        DATASET_PATH
    )

    print(f"Registros cargados: {len(df)}")

    df_limpio = limpiar_datos(
        df
    )

    print(
        f"Registros válidos después de la limpieza: "
        f"{len(df_limpio)}"
    )

    if df_limpio.empty:
        raise ValueError(
            "No existen registros válidos para ejecutar MapReduce."
        )

    # ========================================================
    # ETAPA 1: MAP
    # ========================================================

    mapped_region, mapped_category = mapear_ventas(
        df_limpio
    )

    print()
    print("Etapa Map completada.")
    print(
        f"Pares generados por región: "
        f"{len(mapped_region)}"
    )
    print(
        f"Pares generados por categoría: "
        f"{len(mapped_category)}"
    )

    # ========================================================
    # ETAPA 2: SHUFFLE
    # ========================================================

    grupos_region = agrupar_datos(
        mapped_region
    )

    grupos_categoria = agrupar_datos(
        mapped_category
    )

    print()
    print("Etapa Shuffle completada.")
    print(
        f"Regiones agrupadas: "
        f"{len(grupos_region)}"
    )
    print(
        f"Categorías agrupadas: "
        f"{len(grupos_categoria)}"
    )

    # ========================================================
    # ETAPA 3: REDUCE
    # ========================================================

    ventas_region = reducir_datos(
        grupos_region
    )

    ventas_categoria = reducir_datos(
        grupos_categoria
    )

    print()
    print("Etapa Reduce completada.")

    # ========================================================
    # CONVERTIR RESULTADOS
    # ========================================================

    df_ventas_region = convertir_resultados_dataframe(
        ventas_region,
        "Región",
    )

    df_ventas_categoria = convertir_resultados_dataframe(
        ventas_categoria,
        "Categoría",
    )

    # ========================================================
    # MOSTRAR RESULTADOS
    # ========================================================

    print()
    print("=" * 60)
    print("VENTAS TOTALES POR REGIÓN")
    print("=" * 60)

    print(
        df_ventas_region.to_string(
            index=False
        )
    )

    print()
    print("=" * 60)
    print("VENTAS TOTALES POR CATEGORÍA")
    print("=" * 60)

    print(
        df_ventas_categoria.to_string(
            index=False
        )
    )

    # ========================================================
    # GUARDAR RESULTADOS
    # ========================================================

    df_ventas_region.to_csv(
        RESULTADO_REGION_PATH,
        index=False,
    )

    df_ventas_categoria.to_csv(
        RESULTADO_CATEGORIA_PATH,
        index=False,
    )

    print()
    print("=" * 60)
    print("PROCESO FINALIZADO CORRECTAMENTE")
    print("=" * 60)

    print("Archivos generados:")
    print(
        f"- Ventas por región:\n"
        f"  {RESULTADO_REGION_PATH}"
    )
    print(
        f"- Ventas por categoría:\n"
        f"  {RESULTADO_CATEGORIA_PATH}"
    )


if __name__ == "__main__":
    main()


    def mapear_ventas(dataframe: pd.DataFrame):
        """
        Etapa Map.

        Genera pares clave-valor:

        - Región → monto de venta.
        - Categoría → monto de venta.
        """

        mapped_region = []
        mapped_category = []

        for _, fila in dataframe.iterrows():
            region = fila["Region"]
            categoria = fila["Category"]
            monto = fila["Monto Venta"]

            mapped_region.append(
                (region, monto)
            )

            mapped_category.append(
                (categoria, monto)
            )

        return mapped_region, mapped_category