$execute positioned $(x) $(y) $(z) run tp @a ~468 ~27 ~4427 180 25
tellraw @a {"text": "Vertical-axis windmill (panemone)", "color": "gold", "bold": true}
tellraw @a {"text": "Persia / Islamic world - attested 9th century CE (al-Masudi); possibly 7th century", "color": "yellow"}
tellraw @a {"text": "Sistan vertical-axis windmill with inlet slot and reed sails over a millstone.", "color": "white"}
tellraw @a {"text": "Stop 102 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 102
schedule function ac:_tour_next 240t
