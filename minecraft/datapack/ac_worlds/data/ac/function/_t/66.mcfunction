$execute positioned $(x) $(y) $(z) run tp @a ~595 ~84 ~3081 180 25
tellraw @a {"text": "Omashu", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Five-tier mountain city with spiralling delivery chutes and Bumi's palace on top.", "color": "white"}
tellraw @a {"text": "Stop 67 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 67
schedule function ac:_tour_next 240t
