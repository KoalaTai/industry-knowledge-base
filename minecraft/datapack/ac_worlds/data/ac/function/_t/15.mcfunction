$execute positioned $(x) $(y) $(z) run tp @a ~225 ~44 ~790 180 25
tellraw @a {"text": "New York", "color": "gold", "bold": true}
tellraw @a {"text": "Colonial America - 1752-1783, the Seven Years' War and the Revolution", "color": "yellow"}
tellraw @a {"text": "Fort George at the Battery, Dutch step-gabled houses, Trinity Church and Broadway.", "color": "white"}
tellraw @a {"text": "Stop 16 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 16
schedule function ac:_tour_next 240t
