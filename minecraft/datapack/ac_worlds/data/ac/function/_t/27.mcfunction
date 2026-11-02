$execute positioned $(x) $(y) $(z) run tp @a ~100 ~43 ~1334 180 25
tellraw @a {"text": "The Great Wall", "color": "gold", "bold": true}
tellraw @a {"text": "Assassin's Creed Chronicles - 1526, 1841 and 1918", "color": "yellow"}
tellraw @a {"text": "A Ming stretch of wall over rolling hills with beacon towers and a palace gate hall.", "color": "white"}
tellraw @a {"text": "Stop 28 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 28
schedule function ac:_tour_next 240t
