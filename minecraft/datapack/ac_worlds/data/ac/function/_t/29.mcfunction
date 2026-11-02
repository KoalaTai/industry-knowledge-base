$execute positioned $(x) $(y) $(z) run tp @a ~450 ~46 ~1374 180 25
tellraw @a {"text": "Petrograd", "color": "gold", "bold": true}
tellraw @a {"text": "Assassin's Creed Chronicles - 1526, 1841 and 1918", "color": "yellow"}
tellraw @a {"text": "Kremlin-style wall, an onion-domed cathedral, the Winter Palace facade and an armoured", "color": "white"}
tellraw @a {"text": "train.", "color": "white"}
tellraw @a {"text": "Stop 30 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 30
schedule function ac:_tour_next 240t
