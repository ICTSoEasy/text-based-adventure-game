DESCRIPTION = 'OFF - extinguish the lamp'

def execute(player, noun):
    lamp = player.hasItem('lamp') or player.game.getRoom(player.getRoom()).ifContains('lamp')
    if not lamp:
        print('YOU HAVE NO SOURCE OF LIGHT.')
        return
    lamp.setState(0)
    lamp.setMakingLight(0)
    print('YOUR LAMP IS NOW OFF.')
