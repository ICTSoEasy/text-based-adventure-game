DESCRIPTION = "Teleport to a room by number (e.g. CHEAT 15)"

def execute(player, noun):
    if noun is None:
        print('Cheat to where? (e.g. CHEAT 15)')
        return
    try:
        room_id = int(noun)
    except ValueError:
        print('Please give a room number.')
        return
    if room_id not in player.game.rooms:
        print(f'Room {room_id} does not exist.')
        return
    player.setRoom(room_id)
    player.look()
