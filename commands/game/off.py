DESCRIPTION = 'OFF - extinguish the lamp'

def execute(player, noun):
    lamp = player.hasItem('lamp')
    if not lamp:
        print('You are not carrying the lamp.')
        return
    if lamp.state == 0:
        print('The lamp is already off.')
        return
    lamp.setState(0)
    lamp.setMakingLight(0)
    print('The lamp is now off.')
