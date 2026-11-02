$execute positioned $(x) $(y) $(z) run tp @a ~60 ~15 ~3282 180 25
tellraw @a {"text": "Western Air Temple", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Inverted pagodas hanging under the cliff edge above a canyon.", "color": "white"}
tellraw @a {"text": "Stop 72 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 72
schedule function ac:_tour_next 240t
