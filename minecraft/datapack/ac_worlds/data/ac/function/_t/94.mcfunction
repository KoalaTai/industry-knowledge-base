$execute positioned $(x) $(y) $(z) run tp @a ~1132 ~81 ~4266 180 25
tellraw @a {"text": "Nocturnal Wonderland", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "Glen Helen Amphitheater, 2018-2019: the sun-face main stage at the foot of the slope and", "color": "white"}
tellraw @a {"text": "the Labyrinth up the hill with its blacklight pillars and hedge maze.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 95 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 95
schedule function ac:_tour_next 240t
