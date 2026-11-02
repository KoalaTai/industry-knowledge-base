$execute positioned $(x) $(y) $(z) run tp @a ~513 ~30 ~4548 180 25
tellraw @a {"text": "Treadwheel cranes and the polyspastos", "color": "gold", "bold": true}
tellraw @a {"text": "Greece and Rome - pulleys 6th century BCE Greece; Roman treadwheel crane 1st century BCE", "color": "yellow"}
tellraw @a {"text": "Treadwheel, jib, pulley block and lewis holding a stone.", "color": "white"}
tellraw @a {"text": "Stop 111 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 111
schedule function ac:_tour_next 240t
