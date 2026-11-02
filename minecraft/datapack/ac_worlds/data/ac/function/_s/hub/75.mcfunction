execute positioned ~ ~ ~ run function ac:terrain/hub/london
forceload remove ~-10 ~1408 ~245 ~1576
forceload remove ~246 ~1408 ~501 ~1576
forceload remove ~502 ~1408 ~757 ~1576
forceload remove ~758 ~1408 ~850 ~1576
tellraw @a {"text": "Placed Victorian London terrain at offset (0, 0).", "color": "green"}
function ac:_adv
