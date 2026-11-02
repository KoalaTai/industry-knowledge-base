$execute positioned $(x) $(y) $(z) run tp @a ~441 ~33 ~4738 180 25
tellraw @a {"text": "From motte-and-bailey to the concentric castle", "color": "gold", "bold": true}
tellraw @a {"text": "Norman and Crusader Europe - 11th-13th centuries", "color": "yellow"}
tellraw @a {"text": "Motte with timber tower, ditch, palisaded bailey with hall and chapel.", "color": "white"}
tellraw @a {"text": "Stop 127 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 127
schedule function ac:_tour_next 240t
