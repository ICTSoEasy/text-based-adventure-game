DESCRIPTION = 'ON - light the lamp'

def execute(player, noun):
    lamp = player.hasItem('lamp')
    if not lamp:
        print('You are not carrying the lamp.')
        return
    if lamp.state == 1:
        print('The lamp is already lit.')
        return
    lamp.setState(1)
    lamp.setMakingLight(1)
    print('The lamp is now lit.')
