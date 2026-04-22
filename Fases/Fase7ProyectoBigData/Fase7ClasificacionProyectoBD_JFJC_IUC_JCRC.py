import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Ruta del archivo
ruta = r"C:\CSV Proyecto BD\retail_store_inventory.csv"

# Cargar datos
df = pd.read_csv(ruta)
print(df.head())

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# Crear variable objetivo
promedio_ventas = df['Units Sold'].mean()
df['alta_demanda'] = (df['Units Sold'] > promedio_ventas).astype(int)

# Variables 
X = df[['Price', 'Units Ordered', 'Inventory Level', 'Discount', 'Holiday/Promotion', 'Competitor Pricing']]
y = df['alta_demanda']

# Modelo
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Predicciones
predicciones = model.predict(X)

print("--- Predicciones Generadas con Éxito ---")
print(predicciones)

# Evaluación
print("Accuracy:", accuracy_score(y, predicciones))

# Información general
print(f"\nTotal de registros: {len(df)}")
print(f"Promedio de ventas calculado: {promedio_ventas:.2f}")


# El modelo de regresión logística alcanzó una precisión aproximada del 71%, 
# mostrando un desempeño consistente. La inclusión de variables adicionales como inventario, 
# pedidos y precios de competencia permitió obtener predicciones más equilibradas, aunque el impacto marginal de algunas variables fue limitado.3

#Se aplicó un modelo de regresión logística para clasificar la demanda, logrando una precisión cercana al 71%, lo que demuestra su utilidad para apoyar decisiones en el entorno retail