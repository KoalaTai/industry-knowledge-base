$execute positioned $(x) $(y) $(z) run tp @a ~615 ~55 ~1558 180 25
tellraw @a {"text": "The Thames and the Railway", "color": "gold", "bold": true}
tellraw @a {"text": "Victorian London - 1868", "color": "yellow"}
tellraw @a {"text": "A brick railway viaduct with a steam locomotive and carriages, warehouses, chimney and", "color": "white"}
tellraw @a {"text": "barges.", "color": "white"}
tellraw @a {"text": "Stop 34 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 34
schedule function ac:_tour_next 240t
