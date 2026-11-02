$execute positioned $(x) $(y) $(z) run tp @a ~225 ~32 ~3342 180 25
tellraw @a {"text": "The Boiling Rock", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Island prison in a boiling lake with coolers, yard, towers and the gondola to the rim.", "color": "white"}
tellraw @a {"text": "Stop 73 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 73
schedule function ac:_tour_next 240t
