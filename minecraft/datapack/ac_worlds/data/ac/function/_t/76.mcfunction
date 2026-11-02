$execute positioned $(x) $(y) $(z) run tp @a ~585 ~45 ~3563 180 25
tellraw @a {"text": "Zaofu", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "Six platinum petal domes around Suyin's estate and the meteorite stage.", "color": "white"}
tellraw @a {"text": "Stop 77 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 77
schedule function ac:_tour_next 240t
