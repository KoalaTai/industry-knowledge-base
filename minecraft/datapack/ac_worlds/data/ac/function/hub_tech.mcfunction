execute store result storage ac:seq x int 1 run data get entity @s Pos[0]
execute store result storage ac:seq y int 1 run data get entity @s Pos[1]
execute store result storage ac:seq z int 1 run data get entity @s Pos[2]
data modify storage ac:seq seq set value "hub_tech"
data modify storage ac:seq step set value 0
tellraw @a {"text": "Premodern technology: 37 build(s) queued. Chunks are force-loaded two seconds before each placement.", "color": "aqua"}
function ac:_next
