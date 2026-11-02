$execute positioned $(x) $(y) $(z) run tp @a ~509 ~27 ~3764 180 25
tellraw @a {"text": "Seven Havens Map", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: Seven Havens - after Korra: the post-cataclysm age of Avatar Pavi", "color": "yellow"}
tellraw @a {"text": "1:12 model of the scarred continent with seven walled havens linked by roads around the", "color": "white"}
tellraw @a {"text": "epicentre.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 12 m", "color": "gray"}
tellraw @a {"text": "Stop 82 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 82
schedule function ac:_tour_next 240t
