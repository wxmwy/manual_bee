import pygame
import sys

def load():

    bg_path = ('assets/bg0.png',
    'assets/bg1.png',
    'assets/bg2.png',
    'assets/bg3.png',
    'assets/bg4.png',
    )
    
    btn_path = 'assets/btn.png'

    IMAGES = {}

    IMAGES['player'] = pygame.image.load('assets/player.png').convert()
    IMAGES['player0'] = pygame.image.load('assets/player0.png').convert()
    IMAGES['player1'] = pygame.image.load('assets/player1.png').convert()
    IMAGES['player2'] = pygame.image.load('assets/player2.png').convert()
    IMAGES['player3'] = pygame.image.load('assets/player3.png').convert()

    IMAGES['bg'] = (
        pygame.image.load(bg_path[0]).convert(),
        pygame.image.load(bg_path[1]).convert(),
        pygame.image.load(bg_path[2]).convert(),
        pygame.image.load(bg_path[3]).convert(),
        pygame.image.load(bg_path[4]).convert(),
    )

    SOUNDS = {}

    SOUNDS['choose'] = 'sounds/choose.mp3'
    SOUNDS['cancel'] = 'sounds/cancel.mp3'
    SOUNDS['m1'] = 'sounds/m1.mp3'
    SOUNDS['m2'] = 'sounds/m2.mp3'
    SOUNDS['m3'] = 'sounds/m3.mp3'
    SOUNDS['m4'] = 'sounds/m4.mp3'

    return IMAGES, SOUNDS