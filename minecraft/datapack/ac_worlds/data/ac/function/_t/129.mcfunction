$execute positioned $(x) $(y) $(z) run tp @a ~200 ~21 ~4819 180 25
tellraw @a {"text": "Aztec chinampas", "color": "gold", "bold": true}
tellraw @a {"text": "Aztec (Mexica) - 14th-16th centuries", "color": "yellow"}
tellraw @a {"text": "Raised lake fields with wattle fences, willows, canals and a canoe.", "color": "white"}
tellraw @a {"text": "Stop 130 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 130
schedule function ac:_tour_next 240t
