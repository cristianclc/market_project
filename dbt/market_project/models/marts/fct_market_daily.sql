-- fct_market_daily.sql

with int_daily_coin_return as (
    SELECT *,
    from {{ref('int_daily_coin_return')}}
),

vol_cap_total as (
    SELECT
    snapshot_date,
    COUNT(DISTINCT(coin_id)) as coins_day, --numero de monedas distintas en el snapshot del día
    SUM(coin_total_volume) as total_volume, --valor total de todas las compras (en un dia)
    SUM(coin_market_cap) as total_market_cap, --valor total de todas las monedas (en un dia)
    SUM(CASE WHEN coin_id = "bitcoin" THEN coin_market_cap ELSE 0 END) as bitcoin_total_market_cap --valor total SOLO de bitcoin
    from int_daily_coin_return
    GROUP BY snapshot_date
),

prev_volume_cap as (
    SELECT *, 
    LAG(total_volume) OVER(ORDER BY snapshot_date) as previous_total_volume, --anterior volumen diario
    LAG(total_market_cap) OVER(ORDER BY snapshot_date) as previous_total_market_cap --anterior market cap diario 
    from vol_cap_total
),

bitcoin_cap_vol_change as (
    SELECT *, 
    (total_volume - previous_total_volume) as daily_total_volume_change, --cambio en volumen diario
    (total_market_cap - previous_total_market_cap) as daily_total_market_cap_change, --cambio en market cap diario 
    SAFE_DIVIDE(bitcoin_total_market_cap, total_market_cap) * 100 as bitcoin_cap_participation_pct --participacion de bitcoin en market cap total
    from prev_volume_cap
)



SELECT * from bitcoin_cap_vol_change