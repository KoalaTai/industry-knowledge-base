$execute positioned $(x) $(y) $(z) run tp @a ~390 ~30 ~799 180 25
tellraw @a {"text": "The Frontier", "color": "gold", "bold": true}
tellraw @a {"text": "Colonial America - 1752-1783, the Seven Years' War and the Revolution", "color": "yellow"}
tellraw @a {"text": "Davenport Homestead manor, a palisaded Kanien'keha:ka longhouse village, a water-powered", "color": "white"}
tellraw @a {"text": "sawmill and forest.", "color": "white"}
tellraw @a {"text": "Stop 17 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 17
schedule function ac:_tour_next 240t
