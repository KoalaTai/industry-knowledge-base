execute positioned ~ ~ ~ run function ac:terrain/hub_tech/tech_1
forceload remove ~-10 ~135 ~245 ~179
forceload remove ~246 ~135 ~501 ~179
forceload remove ~502 ~135 ~535 ~179
tellraw @a {"text": "Placed Premodern technology terrain at offset (0, 0).", "color": "green"}
function ac:_adv
