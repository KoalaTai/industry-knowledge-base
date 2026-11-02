$execute positioned $(x) $(y) $(z) run tp @a ~215 ~45 ~186 180 25
tellraw @a {"text": "Jerusalem", "color": "gold", "bold": true}
tellraw @a {"text": "The Holy Land - 1191, the Third Crusade", "color": "yellow"}
tellraw @a {"text": "Walled city with the Dome of the Rock, al-Aqsa and the Holy Sepulchre.", "color": "white"}
tellraw @a {"text": "Stop 2 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 2
schedule function ac:_tour_next 240t
