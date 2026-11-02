execute positioned ~ ~ ~ run function ac:raw/insomniac/edc_grounds
forceload remove ~-150 ~-150 ~105 ~105
forceload remove ~-150 ~106 ~105 ~150
forceload remove ~106 ~-150 ~150 ~105
forceload remove ~106 ~106 ~150 ~150
tellraw @a {"text": "Placed EDC Las Vegas grounds at offset (0, 0).", "color": "green"}
function ac:_adv
