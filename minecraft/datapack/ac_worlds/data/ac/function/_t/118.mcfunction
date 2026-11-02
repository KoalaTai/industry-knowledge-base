$execute positioned $(x) $(y) $(z) run tp @a ~411 ~33 ~4613 180 25
tellraw @a {"text": "Al-Jazari's machines: crank, camshaft and the elephant clock", "color": "gold", "bold": true}
tellraw @a {"text": "Artuqid state (Islamic world) - Book of Knowledge of Ingenious Mechanical Devices, 1206", "color": "yellow"}
tellraw @a {"text": "Al-Jazari's elephant clock with tank, float, scribe, dragons and phoenix.", "color": "white"}
tellraw @a {"text": "Stop 119 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 119
schedule function ac:_tour_next 240t
