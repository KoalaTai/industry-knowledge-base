$execute positioned $(x) $(y) $(z) run tp @a ~535 ~25 ~2659 180 25
tellraw @a {"text": "Shinto Shrine", "color": "gold", "bold": true}
tellraw @a {"text": "Sengoku Japan - 1579-1581, the Azuchi-Momoyama period", "color": "yellow"}
tellraw @a {"text": "Torii, stone lanterns, water basin, haiden and honden among cherry trees.", "color": "white"}
tellraw @a {"text": "Stop 61 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 61
schedule function ac:_tour_next 240t
