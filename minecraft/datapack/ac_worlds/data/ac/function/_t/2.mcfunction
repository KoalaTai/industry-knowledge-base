$execute positioned $(x) $(y) $(z) run tp @a ~375 ~41 ~156 180 25
tellraw @a {"text": "Acre", "color": "gold", "bold": true}
tellraw @a {"text": "The Holy Land - 1191, the Third Crusade", "color": "yellow"}
tellraw @a {"text": "Crusader port: Hospitaller fortress and vaulted refectory, harbour, breakwater and the", "color": "white"}
tellraw @a {"text": "Tower of Flies.", "color": "white"}
tellraw @a {"text": "Stop 3 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 3
schedule function ac:_tour_next 240t
