$execute positioned $(x) $(y) $(z) run tp @a ~265 ~78 ~3503 180 25
tellraw @a {"text": "Pro-bending Arena", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "Golden dome on the bay, tiered stands, the ring over water with its zones.", "color": "white"}
tellraw @a {"text": "Stop 75 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 75
schedule function ac:_tour_next 240t
