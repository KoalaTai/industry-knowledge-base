$execute positioned $(x) $(y) $(z) run tp @a ~511 ~24 ~558 180 25
tellraw @a {"text": "Grand Bazaar", "color": "gold", "bold": true}
tellraw @a {"text": "Ottoman Constantinople - 1511-1512", "color": "yellow"}
tellraw @a {"text": "Vaulted market streets under rows of small domes.", "color": "white"}
tellraw @a {"text": "Stop 14 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 14
schedule function ac:_tour_next 240t
