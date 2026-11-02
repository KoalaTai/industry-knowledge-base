$execute positioned $(x) $(y) $(z) run tp @a ~412 ~84 ~1759 180 25
tellraw @a {"text": "Alexandria: Pharos and Library", "color": "gold", "bold": true}
tellraw @a {"text": "Ptolemaic Egypt - 49-43 BCE, reign of Ptolemy XIII and Cleopatra VII", "color": "yellow"}
tellraw @a {"text": "The three-tier Pharos lighthouse on its island mole, and the Mouseion library hall lined", "color": "white"}
tellraw @a {"text": "with scroll racks.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2 m", "color": "gray"}
tellraw @a {"text": "Stop 37 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 37
schedule function ac:_tour_next 240t
