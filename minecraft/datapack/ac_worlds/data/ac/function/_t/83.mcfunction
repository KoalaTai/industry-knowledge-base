$execute positioned $(x) $(y) $(z) run tp @a ~351 ~45 ~4005 180 25
tellraw @a {"text": "cosmicMEADOW", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The 2023-2024 wide LED wall under a truss canopy, with giant daisies and sunflowers along", "color": "white"}
tellraw @a {"text": "the meadow.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 84 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 84
schedule function ac:_tour_next 240t
