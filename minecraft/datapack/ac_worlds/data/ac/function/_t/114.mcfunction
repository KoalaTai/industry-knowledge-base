$execute positioned $(x) $(y) $(z) run tp @a ~201 ~19 ~4637 180 25
tellraw @a {"text": "The Grand Canal and the pound lock", "color": "gold", "bold": true}
tellraw @a {"text": "Sui and Song China - Grand Canal 605-609 CE; pound lock by Qiao Weiyue 984 CE", "color": "yellow"}
tellraw @a {"text": "Lock chamber between two levels with a barge inside.", "color": "white"}
tellraw @a {"text": "Stop 115 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 115
schedule function ac:_tour_next 240t
