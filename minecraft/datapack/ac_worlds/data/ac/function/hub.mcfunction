execute store result storage ac:seq x int 1 run data get entity @s Pos[0]
execute store result storage ac:seq y int 1 run data get entity @s Pos[1]
execute store result storage ac:seq z int 1 run data get entity @s Pos[2]
data modify storage ac:seq seq set value "hub"
data modify storage ac:seq step set value 0
data modify storage ac:hub x set from storage ac:seq x
data modify storage ac:hub y set from storage ac:seq y
data modify storage ac:hub z set from storage ac:seq z
tellraw @a {"text": "Everything: 119 build(s) queued. Chunks are force-loaded two seconds before each placement.", "color": "aqua"}
function ac:_next
