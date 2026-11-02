execute unless data storage ac:hub z if data storage ac:seq {seq:"hub"} run data modify storage ac:hub x set from storage ac:seq x
execute unless data storage ac:hub z if data storage ac:seq {seq:"hub"} run data modify storage ac:hub y set from storage ac:seq y
execute unless data storage ac:hub z if data storage ac:seq {seq:"hub"} run data modify storage ac:hub z set from storage ac:seq z
execute unless data storage ac:hub x run tellraw @s {"text": "No hub built yet: run /function ac:hub first (ac:index for single builds).", "color": "red"}
execute if data storage ac:hub x run function ac:_goto/italy with storage ac:hub
