$execute positioned $(x) $(y) $(z) run tp @a ~198 ~24 ~4457 180 25
tellraw @a {"text": "Obelisk quarrying and raising", "color": "gold", "bold": true}
tellraw @a {"text": "Egypt (New Kingdom) - c. 1500-1200 BCE", "color": "yellow"}
tellraw @a {"text": "The Unfinished Obelisk in its trench with dolerite pounders, and one being tipped into a", "color": "white"}
tellraw @a {"text": "sand pit.", "color": "white"}
tellraw @a {"text": "Stop 98 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 98
schedule function ac:_tour_next 240t
