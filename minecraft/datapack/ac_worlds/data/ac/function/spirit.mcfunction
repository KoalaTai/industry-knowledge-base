gamemode spectator @s
effect give @s minecraft:night_vision infinite 0 true
tellraw @s {"text": "Spirit mode: you are a ghost. Fly through anything, scroll to change speed, see in the dark.", "color": "light_purple", "bold": true}
tellraw @s {"text": "/function ac:overview floats you above the hub; /function ac:goto/<world> jumps to a row; /function ac:fly to come back.", "color": "gray"}
