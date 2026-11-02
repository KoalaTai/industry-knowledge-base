$execute positioned $(x) $(y) $(z) run tp @a ~275 ~76 ~1588 180 25
tellraw @a {"text": "St Paul's Cathedral", "color": "gold", "bold": true}
tellraw @a {"text": "Victorian London - 1868", "color": "yellow"}
tellraw @a {"text": "Wren's dome on its colonnaded drum with twin west towers, over City streets.", "color": "white"}
tellraw @a {"text": "Stop 32 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 32
schedule function ac:_tour_next 240t
