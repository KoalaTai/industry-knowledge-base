$execute positioned $(x) $(y) $(z) run tp @a ~1196 ~52 ~3995 180 25
tellraw @a {"text": "wasteLAND", "color": "gold", "bold": true}
tellraw @a {"text": "Insomniac Events - 1993-2026", "color": "yellow"}
tellraw @a {"text": "The post-2019 junkyard: rusted truss LED wall, scrap towers with flames, a crashed semi,", "color": "white"}
tellraw @a {"text": "barrels and tyres.", "color": "white"}
tellraw @a {"text": "Scale: 1 block = 1 m", "color": "gray"}
tellraw @a {"text": "Stop 88 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 88
schedule function ac:_tour_next 240t
