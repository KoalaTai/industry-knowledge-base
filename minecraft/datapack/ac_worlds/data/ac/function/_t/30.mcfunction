$execute positioned $(x) $(y) $(z) run tp @a ~90 ~75 ~1548 180 25
tellraw @a {"text": "Westminster", "color": "gold", "bold": true}
tellraw @a {"text": "Victorian London - 1868", "color": "yellow"}
tellraw @a {"text": "The Palace of Westminster river front, Victoria Tower, the clock tower with Big Ben and", "color": "white"}
tellraw @a {"text": "Westminster Bridge.", "color": "white"}
tellraw @a {"text": "Stop 31 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 31
schedule function ac:_tour_next 240t
