$execute positioned $(x) $(y) $(z) run tp @a ~306 ~25 ~4552 180 25
tellraw @a {"text": "The arch, the vault and the dome", "color": "gold", "bold": true}
tellraw @a {"text": "Etruscan and Roman - true arch in Etruria 4th century BCE; Roman vaults from 2nd century BCE", "color": "yellow"}
tellraw @a {"text": "Arch on centering, finished arch, barrel vault and groin vault.", "color": "white"}
tellraw @a {"text": "Stop 108 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 108
schedule function ac:_tour_next 240t
