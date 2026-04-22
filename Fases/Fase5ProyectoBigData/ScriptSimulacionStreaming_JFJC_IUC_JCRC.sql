-- Se inserta un dato nuevo tipo "streaming" en la tabla staging

INSERT INTO staging_retail
VALUES (
'2022-01-01',
'S001',
'P0001',
'Groceries',
'North',
999,
50,
60,
55.00,
35.00,
5,
'Sunny',
0,
33.00,
'Autumn'
);

-- Se hace el insert usando joins para las demas dimensiones

INSERT INTO fact_ventas_inventario
SELECT
t.id_tiempo,
ti.id_tienda,
p.id_producto,
c.id_clima,
s.units_sold,
s.units_ordered,
s.inventory_level,
s.demand_forecast,
s.price,
s.discount,
s.competitor_pricing

FROM staging_retail s
JOIN dim_tiempo t
ON s.fecha = t.fecha
AND s.seasonality = t.seasonality
AND s.holiday = t.holiday

JOIN dim_tienda ti
ON s.store_id = ti.store_id
AND s.region = ti.region

JOIN dim_producto p
ON s.product_id = p.product_id
AND s.category = p.category

JOIN dim_clima c
ON s.weather_condition = c.weather_condition

WHERE s.inventory_level = 999; -- Dato nuevo con valor exagerado para que no se camuflajee con los demás


-- Consulta para ver el dato ya en la fact table
SELECT *
FROM fact_ventas_inventario
WHERE inventory_level = 999;