$execute positioned $(x) $(y) $(z) run tp @a ~81 ~44 ~972 180 25
tellraw @a {"text": "Havana", "color": "gold", "bold": true}
tellraw @a {"text": "The Caribbean - 1715-1777, the Golden Age of Piracy to the eve of revolution", "color": "yellow"}
tellraw @a {"text": "Castillo del Morro with lighthouse, the cathedral plaza, Spanish streets and a galleon.", "color": "white"}
tellraw @a {"text": "Stop 19 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 19
schedule function ac:_tour_next 240t
