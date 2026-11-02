$execute positioned $(x) $(y) $(z) run tp @a ~299 ~23 ~4637 180 25
tellraw @a {"text": "Stepwells (baori, vav)", "color": "gold", "bold": true}
tellraw @a {"text": "India (Rajasthan and Gujarat) - Chand Baori c. 800-900 CE; Rani ki Vav 1063", "color": "yellow"}
tellraw @a {"text": "Chand Baori type stepwell, 12 storeys down to the water.", "color": "white"}
tellraw @a {"text": "Stop 117 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 117
schedule function ac:_tour_next 240t
