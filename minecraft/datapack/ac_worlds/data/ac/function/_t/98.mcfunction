$execute positioned $(x) $(y) $(z) run tp @a ~293 ~40 ~4473 180 25
tellraw @a {"text": "Ziggurats and fired brick", "color": "gold", "bold": true}
tellraw @a {"text": "Sumer, Babylon - Ur ziggurat c. 2100 BCE", "color": "yellow"}
tellraw @a {"text": "Ur-type ziggurat: fired-brick skin, weep holes, triple stair and shrine.", "color": "white"}
tellraw @a {"text": "Stop 99 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 99
schedule function ac:_tour_next 240t
