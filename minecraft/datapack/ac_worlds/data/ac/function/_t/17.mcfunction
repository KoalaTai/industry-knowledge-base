$execute positioned $(x) $(y) $(z) run tp @a ~576 ~39 ~801 180 25
tellraw @a {"text": "North Atlantic", "color": "gold", "bold": true}
tellraw @a {"text": "Colonial America - 1752-1783, the Seven Years' War and the Revolution", "color": "yellow"}
tellraw @a {"text": "The Morrigan among icebergs with a Hudson Valley fort on the shore (Rogue).", "color": "white"}
tellraw @a {"text": "Stop 18 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 18
schedule function ac:_tour_next 240t
