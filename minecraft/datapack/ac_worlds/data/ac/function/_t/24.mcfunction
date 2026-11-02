$execute positioned $(x) $(y) $(z) run tp @a ~205 ~35 ~1133 180 25
tellraw @a {"text": "The Bastille", "color": "gold", "bold": true}
tellraw @a {"text": "Revolutionary Paris - 1789-1794", "color": "yellow"}
tellraw @a {"text": "The eight-towered fortress prison in its moat, with the faubourg Saint-Antoine around it.", "color": "white"}
tellraw @a {"text": "Stop 25 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 25
schedule function ac:_tour_next 240t
