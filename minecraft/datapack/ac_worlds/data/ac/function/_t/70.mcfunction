$execute positioned $(x) $(y) $(z) run tp @a ~1255 ~44 ~3041 180 25
tellraw @a {"text": "Wan Shi Tong's Library", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Only the spire shows above the desert; below, the great dome with four gallery levels, the", "color": "white"}
tellraw @a {"text": "owl spirit, the planetarium and the catalogue room.", "color": "white"}
tellraw @a {"text": "Stop 71 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 71
schedule function ac:_tour_next 240t
