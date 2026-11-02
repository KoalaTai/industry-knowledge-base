$execute positioned $(x) $(y) $(z) run tp @a ~827 ~24 ~1749 180 25
tellraw @a {"text": "The Nile", "color": "gold", "bold": true}
tellraw @a {"text": "Ptolemaic Egypt - 49-43 BCE, reign of Ptolemy XIII and Cleopatra VII", "color": "yellow"}
tellraw @a {"text": "River bank with shadufs, irrigation canals and wheat fields, papyrus marsh, a felucca and", "color": "white"}
tellraw @a {"text": "a Nilometer.", "color": "white"}
tellraw @a {"text": "Stop 40 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 40
schedule function ac:_tour_next 240t
