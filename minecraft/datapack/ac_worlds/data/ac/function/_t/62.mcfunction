$execute positioned $(x) $(y) $(z) run tp @a ~225 ~62 ~2870 180 25
tellraw @a {"text": "Hilltop Burg", "color": "gold", "bold": true}
tellraw @a {"text": "Holy Roman Empire (Hexe) - 16th century, the witch trials", "color": "yellow"}
tellraw @a {"text": "Bergfried keep and curtain wall on a crag above the Black Forest.", "color": "white"}
tellraw @a {"text": "Stop 63 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 63
schedule function ac:_tour_next 240t
