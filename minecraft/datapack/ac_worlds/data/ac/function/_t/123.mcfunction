$execute positioned $(x) $(y) $(z) run tp @a ~270 ~40 ~4694 180 25
tellraw @a {"text": "The mechanical clock and the verge escapement", "color": "gold", "bold": true}
tellraw @a {"text": "Medieval Europe (with Chinese and Islamic water-clock precursors) - weight-driven escapement clocks from the 1280s-1300s", "color": "yellow"}
tellraw @a {"text": "Belfry with weight, drum, crown wheel, verge and foliot, bell and dial.", "color": "white"}
tellraw @a {"text": "Stop 124 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 124
schedule function ac:_tour_next 240t
