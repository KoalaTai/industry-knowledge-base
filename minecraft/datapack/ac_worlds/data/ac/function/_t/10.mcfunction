$execute positioned $(x) $(y) $(z) run tp @a ~195 ~76 ~578 180 25
tellraw @a {"text": "Galata Tower", "color": "gold", "bold": true}
tellraw @a {"text": "Ottoman Constantinople - 1511-1512", "color": "yellow"}
tellraw @a {"text": "The Genoese tower on its hill above the Golden Horn with the ferry quay.", "color": "white"}
tellraw @a {"text": "Stop 11 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 11
schedule function ac:_tour_next 240t
