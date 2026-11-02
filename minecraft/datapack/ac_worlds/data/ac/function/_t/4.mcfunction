$execute positioned $(x) $(y) $(z) run tp @a ~85 ~70 ~393 180 25
tellraw @a {"text": "Florence", "color": "gold", "bold": true}
tellraw @a {"text": "Renaissance Italy - 1476-1507", "color": "yellow"}
tellraw @a {"text": "Santa Maria del Fiore with Brunelleschi's ribbed dome, Giotto's campanile, Palazzo", "color": "white"}
tellraw @a {"text": "Vecchio, Piazza della Signoria and the Ponte Vecchio.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2 m", "color": "gray"}
tellraw @a {"text": "Stop 5 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 5
schedule function ac:_tour_next 240t
