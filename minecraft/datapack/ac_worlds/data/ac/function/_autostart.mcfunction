scoreboard players set #auto ac_flag 2
tellraw @a {"text": "AC Worlds: auto-build of the full hub starts around the first player in 15 seconds.", "color": "gold", "bold": true}
tellraw @a {"text": "Run /function ac:cancel to stop it, or /function ac:index to pick single builds instead.", "color": "yellow"}
schedule function ac:_autobuild 300t
