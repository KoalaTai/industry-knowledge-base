$execute positioned $(x) $(y) $(z) run tp @a ~40 ~32 ~4487 180 25
tellraw @a {"text": "Pyramid construction: ramps, sledges and copper tools", "color": "gold", "bold": true}
tellraw @a {"text": "Egypt (Old Kingdom) - c. 2600-2500 BCE", "color": "yellow"}
tellraw @a {"text": "Half-built pyramid with haul ramp, sledge on wetted sand, lever gang and the water-", "color": "white"}
tellraw @a {"text": "levelling trench.", "color": "white"}
tellraw @a {"text": "Stop 96 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 96
schedule function ac:_tour_next 240t
