$execute positioned $(x) $(y) $(z) run tp @a ~90 ~84 ~3543 180 25
tellraw @a {"text": "Republic City", "color": "gold", "bold": true}
tellraw @a {"text": "The Legend of Korra - 170-174 AG", "color": "yellow"}
tellraw @a {"text": "Art-deco skyscrapers, City Hall, the elevated rail, Satomobiles, Aang's memorial statue in", "color": "white"}
tellraw @a {"text": "Yue Bay and the downtown spirit portal.", "color": "white"}
tellraw @a {"text": "Stop 74 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 74
schedule function ac:_tour_next 240t
