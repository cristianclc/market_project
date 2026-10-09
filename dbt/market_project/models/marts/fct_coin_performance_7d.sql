-- fct_coin_performance_7d.sql

WITH int_daily_coin_return AS (
    SELECT *
    FROM {{ref('int_daily_coin_return')}}
),

weekly_changes AS (
    SELECT *,
    LAG(current_price, 7) OVER(PARTITION BY coin_id ORDER BY snapshot_date) as price_7d, --precio de hace 7 días
    COUNT(coin_id) OVER(last_week) as days_in_window_7d, --conteo de cuantos días estuvo la moneda en los 7 últimos
    COUNT(CASE WHEN daily_price_change_pct > 0 THEN 1 END) OVER(last_week) as positive_return_count_7d --conteo de cuantas veces se registró un retorno positivo en la última semana
    FROM int_daily_coin_return
    WINDOW last_week AS (
        PARTITION BY coin_id 
        ORDER BY snapshot_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW 
    )
),

coin_return_std_tendency AS (
    SELECT *,
    days_in_window_7d = 7 AS is_full_window,
    (current_price - price_7d) AS price_7d_return,
    STDDEV_SAMP(daily_price_change_pct) OVER(last_week) AS weekly_price_volatility, --desviación estándar de retorno diario (volatiliad de los últimos 7 días)
    AVG(current_price) OVER(last_week) AS price_ma_7d, --promedio de la última semana, si precio actual es mayor, alcista
    AVG(coin_total_volume) OVER(last_week) AS weekly_avg_volume, --volumen total de esta semana
    AVG(coin_total_volume) OVER(PARTITION BY coin_id  ORDER BY snapshot_date ROWS BETWEEN 13 PRECEDING AND 7 PRECEDING) AS last_week_avg_volume --volumen total de la semana pasada
    FROM weekly_changes
    WINDOW last_week AS (
        PARTITION BY coin_id 
        ORDER BY snapshot_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW 
    )
),

tendency AS (
    SELECT *,
    SAFE_DIVIDE(price_7d_return, price_7d) AS price_7d_return_pct, --porcentaje de retorno en los últimos 7 días
    current_price >  price_ma_7d as bool_actualprice_higher_than_mean --columna booleana de si precio actual es superior a media semanal
    FROM coin_return_std_tendency
),

ranking AS (
    SELECT *,
    RANK() OVER(PARTITION BY snapshot_date ORDER BY price_7d_return_pct DESC) as return_7d_rank --ranking de los retornos semanales por moneda
    FROM tendency
)



SELECT *  EXCEPT(days_in_window_7d) FROM ranking