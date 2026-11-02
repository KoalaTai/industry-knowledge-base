$execute positioned $(x) $(y) $(z) run tp @a ~60 ~68 ~1163 180 25
tellraw @a {"text": "Notre-Dame", "color": "gold", "bold": true}
tellraw @a {"text": "Revolutionary Paris - 1789-1794", "color": "yellow"}
tellraw @a {"text": "The cathedral with flying buttresses, rose window and spire on the Ile de la Cite, with", "color": "white"}
tellraw @a {"text": "bridges over the Seine.", "color": "white"}
tellraw @a {"text": "Stop 24 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 24
schedule function ac:_tour_next 240t
