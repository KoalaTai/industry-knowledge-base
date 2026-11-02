$execute positioned $(x) $(y) $(z) run tp @a ~79 ~28 ~4694 180 25
tellraw @a {"text": "The counterweight trebuchet", "color": "gold", "bold": true}
tellraw @a {"text": "Byzantine, Islamic and Crusader Levant - traction trebuchet from China (4th century BCE) via the Avars (6th century); counterweight type by the 1180s", "color": "yellow"}
tellraw @a {"text": "Counterweight trebuchet and a breached wall.", "color": "white"}
tellraw @a {"text": "Stop 121 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 121
schedule function ac:_tour_next 240t
