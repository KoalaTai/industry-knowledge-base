$execute positioned $(x) $(y) $(z) run tp @a ~60 ~58 ~176 180 25
tellraw @a {"text": "Masyaf", "color": "gold", "bold": true}
tellraw @a {"text": "The Holy Land - 1191, the Third Crusade", "color": "yellow"}
tellraw @a {"text": "The Assassin fortress on its crag with keep, library wing, leap-of-faith tower and", "color": "white"}
tellraw @a {"text": "haystack, above the village.", "color": "white"}
tellraw @a {"text": "Stop 1 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 1
schedule function ac:_tour_next 240t
