execute positioned ~90 ~ ~1717 run function ac:raw/egypt/giza
forceload remove ~0 ~1607 ~255 ~1862
forceload remove ~0 ~1863 ~255 ~1913
forceload remove ~256 ~1607 ~317 ~1862
forceload remove ~256 ~1863 ~317 ~1913
tellraw @a {"text": "Placed Giza Plateau at offset (90, 1717).", "color": "green"}
function ac:_adv
