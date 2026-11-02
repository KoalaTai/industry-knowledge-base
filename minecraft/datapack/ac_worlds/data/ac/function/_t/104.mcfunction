$execute positioned $(x) $(y) $(z) run tp @a ~79 ~22 ~4544 180 25
tellraw @a {"text": "Torsion catapults", "color": "gold", "bold": true}
tellraw @a {"text": "Greece (Syracuse, Macedon), Rome - gastraphetes c. 399 BCE; torsion engines from c. 340 BCE", "color": "yellow"}
tellraw @a {"text": "Torsion ballista and onager.", "color": "white"}
tellraw @a {"text": "Stop 105 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 105
schedule function ac:_tour_next 240t
