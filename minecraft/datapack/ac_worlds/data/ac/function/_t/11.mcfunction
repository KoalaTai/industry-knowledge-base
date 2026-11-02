$execute positioned $(x) $(y) $(z) run tp @a ~305 ~33 ~638 180 25
tellraw @a {"text": "Theodosian Walls", "color": "gold", "bold": true}
tellraw @a {"text": "Ottoman Constantinople - 1511-1512", "color": "yellow"}
tellraw @a {"text": "Triple land walls: moat, outer wall, inner wall with brick bands and a gate.", "color": "white"}
tellraw @a {"text": "Stop 12 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 12
schedule function ac:_tour_next 240t
