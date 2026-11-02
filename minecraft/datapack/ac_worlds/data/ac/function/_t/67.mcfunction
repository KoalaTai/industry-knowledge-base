$execute positioned $(x) $(y) $(z) run tp @a ~760 ~82 ~3141 180 25
tellraw @a {"text": "Ba Sing Se", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "The Outer Wall, Lower, Middle and Upper Rings, the Jasmine Dragon, the monorail and the", "color": "white"}
tellraw @a {"text": "Earth King's palace.", "color": "white"}
tellraw @a {"text": "Stop 68 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 68
schedule function ac:_tour_next 240t
