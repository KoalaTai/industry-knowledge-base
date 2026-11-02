$execute positioned $(x) $(y) $(z) run tp @a ~370 ~21 ~4694 180 25
tellraw @a {"text": "Woodblock printing, movable type and the press", "color": "gold", "bold": true}
tellraw @a {"text": "China, Korea, Europe - 7th century to 1450", "color": "yellow"}
tellraw @a {"text": "Screw press, type cases, composing stone, drying lines and a scribe's desk.", "color": "white"}
tellraw @a {"text": "Stop 126 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 126
schedule function ac:_tour_next 240t
