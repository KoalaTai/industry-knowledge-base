$execute positioned $(x) $(y) $(z) run tp @a ~886 ~73 ~4275 180 25
tellraw @a {"text": "Escape: Psycho Circus", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "Escape 2018 at NOS: the Slaughterhouse stage in a giant clown's mouth under a striped big", "color": "white"}
tellraw @a {"text": "top with circus cages, and Ghouls' Graveyard's haunted house with headstones and dead", "color": "white"}
tellraw @a {"text": "trees.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 94 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 94
schedule function ac:_tour_next 240t
