$execute positioned $(x) $(y) $(z) run tp @a ~905 ~35 ~3031 180 25
tellraw @a {"text": "Kyoshi Island", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "The village, the Kyoshi Warriors' dojo, the statue of Avatar Kyoshi and the Unagi's bay.", "color": "white"}
tellraw @a {"text": "Stop 69 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 69
schedule function ac:_tour_next 240t
