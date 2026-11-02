$execute positioned $(x) $(y) $(z) run tp @a ~981 ~58 ~4020 180 25
tellraw @a {"text": "bassPOD", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The 2022-2025 geodesic half-dome with its heavy LED front, bass stacks, and the skull and", "color": "white"}
tellraw @a {"text": "claws over the booth.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 87 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 87
schedule function ac:_tour_next 240t
