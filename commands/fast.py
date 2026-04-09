import TERMINAL

DESCRIPTION = 'FAST - toggle typewriter effect on/off'

def execute(player, noun):
    t = TERMINAL.get()
    if t is None:
        print('No terminal to configure.')
        return
    if t.typewriter_speed > 0:
        t.typewriter_speed = 0
        print('Typewriter effect off.')
    else:
        t.typewriter_speed = 0.02
        print('Typewriter effect on.')
