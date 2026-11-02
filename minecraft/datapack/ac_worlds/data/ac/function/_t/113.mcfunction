$execute positioned $(x) $(y) $(z) run tp @a ~155 ~24 ~4611 180 25
tellraw @a {"text": "Chinese cast iron and the water-powered blast furnace", "color": "gold", "bold": true}
tellraw @a {"text": "China (Zhou to Han) - cast iron by 5th century BCE; Du Shi's water-powered bellows 31 CE", "color": "yellow"}
tellraw @a {"text": "Han furnace with waterwheel-driven bellows, tap hole and pig bed.", "color": "white"}
tellraw @a {"text": "Stop 114 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 114
schedule function ac:_tour_next 240t
