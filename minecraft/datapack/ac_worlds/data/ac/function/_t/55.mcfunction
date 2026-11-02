$execute positioned $(x) $(y) $(z) run tp @a ~495 ~63 ~2498 180 25
tellraw @a {"text": "Alamut", "color": "gold", "bold": true}
tellraw @a {"text": "Abbasid Baghdad - 861 CE, the Anarchy at Samarra", "color": "yellow"}
tellraw @a {"text": "The Hidden Ones' fortress on its rock with the single stair path.", "color": "white"}
tellraw @a {"text": "Stop 56 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 56
schedule function ac:_tour_next 240t
