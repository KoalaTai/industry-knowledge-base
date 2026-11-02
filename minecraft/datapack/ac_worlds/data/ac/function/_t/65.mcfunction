$execute positioned $(x) $(y) $(z) run tp @a ~420 ~80 ~3061 180 25
tellraw @a {"text": "Southern Air Temple", "color": "gold", "bold": true}
tellraw @a {"text": "Avatar: The Last Airbender - 99-100 AG, the end of the Hundred Year War", "color": "yellow"}
tellraw @a {"text": "Spires on the peak, the sanctuary of Avatar statues, the airball court and Momo's orchard.", "color": "white"}
tellraw @a {"text": "Stop 66 of 132.  Next in 12 s; ac:tour_next to skip, ac:tour_stop to end.", "color": "dark_gray"}
data modify storage ac:tour i set value 66
schedule function ac:_tour_next 240t
