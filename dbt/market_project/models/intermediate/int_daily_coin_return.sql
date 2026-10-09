-- int_daily_coin_return.sql

with stg_market_snapshot as (
    select 
        coin_id,
        coin_name,
        coin_symbol,
        snapshot_date,
        last_updated,
        current_price,
        coin_total_volume,
        coin_market_cap
    from {{ref('stg_market_snapshot')}}
),

previous_table as ( 
    select *,
    LAG(current_price) OVER(por_moneda) as previous_day_price,
    LAG(coin_total_volume) OVER(por_moneda) as previous_day_volume,
    LAG(coin_market_cap) OVER(por_moneda) as previous_day_market_cap
    from stg_market_snapshot
    WINDOW por_moneda AS (
        PARTITION BY coin_id
        ORDER BY snapshot_date
    )
),

--agregar DATE DIFF más adelante

return_and_change_table as ( 
    select *,
    (current_price - previous_day_price) as daily_price_change,

    SAFE_DIVIDE((current_price - previous_day_price), previous_day_price) * 100 as daily_price_change_pct, --porcentaje precio

    (coin_total_volume - previous_day_volume) as daily_volume_change,

    SAFE_DIVIDE((coin_total_volume - previous_day_volume), previous_day_volume) * 100 as daily_volume_change_pct, --porcentaje volumen
 
    (coin_market_cap - previous_day_market_cap) as daily_market_cap_change,

    SAFE_DIVIDE((coin_market_cap - previous_day_market_cap), previous_day_market_cap) * 100 as daily_market_cap_change_pct --porcentaje market cap

    from previous_table     
)

select * from return_and_change_table