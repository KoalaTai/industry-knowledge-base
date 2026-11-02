$execute positioned $(x) $(y) $(z) run tp @a ~780 ~33 ~1568 180 25
tellraw @a {"text": "East End Streets", "color": "gold", "bold": true}
tellraw @a {"text": "Victorian London - 1868", "color": "yellow"}
tellraw @a {"text": "Brick terraces, a covered market, a gin palace and gas lamps.", "color": "white"}
tellraw @a {"text": "Stop 35 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 35
schedule function ac:_tour_next 240t
