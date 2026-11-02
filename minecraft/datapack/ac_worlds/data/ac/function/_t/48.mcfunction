$execute positioned $(x) $(y) $(z) run tp @a ~420 ~39 ~2297 180 25
tellraw @a {"text": "Jorvik", "color": "gold", "bold": true}
tellraw @a {"text": "Viking England and Norway - 873 CE, the Great Heathen Army", "color": "yellow"}
tellraw @a {"text": "Viking York: earth-and-timber rampart, the minster, Coppergate craft plots and wharves.", "color": "white"}
tellraw @a {"text": "Stop 49 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 49
schedule function ac:_tour_next 240t
