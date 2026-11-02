$execute positioned $(x) $(y) $(z) run tp @a ~430 ~53 ~2116 180 25
tellraw @a {"text": "Delphi", "color": "gold", "bold": true}
tellraw @a {"text": "Classical Greece - 431-422 BCE, the Peloponnesian War", "color": "yellow"}
tellraw @a {"text": "Terraced sanctuary: the sacred way, treasuries, Temple of Apollo, theatre and the Pythia's", "color": "white"}
tellraw @a {"text": "tripod.", "color": "white"}
tellraw @a {"text": "Stop 44 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 44
schedule function ac:_tour_next 240t
