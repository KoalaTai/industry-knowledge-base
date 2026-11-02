$execute positioned $(x) $(y) $(z) run tp @a ~60 ~68 ~608 180 25
tellraw @a {"text": "Hagia Sophia", "color": "gold", "bold": true}
tellraw @a {"text": "Ottoman Constantinople - 1511-1512", "color": "yellow"}
tellraw @a {"text": "Justinian's domed church of 537 with its pendentive dome, half domes and Ottoman minarets.", "color": "white"}
tellraw @a {"text": "Stop 10 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 10
schedule function ac:_tour_next 240t
