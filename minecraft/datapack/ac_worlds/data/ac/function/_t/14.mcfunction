$execute positioned $(x) $(y) $(z) run tp @a ~70 ~61 ~799 180 25
tellraw @a {"text": "Boston", "color": "gold", "bold": true}
tellraw @a {"text": "Colonial America - 1752-1783, the Seven Years' War and the Revolution", "color": "yellow"}
tellraw @a {"text": "Old North Church with its lantern steeple, Long Wharf, brick streets and a ship at anchor.", "color": "white"}
tellraw @a {"text": "Stop 15 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 15
schedule function ac:_tour_next 240t
