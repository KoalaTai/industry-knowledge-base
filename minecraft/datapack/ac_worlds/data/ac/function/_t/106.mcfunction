$execute positioned $(x) $(y) $(z) run tp @a ~213 ~37 ~4548 180 25
tellraw @a {"text": "Aqueducts", "color": "gold", "bold": true}
tellraw @a {"text": "Rome - Aqua Appia 312 BCE to Aqua Alexandrina 226 CE", "color": "yellow"}
tellraw @a {"text": "Two-tier arcade into a castellum with three lead mains.", "color": "white"}
tellraw @a {"text": "Stop 107 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 107
schedule function ac:_tour_next 240t
