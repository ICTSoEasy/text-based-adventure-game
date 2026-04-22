DESCRIPTION = 'X - cheat: grab lamp and turn it on'

def execute(player, noun):
    print('NO RULES.')
    lamp = player.game.findItem('LAMP')
    if lamp is None:
        print('Lamp not found.')
        return
    for room in player.game.rooms.values():
        if lamp in room.getContains():
            room.remove(lamp)
            break
    player.items.append(lamp)
    lamp.setState(1)
    lamp.setMakingLight(1)
    print('YOUR LAMP IS NOW ON.')
