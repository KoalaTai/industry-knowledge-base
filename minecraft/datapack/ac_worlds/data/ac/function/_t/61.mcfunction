$execute positioned $(x) $(y) $(z) run tp @a ~70 ~46 ~2880 180 25
tellraw @a {"text": "Free Imperial Town", "color": "gold", "bold": true}
tellraw @a {"text": "Holy Roman Empire (Hexe) - 16th century, the witch trials", "color": "yellow"}
tellraw @a {"text": "Walled half-timbered town with Rathaus, market well, church spire, and the pyre field", "color": "white"}
tellraw @a {"text": "outside the gate.", "color": "white"}
tellraw @a {"text": "Stop 62 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 62
schedule function ac:_tour_next 240t
