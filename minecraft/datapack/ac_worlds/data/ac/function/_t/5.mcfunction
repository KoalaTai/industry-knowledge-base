$execute positioned $(x) $(y) $(z) run tp @a ~255 ~41 ~347 180 25
tellraw @a {"text": "Monteriggioni", "color": "gold", "bold": true}
tellraw @a {"text": "Renaissance Italy - 1476-1507", "color": "yellow"}
tellraw @a {"text": "The hill town's ring wall with fourteen towers, the Villa Auditore and the square.", "color": "white"}
tellraw @a {"text": "Stop 6 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 6
schedule function ac:_tour_next 240t
