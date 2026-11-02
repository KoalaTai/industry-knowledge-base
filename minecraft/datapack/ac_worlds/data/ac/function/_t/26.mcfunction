$execute positioned $(x) $(y) $(z) run tp @a ~615 ~63 ~1133 180 25
tellraw @a {"text": "Streets of the Revolution", "color": "gold", "bold": true}
tellraw @a {"text": "Revolutionary Paris - 1789-1794", "color": "yellow"}
tellraw @a {"text": "Tall houses, a barricade, the guillotine and a tethered Montgolfier balloon.", "color": "white"}
tellraw @a {"text": "Stop 27 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 27
schedule function ac:_tour_next 240t
