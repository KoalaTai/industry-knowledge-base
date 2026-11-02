$data modify storage ac:tour x set value $(x)
$data modify storage ac:tour y set value $(y)
$data modify storage ac:tour z set value $(z)
data modify storage ac:tour i set value 0
gamemode spectator @a
tellraw @a {"text": "AC Worlds tour: 132 stops, 12 seconds each. /function ac:tour_next skips, ac:tour_stop ends.", "color": "gold", "bold": true}
function ac:_tour_next
