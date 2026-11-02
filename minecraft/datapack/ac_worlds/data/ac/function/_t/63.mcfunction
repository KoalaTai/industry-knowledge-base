$execute positioned $(x) $(y) $(z) run tp @a ~70 ~32 ~3041 180 25
tellraw @a {"text": "Southern Water Tribe", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Igloos and tents inside the snow wall, Sokka's watchtower, the Fire Navy wreck and the", "color": "white"}
tellraw @a {"text": "iceberg.", "color": "white"}
tellraw @a {"text": "Stop 64 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 64
schedule function ac:_tour_next 240t
