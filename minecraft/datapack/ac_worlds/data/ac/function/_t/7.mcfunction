$execute positioned $(x) $(y) $(z) run tp @a ~645 ~57 ~437 180 25
tellraw @a {"text": "Rome", "color": "gold", "bold": true}
tellraw @a {"text": "Renaissance Italy - 1476-1507", "color": "yellow"}
tellraw @a {"text": "The Colosseum, the Pantheon with its oculus, Castel Sant'Angelo on the Tiber, a Roman road", "color": "white"}
tellraw @a {"text": "and Forum ruins.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2 m", "color": "gray"}
tellraw @a {"text": "Stop 8 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 8
schedule function ac:_tour_next 240t
