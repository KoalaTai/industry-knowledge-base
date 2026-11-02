$execute positioned $(x) $(y) $(z) run tp @a ~577 ~39 ~952 180 25
tellraw @a {"text": "Port-au-Prince", "color": "gold", "bold": true}
tellraw @a {"text": "The Caribbean - 1715-1777, the Golden Age of Piracy to the eve of revolution", "color": "yellow"}
tellraw @a {"text": "The French fort and harbour of Saint-Domingue (Freedom Cry).", "color": "white"}
tellraw @a {"text": "Stop 22 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 22
schedule function ac:_tour_next 240t
