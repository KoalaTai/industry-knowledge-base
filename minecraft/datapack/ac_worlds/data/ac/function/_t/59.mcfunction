$execute positioned $(x) $(y) $(z) run tp @a ~400 ~30 ~2699 180 25
tellraw @a {"text": "Iga Province", "color": "gold", "bold": true}
tellraw @a {"text": "Sengoku Japan - 1579-1581, the Azuchi-Momoyama period", "color": "yellow"}
tellraw @a {"text": "Thatched farmhouses in terraced rice paddies with a shinobi training hall and hidden", "color": "white"}
tellraw @a {"text": "cellar.", "color": "white"}
tellraw @a {"text": "Stop 60 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 60
schedule function ac:_tour_next 240t
