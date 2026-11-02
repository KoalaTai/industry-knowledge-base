$execute positioned $(x) $(y) $(z) run tp @a ~20 ~18 ~4544 180 25
tellraw @a {"text": "Antikythera mechanism", "color": "gold", "bold": true}
tellraw @a {"text": "Hellenistic Greece - c. 150-60 BCE", "color": "yellow"}
tellraw @a {"text": "Exploded relief: zodiac dial, gear train, crank and pointer.", "color": "white"}
tellraw @a {"text": "Stop 104 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 104
schedule function ac:_tour_next 240t
