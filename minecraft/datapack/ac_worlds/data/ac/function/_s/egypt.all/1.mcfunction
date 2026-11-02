execute positioned ~90 ~ ~110 run function ac:raw/egypt/giza
forceload remove ~0 ~0 ~255 ~255
forceload remove ~0 ~256 ~255 ~306
forceload remove ~256 ~0 ~317 ~255
forceload remove ~256 ~256 ~317 ~306
tellraw @a {"text": "Placed Giza Plateau at offset (90, 110).", "color": "green"}
function ac:_adv
