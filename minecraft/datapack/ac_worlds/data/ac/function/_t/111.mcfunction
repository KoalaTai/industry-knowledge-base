$execute positioned $(x) $(y) $(z) run tp @a ~24 ~41 ~4613 180 25
tellraw @a {"text": "Watermills and the Barbegal cascade", "color": "gold", "bold": true}
tellraw @a {"text": "Rome - vertical watermill described by Vitruvius 1st century BCE; Barbegal early 2nd century CE", "color": "yellow"}
tellraw @a {"text": "Three overshot wheels in cascade, each driving a millstone.", "color": "white"}
tellraw @a {"text": "Stop 112 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 112
schedule function ac:_tour_next 240t
