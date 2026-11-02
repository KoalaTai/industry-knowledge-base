$execute positioned $(x) $(y) $(z) run tp @a ~152 ~18 ~4702 180 25
tellraw @a {"text": "The heavy plough, the horse collar and three-field rotation", "color": "gold", "bold": true}
tellraw @a {"text": "Medieval Europe - heavy plough spreading from the 7th century; padded horse collar by the 10th; three-field system from the 8th-9th century", "color": "yellow"}
tellraw @a {"text": "Three open fields in rotation with a heavy plough and collared horse.", "color": "white"}
tellraw @a {"text": "Stop 122 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 122
schedule function ac:_tour_next 240t
