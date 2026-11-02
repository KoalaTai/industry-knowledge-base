execute positioned ~2106 ~ ~150 run function ac:raw/insomniac/edc_grounds
forceload remove ~1956 ~0 ~2211 ~255
forceload remove ~1956 ~256 ~2211 ~300
forceload remove ~2212 ~0 ~2256 ~255
forceload remove ~2212 ~256 ~2256 ~300
tellraw @a {"text": "Placed EDC Las Vegas grounds at offset (2106, 150).", "color": "green"}
function ac:_adv
