$execute positioned $(x) $(y) $(z) run tp @a ~285 ~46 ~4839 180 25
tellraw @a {"text": "Mesoamerican pyramids and Maya astronomy", "color": "gold", "bold": true}
tellraw @a {"text": "Teotihuacan, Maya, Aztec - c. 100 BCE to 1500 CE", "color": "yellow"}
tellraw @a {"text": "Nine-tier pyramid with four stairways and serpent heads.", "color": "white"}
tellraw @a {"text": "Stop 131 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 131
schedule function ac:_tour_next 240t
