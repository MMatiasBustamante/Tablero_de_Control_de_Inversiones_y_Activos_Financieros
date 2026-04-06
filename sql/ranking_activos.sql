-- 01_ranking_activos.sql
-- Ranking general de activos por Sharpe Ratio

SELECT 
    index AS ticker,
    retorno_anual,
    sharpe_ratio,
    volatilidad_anual,
    max_drawdown
FROM metricas_riesgo
ORDER BY sharpe_ratio DESC;

--query 1: Buscar los 3 ticker con mayor retorno anual
select index as ticker, retorno_anual
from metricas_riesgo 
order by retorno_anual desc limit 3

--query 2:  Activos con drawdown peor a -40%
select index as ticker, max_drawdown
from metricas_riesgo
where max_drawdown < -0.4
order by max_drawdown desc

