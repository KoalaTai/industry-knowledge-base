execute positioned ~ ~ ~ run function ac:terrain/hub_avatar/atla
forceload remove ~-10 ~6 ~245 ~254
forceload remove ~246 ~6 ~501 ~254
forceload remove ~502 ~6 ~757 ~254
forceload remove ~758 ~6 ~1013 ~254
forceload remove ~1014 ~6 ~1269 ~254
forceload remove ~1270 ~6 ~1325 ~254
tellraw @a {"text": "Placed Avatar: The Last Airbender terrain at offset (0, 0).", "color": "green"}
function ac:_adv
