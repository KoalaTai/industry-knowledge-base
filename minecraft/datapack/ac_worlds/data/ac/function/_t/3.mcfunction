$execute positioned $(x) $(y) $(z) run tp @a ~535 ~57 ~166 180 25
tellraw @a {"text": "Damascus", "color": "gold", "bold": true}
tellraw @a {"text": "The Holy Land - 1191, the Third Crusade", "color": "yellow"}
tellraw @a {"text": "The Umayyad Mosque with three minarets and a 120-block covered souk.", "color": "white"}
tellraw @a {"text": "Stop 4 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 4
schedule function ac:_tour_next 240t
