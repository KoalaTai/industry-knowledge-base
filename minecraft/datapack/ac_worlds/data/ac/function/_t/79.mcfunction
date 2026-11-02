$execute positioned $(x) $(y) $(z) run tp @a ~90 ~41 ~3784 180 25
tellraw @a {"text": "A Haven", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: Seven Havens - after Korra: the post-cataclysm age of Avatar Pavi", "color": "yellow"}
tellraw @a {"text": "Concentric earthbent walls with twelve towers, terraced farms, a ring of houses and the", "color": "white"}
tellraw @a {"text": "spirit crystal core in its moat; wastes and craters outside the gate.", "color": "white"}
tellraw @a {"text": "Stop 80 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 80
schedule function ac:_tour_next 240t
