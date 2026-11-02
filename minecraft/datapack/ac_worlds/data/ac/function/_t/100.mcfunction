$execute positioned $(x) $(y) $(z) run tp @a ~423 ~27 ~4487 180 25
tellraw @a {"text": "Qanat", "color": "gold", "bold": true}
tellraw @a {"text": "Persia (Achaemenid and earlier) - first millennium BCE", "color": "yellow"}
tellraw @a {"text": "Cut-away hillside showing mother well, shafts, graded tunnel and outlet fields.", "color": "white"}
tellraw @a {"text": "Stop 101 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 101
schedule function ac:_tour_next 240t
