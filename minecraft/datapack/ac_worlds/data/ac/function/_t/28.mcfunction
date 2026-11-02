$execute positioned $(x) $(y) $(z) run tp @a ~285 ~32 ~1407 180 25
tellraw @a {"text": "Amritsar", "color": "gold", "bold": true}
tellraw @a {"text": "Assassin's Creed Chronicles - 1526, 1841 and 1918", "color": "yellow"}
tellraw @a {"text": "The Golden Temple in its sacred pool with the causeway, plus a stepwell.", "color": "white"}
tellraw @a {"text": "Stop 29 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 29
schedule function ac:_tour_next 240t
