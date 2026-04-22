# Map Reduce - Fase 6 Proyecto Big data 

# Librerias 

import pandas as pd
from collections import defaultdict

# (Carga de datos)

df = pd.read_csv(r"C:\CSV Proyecto BD\retail_store_inventory.csv")


# ETAPA 1: MAP 

# Lista que almacenará tuplas (región, monto)
mapped_region = []

# Lista que almacenará tuplas (categoría, monto)
mapped_category = []


for _, row in df.iterrows():

    # Variables para usar 
    region = row.get("Region")
    category = row.get("Category")
    units_sold = row.get("Units Sold")
    price = row.get("Price")

    # Validar los datos 
    if pd.isna(region) or pd.isna(category):
        continue

    if units_sold <= 0 or price <= 0:
        continue

    # Calcula el monto de venta
    monto = units_sold * price

    # Fase de MAP 
    mapped_region.append((region, monto))
    mapped_category.append((category, monto))



# ETAPA 2: SHUFFLE 


def agrupar(mapped_data):
    groups = defaultdict(list)
    for k, v in mapped_data:
        groups[k].append(v)
    return groups

groups_region = agrupar(mapped_region)
groups_category = agrupar(mapped_category)



# ETAPA 3: REDUCE 

# Ventas totales por región
reduced_region = {k: sum(vs) for k, vs in groups_region.items()}

# Ventas totales por categoría
reduced_category = {k: sum(vs) for k, vs in groups_category.items()}



# RESULTADOS

print("\nVentas por región:")
print(reduced_region)

print("\nVentas por categoría:")
print(reduced_category)


