$execute positioned $(x) $(y) $(z) run tp @a ~132 ~26 ~4544 180 25
tellraw @a {"text": "Hero of Alexandria: the aeolipile and automata", "color": "gold", "bold": true}
tellraw @a {"text": "Roman Egypt - 1st century CE", "color": "yellow"}
tellraw @a {"text": "Hero's steam sphere over a fire, and his automatic temple doors in cut-away.", "color": "white"}
tellraw @a {"text": "Stop 106 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 106
schedule function ac:_tour_next 240t
