schedule clear ac:_autobuild
schedule clear ac:_next
schedule clear ac:_tour_next
scoreboard players set #auto ac_flag 0
forceload remove all
tellraw @a {"text": "AC Worlds: build sequence cancelled and chunks released.", "color": "red"}
