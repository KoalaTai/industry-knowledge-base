execute unless data storage ac:hub x run tellraw @s {"text": "No hub built yet: run /function ac:hub first (ac:index for single builds).", "color": "red"}
execute if data storage ac:hub x run function ac:_goto/seven_havens with storage ac:hub
