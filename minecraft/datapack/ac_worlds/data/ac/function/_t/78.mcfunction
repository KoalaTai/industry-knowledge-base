$execute positioned $(x) $(y) $(z) run tp @a ~950 ~64 ~3503 180 25
tellraw @a {"text": "Future Industries", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "Asami's factory, airfield and biplane, test track, and Kuvira's Colossus on its", "color": "white"}
tellraw @a {"text": "scaffolding.", "color": "white"}
tellraw @a {"text": "Stop 79 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 79
schedule function ac:_tour_next 240t
