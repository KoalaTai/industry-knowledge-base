$execute positioned $(x) $(y) $(z) run tp @a ~70 ~31 ~2287 180 25
tellraw @a {"text": "Ravensthorpe", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "The riverside settlement: longhouse, barracks, forge, seer's hut, dock and longship inside", "color": "white"}
tellraw @a {"text": "a palisade.", "color": "white"}
tellraw @a {"text": "Stop 47 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 47
schedule function ac:_tour_next 240t
