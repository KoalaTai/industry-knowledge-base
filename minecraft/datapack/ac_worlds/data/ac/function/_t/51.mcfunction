$execute positioned $(x) $(y) $(z) run tp @a ~887 ~45 ~2297 180 25
tellraw @a {"text": "Rygjafylke Fjord", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "A snowy fjord with a hall, a stave-style chapel, a waterfall and a longship.", "color": "white"}
tellraw @a {"text": "Stop 52 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 52
schedule function ac:_tour_next 240t
