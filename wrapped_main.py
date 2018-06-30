import pygame
import main_utils
import time

FPS = 40
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512
pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),pygame.NOFRAME|pygame.FULLSCREEN )
pygame.display.set_caption('Flappy Bird')
start = False
which = [0, 0]
IMAGES, SOUNDS = main_utils.load()

PLAYERWIDTH = IMAGES['player'].get_width()/2
PLAYERHEIGHT = IMAGES['player'].get_height()/2


class GameState:
    def __init__(self):
        self.playerx = SCREENWIDTH/2-PLAYERWIDTH
        self.playery = SCREENHEIGHT/2-PLAYERHEIGHT

    def framestep(self, which):
        SCREEN.blit(IMAGES['bg'][which[0]], (0,0))
        SCREEN.blit(IMAGES['player'], (self.playerx+3, self.playery+10))
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    def play(s):
        SOUNDS[s].play()

#which = game.hit(pos[0], pos[1], which)

def hit(x, y, which):
    rst = which
    if SCREENWIDTH/2 - PLAYERWIDTH < x < SCREENWIDTH/2 + PLAYERWIDTH and SCREENHEIGHT/2 -PLAYERHEIGHT < y < SCREENHEIGHT/2+PLAYERHEIGHT:
        if rst[0] != 0:
            pygame.mixer.music.load(SOUNDS['choose'])
            pygame.mixer.music.play()
            time.sleep(0.1)
            rst[1] = 1
    else:
        if x < SCREENWIDTH/2:
            if y < SCREENHEIGHT/2:
                rst[0] = 1
                if not (x > SCREENWIDTH /2 - PLAYERWIDTH and y > SCREENHEIGHT/2 - PLAYERHEIGHT):
                    #rst[0] = 1 - rst[0]
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
            else:
                rst[0] = 3
                if not(x > SCREENWIDTH /2 - PLAYERWIDTH and y < SCREENHEIGHT/2 + PLAYERHEIGHT):
                    #rst[0] = 3 - rst[0]
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
        else:
            if y < SCREENHEIGHT/2:
                rst[0] = 2
                if not (x < SCREENWIDTH/2 + PLAYERWIDTH and y > SCREENHEIGHT/2 - PLAYERHEIGHT):
                    #rst[0] = 2 - rst[0]
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
            else:
                rst[0] = 4
                if not (x < SCREENWIDTH/2 + PLAYERWIDTH and y < SCREENHEIGHT/2 + PLAYERHEIGHT):
                    #rst[0] = 4 - rst[0]
                    if rst[0] == 0:
                        pygame.mixer.music.load(SOUNDS['cancel'])
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load(SOUNDS['choose'])
                        pygame.mixer.music.play()
    return rst