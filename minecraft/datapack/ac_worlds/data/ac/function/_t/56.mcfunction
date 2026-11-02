$execute positioned $(x) $(y) $(z) run tp @a ~640 ~26 ~2471 180 25
tellraw @a {"text": "Karkh Bazaar", "color": "gold", "bold": true}
tellraw @a {"text": "Abbasid Baghdad - 861 CE, the Anarchy at Samarra", "color": "yellow"}
tellraw @a {"text": "Covered suq, caravanserai, hammam and a noria waterwheel on the canal.", "color": "white"}
tellraw @a {"text": "Stop 57 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 57
schedule function ac:_tour_next 240t
