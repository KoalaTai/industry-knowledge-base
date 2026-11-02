$execute positioned $(x) $(y) $(z) run tp @a ~440 ~47 ~1568 180 25
tellraw @a {"text": "Tower of London", "color": "gold", "bold": true}
tellraw @a {"text": "Victorian London - 1868", "color": "yellow"}
tellraw @a {"text": "The White Tower inside two curtain walls and the moat, with Traitors' Gate on the Thames.", "color": "white"}
tellraw @a {"text": "Stop 33 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 33
schedule function ac:_tour_next 240t
