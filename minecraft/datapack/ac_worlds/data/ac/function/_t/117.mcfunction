$execute positioned $(x) $(y) $(z) run tp @a ~360 ~19 ~4625 180 25
tellraw @a {"text": "The astrolabe", "color": "gold", "bold": true}
tellraw @a {"text": "Hellenistic Greece, perfected in the Islamic world - theory from Hipparchus (2nd century BCE); oldest surviving instruments 9th-10th century CE", "color": "yellow"}
tellraw @a {"text": "Giant astrolabe: limb, almucantars, rete, star pointers, alidade.", "color": "white"}
tellraw @a {"text": "Stop 118 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 118
schedule function ac:_tour_next 240t
