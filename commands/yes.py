DESCRIPTION = 'YES - affirmative response'

def execute(player, noun):
    msg = player.game.messages.get('instructions')
    if msg:
        print(msg)
    else:
        print('OK.')
