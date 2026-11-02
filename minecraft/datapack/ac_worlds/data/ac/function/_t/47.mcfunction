$execute positioned $(x) $(y) $(z) run tp @a ~245 ~34 ~2297 180 25
tellraw @a {"text": "Lunden", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "Saxon houses among ruined Roman walls and amphitheatre, a wooden bridge and the market", "color": "white"}
tellraw @a {"text": "strand.", "color": "white"}
tellraw @a {"text": "Stop 48 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 48
schedule function ac:_tour_next 240t
