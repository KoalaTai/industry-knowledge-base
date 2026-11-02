$execute positioned $(x) $(y) $(z) run tp @a ~772 ~72 ~3523 180 25
tellraw @a {"text": "Spirit Wilds", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "The Tree of Time, glowing spirit forest, floating islets, the Southern portal and Iroh's", "color": "white"}
tellraw @a {"text": "tea garden.", "color": "white"}
tellraw @a {"text": "Stop 78 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 78
schedule function ac:_tour_next 240t
