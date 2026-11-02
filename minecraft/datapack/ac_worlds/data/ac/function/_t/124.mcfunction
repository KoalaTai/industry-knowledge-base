$execute positioned $(x) $(y) $(z) run tp @a ~319 ~38 ~4690 180 25
tellraw @a {"text": "Gothic engineering: pointed arch, rib vault, flying buttress", "color": "gold", "bold": true}
tellraw @a {"text": "Medieval France and Europe - 12th-13th centuries", "color": "yellow"}
tellraw @a {"text": "One nave bay in section: pointed rib vault, clerestory, flyers, pinnacles.", "color": "white"}
tellraw @a {"text": "Stop 125 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 125
schedule function ac:_tour_next 240t
