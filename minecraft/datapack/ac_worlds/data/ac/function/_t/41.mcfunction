$execute positioned $(x) $(y) $(z) run tp @a ~90 ~59 ~2136 180 25
tellraw @a {"text": "Athens", "color": "gold", "bold": true}
tellraw @a {"text": "Classical Greece - 431-422 BCE, the Peloponnesian War", "color": "yellow"}
tellraw @a {"text": "The Acropolis rock with Parthenon, Erechtheion, Propylaia and Athena Promachos; the", "color": "white"}
tellraw @a {"text": "theatre and agora below.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2 m", "color": "gray"}
tellraw @a {"text": "Stop 42 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 42
schedule function ac:_tour_next 240t
