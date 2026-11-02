$execute positioned $(x) $(y) $(z) run tp @a ~119 ~26 ~4439 180 25
tellraw @a {"text": "Shaduf", "color": "gold", "bold": true}
tellraw @a {"text": "Egypt and Mesopotamia - attested c. 2000 BCE Mesopotamia; Egypt by the New Kingdom (c. 1500 BCE)", "color": "yellow"}
tellraw @a {"text": "Three shadufs lifting water in series from a canal to a terrace garden.", "color": "white"}
tellraw @a {"text": "Stop 97 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 97
schedule function ac:_tour_next 240t
