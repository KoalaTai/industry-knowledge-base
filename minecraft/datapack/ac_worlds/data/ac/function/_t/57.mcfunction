$execute positioned $(x) $(y) $(z) run tp @a ~70 ~71 ~2709 180 25
tellraw @a {"text": "Azuchi Castle", "color": "gold", "bold": true}
tellraw @a {"text": "Sengoku Japan - 1579-1581, the Azuchi-Momoyama period", "color": "yellow"}
tellraw @a {"text": "Nobunaga's tenshu on its sloped stone base above the lake, with yagura towers and plaster", "color": "white"}
tellraw @a {"text": "walls.", "color": "white"}
tellraw @a {"text": "Stop 58 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 58
schedule function ac:_tour_next 240t
