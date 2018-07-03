import pygame
import sys
def load():
    # path of player with different states
    PLAYER_PATH = (
    'assets/player/player0.png',
    'assets/player/player1.png',
    'assets/player/player2.png',
    'assets/player/player3.png',
    'assets/player/playerdie.png',
    )


    # path of pipe
    PIPE_PATH = (
        'assets/flytrap/plant1.png',
        'assets/flytrap/plant2.png',
        'assets/flytrap/plant3.png',
        'assets/flytrap/plant4.png',
        'assets/flytrap/plant5.png',
        'assets/flytrap/plant6.png',
        'assets/flytrap/plant7.png',
        'assets/flytrap/plant8.png',
    )


    IMAGES, SOUNDS, HITMASKS = {}, {}, {}

    IMAGES['score'] = pygame.image.load('assets/flytrap/score0.png').convert_alpha()
    IMAGES['score0'] = pygame.image.load('assets/flytrap/score1.png').convert_alpha()
    IMAGES['end'] = pygame.image.load('assets/flytrap/end.png').convert_alpha()
    IMAGES['start'] = pygame.image.load('assets/flytrap/start.png').convert_alpha()
    IMAGES['stop'] = pygame.image.load('assets/flytrap/stop.png').convert_alpha()
    IMAGES['change'] = pygame.image.load('assets/flytrap/change.png').convert_alpha()
    IMAGES['back'] = pygame.image.load('assets/flytrap/back.png').convert_alpha()
    IMAGES['sco'] = pygame.image.load('assets/ai.png').convert_alpha()

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/number/0.png').convert_alpha(),
        pygame.image.load('assets/number/1.png').convert_alpha(),
        pygame.image.load('assets/number/2.png').convert_alpha(),
        pygame.image.load('assets/number/3.png').convert_alpha(),
        pygame.image.load('assets/number/4.png').convert_alpha(),
        pygame.image.load('assets/number/5.png').convert_alpha(),
        pygame.image.load('assets/number/6.png').convert_alpha(),
        pygame.image.load('assets/number/7.png').convert_alpha(),
        pygame.image.load('assets/number/8.png').convert_alpha(),
        pygame.image.load('assets/number/9.png').convert_alpha()
    )

    # base (ground) sprite
    # IMAGES['base'] = pygame.image.load('flytrap/assets/sprites/base.png').convert_alpha()
    IMAGES['base-fake'] = pygame.image.load('assets/fake/base.png').convert_alpha()

    # # sounds
    SOUNDS['start'] = 'sounds/start.mp3'
    SOUNDS['cheer'] = 'sounds/cheer.mp3'
    SOUNDS['die'] = 'sounds/die.mp3'
    SOUNDS['stop'] = 'sounds/stop.mp3'
    SOUNDS['change'] = 'sounds/change.mp3'

    # select random background sprites
    IMAGES['background'] = pygame.image.load('assets/flytrap/bg.png').convert()
    IMAGES['background-fake'] = pygame.image.load('assets/fake/background.png').convert()

    # select random player sprites
    IMAGES['player'] = (
        pygame.image.load(PLAYER_PATH[0]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[1]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[2]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[3]).convert_alpha(),
        pygame.image.load(PLAYER_PATH[4]).convert_alpha(),
    )

    IMAGES['player-fake'] = (
        pygame.image.load('assets/fake/player-up.png').convert_alpha(),
        pygame.image.load('assets/fake/player-mid.png').convert_alpha(),
        pygame.image.load('assets/fake/player-down.png').convert_alpha(),
        pygame.image.load('assets/fake/playerdie.png').convert_alpha(),
    )

    # select random pipe sprites
    IMAGES['pipe'] = (
        pygame.image.load(PIPE_PATH[0]).convert_alpha(),
        pygame.image.load(PIPE_PATH[1]).convert_alpha(),
        pygame.image.load(PIPE_PATH[2]).convert_alpha(),
        pygame.image.load(PIPE_PATH[3]).convert_alpha(),
        pygame.image.load(PIPE_PATH[4]).convert_alpha(),
        pygame.image.load(PIPE_PATH[5]).convert_alpha(),
        pygame.image.load(PIPE_PATH[6]).convert_alpha(),
        pygame.image.load(PIPE_PATH[7]).convert_alpha(),
    )

    IMAGES['pipe-fake'] = (
        pygame.transform.rotate(pygame.image.load('assets/fake/pipe.png').convert_alpha(), 180),
        pygame.image.load('assets/fake/pipe.png').convert_alpha(),
    )

    # hismask for pipes
    HITMASKS['pipe'] = (
        getHitmask(IMAGES['pipe'][0]),
        getHitmask(IMAGES['pipe'][1]),
        getHitmask(IMAGES['pipe'][2]),
        getHitmask(IMAGES['pipe'][3]),
        getHitmask(IMAGES['pipe'][4]),
        getHitmask(IMAGES['pipe'][5]),
        getHitmask(IMAGES['pipe'][6]),
        getHitmask(IMAGES['pipe'][7]),
    )

    HITMASKS['back'] = getHitmask(IMAGES['back'])
    HITMASKS['change'] = getHitmask(IMAGES['change'])
    HITMASKS['stop'] = getHitmask(IMAGES['stop'])
    HITMASKS['start'] = getHitmask(IMAGES['start'])

    # hitmask for player
    HITMASKS['player'] = (
        getHitmask(IMAGES['player'][0]),
        getHitmask(IMAGES['player'][1]),
        getHitmask(IMAGES['player'][2]),
        getHitmask(IMAGES['player'][3]),
        getHitmask(IMAGES['player'][4]),
    )

    return IMAGES, SOUNDS, HITMASKS

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
