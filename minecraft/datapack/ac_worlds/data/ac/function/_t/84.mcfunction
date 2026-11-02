$execute positioned $(x) $(y) $(z) run tp @a ~571 ~76 ~3983 180 25
tellraw @a {"text": "circuitGROUNDS", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The 2016-2024 panoramic design: five LED-hung truss arches spanning the crowd like a", "color": "white"}
tellraw @a {"text": "spaceship frame.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 85 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 85
schedule function ac:_tour_next 240t
