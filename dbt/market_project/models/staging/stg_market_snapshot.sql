-- stg_market_snapshot.sql

with 

source as ( --se usa name, no schema en primer parámetro de source
    select * from  {{source('crypto_raw','market_snapshot')}} --seleccionamos todo de nuestra fuente en crypto_raw.market_snapshot
),

renamed_table as ( --no seleccionamos, images ni roi 
    
    select 
    
    -- renamed
    id as coin_id,
    symbol as coin_symbol,
    name as coin_name,

    current_price,

    -- renamed
    market_cap as coin_market_cap,
    market_cap_rank as coin_market_cap_rank,
    fully_diluted_valuation,

    -- renamed
    total_volume as coin_total_volume,

    -- renamed
    high_24h as highest_value_24h,
    low_24h as lowest_value_24h,

    price_change_24h,
    price_change_percentage_24h,
    market_cap_change_24h,
    market_cap_change_percentage_24h,
    circulating_supply,
    total_supply,
    max_supply,

    -- renamed
    ath as all_time_high,
    atl as all_time_low,

    ath_change_percentage,
    ath_date,
    atl_change_percentage,
    atl_date,

    last_updated,
    snapshot_date

    from source

),

deduplication_table as ( --para evitar empates
    select *,
    ROW_NUMBER() OVER(PARTITION BY coin_id, snapshot_date ORDER BY last_updated DESC) as rn
    from renamed_table
    QUALIFY rn = 1
)

select * except(rn) from deduplication_table --quitamos la columna de row_number para empates

