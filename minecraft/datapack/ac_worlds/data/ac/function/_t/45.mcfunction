$execute positioned $(x) $(y) $(z) run tp @a ~700 ~36 ~2136 180 25
tellraw @a {"text": "Atlantis", "color": "gold", "bold": true}
tellraw @a {"text": "Classical Greece - 431-422 BCE, the Peloponnesian War", "color": "yellow"}
tellraw @a {"text": "Plato's concentric rings of land and sea around the temple of Poseidon.", "color": "white"}
tellraw @a {"text": "Stop 46 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 46
schedule function ac:_tour_next 240t
