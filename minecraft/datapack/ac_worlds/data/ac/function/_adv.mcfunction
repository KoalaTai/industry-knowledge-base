execute store result score #seq ac_step run data get storage ac:seq step
scoreboard players add #seq ac_step 1
execute store result storage ac:seq step int 1 run scoreboard players get #seq ac_step
schedule function ac:_next 60t
