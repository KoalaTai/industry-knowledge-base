$execute positioned $(x) $(y) $(z) run tp @a ~700 ~76 ~2337 180 25
tellraw @a {"text": "Asgard", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "The golden hall on its rock, the Bifrost rainbow bridge, Yggdrasil and the well of Urd.", "color": "white"}
tellraw @a {"text": "Stop 51 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 51
schedule function ac:_tour_next 240t
