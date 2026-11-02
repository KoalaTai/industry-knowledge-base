$execute positioned $(x) $(y) $(z) run tp @a ~840 ~54 ~327 180 25
tellraw @a {"text": "San Gimignano", "color": "gold", "bold": true}
tellraw @a {"text": "Renaissance Italy - 1476-1507", "color": "yellow"}
tellraw @a {"text": "Fourteen family towers inside the town wall.", "color": "white"}
tellraw @a {"text": "Stop 9 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 9
schedule function ac:_tour_next 240t
