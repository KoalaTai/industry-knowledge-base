$execute positioned $(x) $(y) $(z) run tp @a ~410 ~30 ~1213 180 25
tellraw @a {"text": "Versailles", "color": "gold", "bold": true}
tellraw @a {"text": "Revolutionary Paris - 1789-1794", "color": "yellow"}
tellraw @a {"text": "The garden front, the Hall of Mirrors, the Latona fountain, the Tapis Vert and the Grand", "color": "white"}
tellraw @a {"text": "Canal.", "color": "white"}
tellraw @a {"text": "Stop 26 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 26
schedule function ac:_tour_next 240t
