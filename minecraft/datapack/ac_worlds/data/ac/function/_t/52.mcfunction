$execute positioned $(x) $(y) $(z) run tp @a ~80 ~51 ~2538 180 25
tellraw @a {"text": "The Round City", "color": "gold", "bold": true}
tellraw @a {"text": "Abbasid Baghdad - 861 CE, the Anarchy at Samarra", "color": "yellow"}
tellraw @a {"text": "Al-Mansur's double circular wall with four gates, the Golden Gate palace and the great", "color": "white"}
tellraw @a {"text": "mosque.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 4 m", "color": "gray"}
tellraw @a {"text": "Stop 53 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 53
schedule function ac:_tour_next 240t
