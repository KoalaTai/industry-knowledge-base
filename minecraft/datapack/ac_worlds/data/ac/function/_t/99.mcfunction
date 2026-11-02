$execute positioned $(x) $(y) $(z) run tp @a ~368 ~19 ~4427 180 25
tellraw @a {"text": "The wheel, the potter's wheel and the spoked-wheel chariot", "color": "gold", "bold": true}
tellraw @a {"text": "Mesopotamia, Eurasian steppe, Egypt - potter's wheel c. 3500 BCE; wheeled vehicles c. 3500-3300 BCE; spoked chariots c. 2000 BCE", "color": "yellow"}
tellraw @a {"text": "Solid-wheel ox cart, spoked chariot with horses, and a potter's wheel.", "color": "white"}
tellraw @a {"text": "Stop 100 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 100
schedule function ac:_tour_next 240t
