$execute positioned $(x) $(y) $(z) run tp @a ~555 ~26 ~2257 180 25
tellraw @a {"text": "Stonehenge", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "Sarsen circle, trilithon horseshoe, avenue and heel stone.", "color": "white"}
tellraw @a {"text": "Stop 50 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 50
schedule function ac:_tour_next 240t
