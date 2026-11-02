$execute positioned $(x) $(y) $(z) run tp @a ~389 ~19 ~4544 180 25
tellraw @a {"text": "Roman roads", "color": "gold", "bold": true}
tellraw @a {"text": "Rome - 312 BCE onward", "color": "yellow"}
tellraw @a {"text": "Four-layer road in cut-away, groma, milestone and a bridge.", "color": "white"}
tellraw @a {"text": "Stop 109 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 109
schedule function ac:_tour_next 240t
