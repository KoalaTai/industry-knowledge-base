$execute positioned $(x) $(y) $(z) run tp @a ~355 ~75 ~4366 180 25
tellraw @a {"text": "EDC Las Vegas grounds", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The Las Vegas Motor Speedway in miniature, 2024 layout: tri-oval, nine stages, entrance", "color": "white"}
tellraw @a {"text": "with the EDC sign, Ferris wheel, rides, and the Parliament, Boombox and Kalliope art cars.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 5 m", "color": "gray"}
tellraw @a {"text": "Stop 92 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 92
schedule function ac:_tour_next 240t
