$execute positioned $(x) $(y) $(z) run tp @a ~410 ~50 ~3503 180 25
tellraw @a {"text": "Air Temple Island", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "Tenzin's temple spires, the spinning airbending gates, the bison stables with Oogi.", "color": "white"}
tellraw @a {"text": "Stop 76 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 76
schedule function ac:_tour_next 240t
