execute positioned ~ ~ ~ run function ac:terrain/hub_insomniac_events/insomniac_2
forceload remove ~-10 ~255 ~245 ~510
forceload remove ~-10 ~511 ~245 ~575
forceload remove ~246 ~255 ~501 ~510
forceload remove ~246 ~511 ~501 ~575
forceload remove ~502 ~255 ~757 ~510
forceload remove ~502 ~511 ~757 ~575
forceload remove ~758 ~255 ~1013 ~510
forceload remove ~758 ~511 ~1013 ~575
forceload remove ~1014 ~255 ~1252 ~510
forceload remove ~1014 ~511 ~1252 ~575
tellraw @a {"text": "Placed Insomniac Events terrain at offset (0, 0).", "color": "green"}
function ac:_adv
