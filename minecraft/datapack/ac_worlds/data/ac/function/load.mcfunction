scoreboard objectives add ac_step dummy
scoreboard objectives add ac_flag dummy
execute unless score #auto ac_flag = #auto ac_flag run scoreboard players set #auto ac_flag 1
gamerule maxCommandChainLength 1000000
tellraw @a {"text": "AC Worlds datapack loaded. /function ac:index lists every build; /function ac:hub builds everything.", "color": "gold"}
