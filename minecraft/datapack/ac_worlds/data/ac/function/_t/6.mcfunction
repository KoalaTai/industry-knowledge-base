$execute positioned $(x) $(y) $(z) run tp @a ~420 ~80 ~357 180 25
tellraw @a {"text": "Venice", "color": "gold", "bold": true}
tellraw @a {"text": "Renaissance Italy - 1476-1507", "color": "yellow"}
tellraw @a {"text": "St Mark's five domes, the campanile, the Doge's Palace, the Rialto bridge, canals and", "color": "white"}
tellraw @a {"text": "gondolas.", "color": "white"}
tellraw @a {"text": "Stop 7 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 7
schedule function ac:_tour_next 240t
