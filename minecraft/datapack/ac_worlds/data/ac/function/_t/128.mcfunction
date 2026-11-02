$execute positioned $(x) $(y) $(z) run tp @a ~115 ~14 ~4839 180 25
tellraw @a {"text": "Andean terraces (andenes) and Moray", "color": "gold", "bold": true}
tellraw @a {"text": "Inca and earlier Andean cultures - pre-Inca to 1530s", "color": "yellow"}
tellraw @a {"text": "Moray-style concentric terraced bowl with irrigation channel.", "color": "white"}
tellraw @a {"text": "Stop 129 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 129
schedule function ac:_tour_next 240t
