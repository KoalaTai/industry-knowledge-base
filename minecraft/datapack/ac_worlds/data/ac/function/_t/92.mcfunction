$execute positioned $(x) $(y) $(z) run tp @a ~640 ~63 ~4286 180 25
tellraw @a {"text": "NOS Events Center", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "San Bernardino dressed for Beyond Wonderland SoCal 2025: the Queen's Domain megastructure,", "color": "white"}
tellraw @a {"text": "Mad Hatter's deck-of-cards castle on the dirt speedway, Damon Hall and the grandstand.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2 m", "color": "gray"}
tellraw @a {"text": "Stop 93 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 93
schedule function ac:_tour_next 240t
