$execute positioned $(x) $(y) $(z) run tp @a ~702 ~34 ~1739 180 25
tellraw @a {"text": "Memphis: Temple of Ptah", "color": "gold", "bold": true}
tellraw @a {"text": "Ptolemaic Egypt - 49-43 BCE, reign of Ptolemy XIII and Cleopatra VII", "color": "yellow"}
tellraw @a {"text": "Pylon gateway, obelisks, sphinx avenue, peristyle court, hypostyle hall and sanctuary,", "color": "white"}
tellraw @a {"text": "plus the colossus.", "color": "white"}
tellraw @a {"text": "Stop 39 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 39
schedule function ac:_tour_next 240t
