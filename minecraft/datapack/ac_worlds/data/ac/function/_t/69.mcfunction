$execute positioned $(x) $(y) $(z) run tp @a ~1080 ~57 ~3101 180 25
tellraw @a {"text": "Fire Nation Capital", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "The caldera city: volcanic rim, Royal Palace with the throne behind flames, and the Agni", "color": "white"}
tellraw @a {"text": "Kai arena.", "color": "white"}
tellraw @a {"text": "Stop 70 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 70
schedule function ac:_tour_next 240t
