DESCRIPTION = 'DEBUG - toggle debug mode, or DEBUG ITEMS to list all items'

def execute(player, noun):
    if noun and noun.upper() == 'ITEMS':
        for room in player.game.rooms.values():
            for item in room.getContains():
                print(f'  Room {room.getId()} ({room.getShortDesc()}): [{item.id}] {item.getShortDesc()} | state={item.state} | words={item.idWords}')
        for item in player.items:
            print(f'  Carried: [{item.id}] {item.getShortDesc()} | state={item.state} | words={item.idWords}')
        return
    current = player.game.settings.get('debug', False)
    player.game.settings['debug'] = not current
    print(f'Debug mode {"ON" if not current else "OFF"}')
