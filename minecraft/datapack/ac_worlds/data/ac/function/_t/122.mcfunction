$execute positioned $(x) $(y) $(z) run tp @a ~222 ~32 ~4700 180 25
tellraw @a {"text": "The European post mill and tower mill", "color": "gold", "bold": true}
tellraw @a {"text": "Medieval Europe - post mill from the 1180s; tower mill from the 14th century", "color": "yellow"}
tellraw @a {"text": "A post mill beside a tower mill.", "color": "white"}
tellraw @a {"text": "Stop 123 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 123
schedule function ac:_tour_next 240t
