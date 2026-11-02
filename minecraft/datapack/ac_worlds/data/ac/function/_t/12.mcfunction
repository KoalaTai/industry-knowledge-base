$execute positioned $(x) $(y) $(z) run tp @a ~405 ~24 ~558 180 25
tellraw @a {"text": "Derinkuyu", "color": "gold", "bold": true}
tellraw @a {"text": "Ottoman Constantinople - 1511-1512", "color": "yellow"}
tellraw @a {"text": "Cappadocian underground city carved seven levels below the fairy chimneys.", "color": "white"}
tellraw @a {"text": "Stop 13 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 13
schedule function ac:_tour_next 240t
