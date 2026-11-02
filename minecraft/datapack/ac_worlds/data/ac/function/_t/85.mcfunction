$execute positioned $(x) $(y) $(z) run tp @a ~776 ~50 ~4005 180 25
tellraw @a {"text": "neonGARDEN", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The 2024 megastructure: enclosed truss hall, LED side bands, the hanging light cube and", "color": "white"}
tellraw @a {"text": "CO2 smoke towers.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 86 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 86
schedule function ac:_tour_next 240t
