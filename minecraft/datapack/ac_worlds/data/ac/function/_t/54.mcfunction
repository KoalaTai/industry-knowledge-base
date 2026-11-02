$execute positioned $(x) $(y) $(z) run tp @a ~350 ~59 ~2489 180 25
tellraw @a {"text": "Great Mosque of Samarra", "color": "gold", "bold": true}
tellraw @a {"text": "Abbasid Baghdad - 861 CE, the Anarchy at Samarra", "color": "yellow"}
tellraw @a {"text": "The walled mosque and the Malwiya spiral minaret on the Tigris.", "color": "white"}
tellraw @a {"text": "Stop 55 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 55
schedule function ac:_tour_next 240t
