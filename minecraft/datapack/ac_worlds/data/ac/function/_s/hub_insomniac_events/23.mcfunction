execute positioned ~355 ~ ~415 run function ac:raw/insomniac/edc_grounds
forceload remove ~205 ~265 ~460 ~520
forceload remove ~205 ~521 ~460 ~565
forceload remove ~461 ~265 ~505 ~520
forceload remove ~461 ~521 ~505 ~565
tellraw @a {"text": "Placed EDC Las Vegas grounds at offset (355, 415).", "color": "green"}
function ac:_adv
