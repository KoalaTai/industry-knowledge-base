$execute positioned $(x) $(y) $(z) run tp @a ~519 ~28 ~4431 180 25
tellraw @a {"text": "Archimedes' screw", "color": "gold", "bold": true}
tellraw @a {"text": "Hellenistic Greece / Ptolemaic Egypt - 3rd century BCE", "color": "yellow"}
tellraw @a {"text": "Inclined screw in a casing lifting water from a pool to a channel.", "color": "white"}
tellraw @a {"text": "Stop 103 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 103
schedule function ac:_tour_next 240t
