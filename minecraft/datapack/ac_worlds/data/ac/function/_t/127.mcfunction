$execute positioned $(x) $(y) $(z) run tp @a ~30 ~22 ~4799 180 25
tellraw @a {"text": "Inca suspension bridges and the Qhapaq Nan", "color": "gold", "bold": true}
tellraw @a {"text": "Inca - 15th-16th centuries; the Q'eswachaka is rewoven every year to this day", "color": "yellow"}
tellraw @a {"text": "Grass-rope suspension bridge over a gorge on the Inca road.", "color": "white"}
tellraw @a {"text": "Stop 128 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 128
schedule function ac:_tour_next 240t
