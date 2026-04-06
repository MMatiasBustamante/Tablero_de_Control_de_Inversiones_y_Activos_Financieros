-- query 3: volatilidad promedio por categoria
--SELECT categoria, AVG(volatilidad_anual)
--FROM metricas_riesgo m JOIN referencia_activos r
--on m.index = r.ticker
--GROUP BY categoria

--query 4: Activo con mejor y peor Sharpe por categoría
select  categoria,
        ticker, 
        sharpe_ratio,
        case when sharpe_ratio = (
            SELECT MAX(sharpe_ratio) 
            FROM metricas_riesgo m2 
            JOIN referencia_activos r2 ON m2.index = r2.ticker
            WHERE r2.categoria = r.categoria) 
            then 'Max'
        else 'Min'
    end as tipo
FROM metricas_riesgo m JOIN referencia_activos r
on m.index = r.ticker
WHERE sharpe_ratio = (
    SELECT MAX(sharpe_ratio) 
    FROM metricas_riesgo m2 
    JOIN referencia_activos r2 ON m2.index = r2.ticker
    WHERE r2.categoria = r.categoria
)
or sharpe_ratio = (
    SELECT MIN(sharpe_ratio) 
    FROM metricas_riesgo m2 
    JOIN referencia_activos r2 ON m2.index = r2.ticker
    WHERE r2.categoria = r.categoria
)
order by categoria, tipo