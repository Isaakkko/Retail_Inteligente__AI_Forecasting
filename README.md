# 🛒 Retail Inteligente — AI Forecasting

**Proyecto Big Data — Análisis y Predicción de Demanda en Retail**
**Colegio Universitario de Cartago — Costa Rica**

**Integrantes:**
- Isaac Ulloa Calvo
- Jeffrey Jiménez Cordero
- Jean Carlo Ramírez Carranza

---

## 📌 Descripción del Proyecto

Este proyecto desarrolla un sistema completo de análisis y predicción de demanda para el sector retail, abarcando desde el modelado de un Data Warehouse hasta la aplicación de modelos de Machine Learning para clasificar la demanda.

El objetivo principal es construir una infraestructura de datos robusta que permita analizar patrones de ventas, niveles de inventario, comportamiento del cliente y variables externas como clima y promociones, con el fin de apoyar la toma de decisiones empresariales.

El proyecto fue desarrollado en siete fases progresivas que van desde la planificación hasta la implementación de modelos predictivos.

---

## 📊 Descripción del Dataset

**Fuente:** [Retail Store Inventory Forecasting Dataset — Kaggle](https://www.kaggle.com/datasets/anirudhchauhan/retail-store-inventory-forecasting-dataset)

El dataset contiene **73,000 registros** históricos de una cadena de tiendas retail con información de ventas, inventario, precios y condiciones externas.

### 📋 Variables del Dataset

| Variable | Descripción |
|---|---|
| **Date** | Fecha del registro |
| **Store ID** | Identificador de la tienda |
| **Product ID** | Identificador del producto |
| **Category** | Categoría del producto |
| **Region** | Región geográfica de la tienda |
| **Inventory Level** | Nivel de inventario disponible |
| **Units Sold** | Unidades vendidas |
| **Units Ordered** | Unidades ordenadas al proveedor |
| **Demand Forecast** | Estimación de demanda |
| **Price** | Precio del producto |
| **Discount** | Descuento aplicado |
| **Weather Condition** | Condición climática del día |
| **Holiday/Promotion** | Indicador de día festivo o promoción |
| **Competitor Pricing** | Precio de la competencia |
| **Seasonality** | Temporada del año |

---

## 🗄️ Arquitectura del Data Warehouse

Se implementó un **esquema estrella** en SQL Server para facilitar el análisis y la consulta eficiente de los datos.

### Tabla de Hechos
**`fact_ventas_inventario`** — Contiene las métricas principales: unidades vendidas, unidades ordenadas, nivel de inventario, pronóstico de demanda, precio, descuento y precio competidor.

### Dimensiones

| Tabla | Descripción |
|---|---|
| **`dim_tiempo`** | Fecha, año, mes, día, temporada y festivo |
| **`dim_tienda`** | ID de tienda y región |
| **`dim_producto`** | ID de producto y categoría |
| **`dim_clima`** | Condición climática |

### Vistas SQL creadas

- `vw_ventas_por_mes` — Ventas e ingresos totales agrupados por mes
- `vw_ventas_por_categoria` — Rendimiento por categoría de producto
- `vw_ventas_por_region` — Comparativo de ventas por región
- `vw_ventas_por_clima` — Impacto de las condiciones climáticas en las ventas
- `vw_forecast_vs_ventas` — Comparación entre demanda estimada y ventas reales

---

## 📁 Estructura del Proyecto
Retail_Inteligente__AI_Forecasting/

**Fase 1 — Planificación**
Definición del alcance, objetivos y requerimientos del proyecto.

**Fase 2 — Modelado y Almacenamiento**
Diseño e implementación del Data Warehouse con esquema estrella en SQL Server. Carga de los 73,000 registros mediante staging table y BULK INSERT.

**Fase 4 — Vistas Analíticas**
Creación de vistas SQL para consultas de negocio: ventas por mes, categoría, región, clima y comparativo de forecast.

**Fase 5 — Streaming en Tiempo Real**
Simulación de procesamiento en tiempo real mediante inserción manual de registros y consultas de validación en tiempo real.

**Fase 6 — Map Reduce**
Implementación del patrón Map-Shuffle-Reduce en Python para calcular ventas totales por región y por categoría de producto.

**Fase 7 — Modelo Predictivo (ML)**
Aplicación de Regresión Logística para clasificar días de alta demanda. El modelo alcanzó una precisión aproximada del **71%**, utilizando variables como precio, inventario, pedidos, descuento, promociones y precio de la competencia.

---

## 🛠️ Tecnologías Utilizadas

- **SQL Server** — Data Warehouse, modelado relacional y vistas analíticas
- **Python 3** — Procesamiento de datos, Map Reduce y Machine Learning
- **pandas** — Manipulación y análisis de datos
- **scikit-learn** — Modelo de Regresión Logística
- **Power BI / Dashboard** — Visualización de resultados

---

## 📈 Resultados Principales

- Data Warehouse funcional con esquema estrella y 73,000 registros cargados
- Vistas SQL que permiten analizar ventas por mes, región, categoría y clima
- Implementación exitosa del patrón Map Reduce para agregaciones de ventas
- Modelo de clasificación con **~71% de precisión** para identificar días de alta demanda

---

## 📌 Notas Finales

Este proyecto integra conceptos de Big Data, ingeniería de datos y Machine Learning aplicados al sector retail. Cada fase construye sobre la anterior, formando un pipeline completo desde el almacenamiento estructurado hasta la predicción inteligente de demanda.


