$execute positioned $(x) $(y) $(z) run tp @a ~245 ~51 ~3071 180 25
tellraw @a {"text": "Northern Water Tribe", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Agna Qel'a: sea wall and water gate, canals, ice houses, the tiered palace and the Spirit", "color": "white"}
tellraw @a {"text": "Oasis with Tui and La.", "color": "white"}
tellraw @a {"text": "Stop 65 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 65
schedule function ac:_tour_next 240t
