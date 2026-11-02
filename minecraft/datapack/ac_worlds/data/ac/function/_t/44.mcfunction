$execute positioned $(x) $(y) $(z) run tp @a ~555 ~29 ~2016 180 25
tellraw @a {"text": "Athenian Trireme", "color": "gold", "bold": true}
tellraw @a {"text": "Classical Greece - 431-422 BCE, the Peloponnesian War", "color": "yellow"}
tellraw @a {"text": "A three-banked warship with bronze ram at a stone mole.", "color": "white"}
tellraw @a {"text": "Stop 45 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 45
schedule function ac:_tour_next 240t
