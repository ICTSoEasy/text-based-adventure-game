DESCRIPTION = "Teleport to a room by number (e.g. CHEAT 15)"

def execute(player, noun):
    if noun is None:
        print('Cheat to where? (e.g. CHEAT 15)')
        return
    try:
        player.setRoom(int(noun))
        player.look()
    except ValueError:
        print('Please give a room number.')
