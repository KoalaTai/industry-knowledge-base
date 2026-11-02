$execute positioned $(x) $(y) $(z) run tp @a ~461 ~22 ~4548 180 25
tellraw @a {"text": "Hypocaust heating and the public bath", "color": "gold", "bold": true}
tellraw @a {"text": "Rome - 1st century BCE onward", "color": "yellow"}
tellraw @a {"text": "Bath cut-away: furnace, pilae, box-tile walls, plunge, roof flues.", "color": "white"}
tellraw @a {"text": "Stop 110 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 110
schedule function ac:_tour_next 240t
