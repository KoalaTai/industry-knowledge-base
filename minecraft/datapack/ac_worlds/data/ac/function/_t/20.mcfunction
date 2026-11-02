$execute positioned $(x) $(y) $(z) run tp @a ~422 ~32 ~962 180 25
tellraw @a {"text": "Kingston", "color": "gold", "bold": true}
tellraw @a {"text": "The Caribbean - 1715-1777, the Golden Age of Piracy to the eve of revolution", "color": "yellow"}
tellraw @a {"text": "A Jamaican sugar plantation: cane fields, windmill, boiling house, great house and", "color": "white"}
tellraw @a {"text": "quarters.", "color": "white"}
tellraw @a {"text": "Stop 21 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 21
schedule function ac:_tour_next 240t
