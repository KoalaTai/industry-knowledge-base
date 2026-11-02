$execute positioned $(x) $(y) $(z) run tp @a ~18 ~24 ~4704 180 25
tellraw @a {"text": "Noria and saqiya waterwheels", "color": "gold", "bold": true}
tellraw @a {"text": "Hellenistic and Islamic Middle East - saqiya in Ptolemaic Egypt 3rd century BCE; the Hama norias from Byzantine times", "color": "yellow"}
tellraw @a {"text": "River noria filling an aqueduct, and an ox-driven saqiya over a well.", "color": "white"}
tellraw @a {"text": "Stop 120 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 120
schedule function ac:_tour_next 240t
