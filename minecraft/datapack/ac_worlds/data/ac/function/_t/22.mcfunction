$execute positioned $(x) $(y) $(z) run tp @a ~742 ~39 ~962 180 25
tellraw @a {"text": "New Orleans", "color": "gold", "bold": true}
tellraw @a {"text": "The Caribbean - 1715-1777, the Golden Age of Piracy to the eve of revolution", "color": "yellow"}
tellraw @a {"text": "French Quarter galleries, St Louis church, and the cypress bayou (Liberation).", "color": "white"}
tellraw @a {"text": "Stop 23 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 23
schedule function ac:_tour_next 240t
