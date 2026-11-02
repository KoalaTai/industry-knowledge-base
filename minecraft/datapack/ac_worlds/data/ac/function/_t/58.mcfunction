$execute positioned $(x) $(y) $(z) run tp @a ~235 ~55 ~2699 180 25
tellraw @a {"text": "Kyoto", "color": "gold", "bold": true}
tellraw @a {"text": "Sengoku Japan - 1579-1581, the Azuchi-Momoyama period", "color": "yellow"}
tellraw @a {"text": "The Golden Pavilion on its pond, a five-storey pagoda, a torii path and the Ryoan-ji dry", "color": "white"}
tellraw @a {"text": "garden.", "color": "white"}
tellraw @a {"text": "Stop 59 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 59
schedule function ac:_tour_next 240t
