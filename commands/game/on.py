DESCRIPTION = 'ON - light the lamp'

def execute(player, noun):
    lamp = player.hasItem('lamp') or player.game.getRoom(player.getRoom()).ifContains('lamp')
    if not lamp:
        print('YOU HAVE NO SOURCE OF LIGHT.')
        return
    lamp.setState(1)
    lamp.setMakingLight(1)
    print('YOUR LAMP IS NOW ON.')
