$execute positioned $(x) $(y) $(z) run tp @a ~1636 ~73 ~4010 180 25
tellraw @a {"text": "bionicJUNGLE", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The 2022 house stage: a giant tree with the LED wall in its trunk, buttress roots, vines,", "color": "white"}
tellraw @a {"text": "butterflies and mushrooms.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 90 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 90
schedule function ac:_tour_next 240t
