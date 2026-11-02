$execute positioned $(x) $(y) $(z) run tp @a ~158 ~78 ~1935 180 25
tellraw @a {"text": "Giza Plateau", "color": "gold", "bold": true}
tellraw @a {"text": "Ptolemaic Egypt - 49-43 BCE, reign of Ptolemy XIII and Cleopatra VII", "color": "yellow"}
tellraw @a {"text": "Khufu, Khafre and Menkaure with the Sphinx in its enclosure, mastaba cemeteries,", "color": "white"}
tellraw @a {"text": "causeways, temples, boat pits and the workers' village. Enter Khufu from the north face:", "color": "white"}
tellraw @a {"text": "descending passage, Grand Gallery, Queen's and King's Chambers.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 2.3 m", "color": "gray"}
tellraw @a {"text": "Stop 36 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 36
schedule function ac:_tour_next 240t
