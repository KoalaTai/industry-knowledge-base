$execute positioned $(x) $(y) $(z) run tp @a ~95 ~35 ~4617 180 25
tellraw @a {"text": "Siege towers, rams and circumvallation", "color": "gold", "bold": true}
tellraw @a {"text": "Assyria, Greece, Rome - 9th century BCE onward", "color": "yellow"}
tellraw @a {"text": "Siege tower on a ramp at a wall, with a ram under its shed.", "color": "white"}
tellraw @a {"text": "Stop 113 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 113
schedule function ac:_tour_next 240t
