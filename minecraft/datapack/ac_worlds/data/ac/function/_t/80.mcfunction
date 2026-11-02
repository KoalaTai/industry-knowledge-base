$execute positioned $(x) $(y) $(z) run tp @a ~304 ~34 ~3784 180 25
tellraw @a {"text": "The Wastes", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: Seven Havens - after Korra: the post-cataclysm age of Avatar Pavi", "color": "yellow"}
tellraw @a {"text": "Cracked, lava-veined ground, toppled skyscrapers, ash drifts, corrupted spirit vines and a", "color": "white"}
tellraw @a {"text": "dead portal.", "color": "white"}
tellraw @a {"text": "Stop 81 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 81
schedule function ac:_tour_next 240t
