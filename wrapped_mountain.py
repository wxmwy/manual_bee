import numpy as np
import sys
import random
import array
import pygame
import mountain_utils
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

FPS = 40
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT),pygame.NOFRAME|pygame.FULLSCREEN)
pygame.display.set_caption('Flappy Bird')

IMAGES, SOUNDS, HITMASKS = mountain_utils.load()
PIPEGAPSIZE = int(100*SCREENHEIGHT/512) # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT #* 0.79

PLAYER_WIDTH = IMAGES['player'][0].get_width()
PLAYER_HEIGHT = IMAGES['player'][0].get_height()
PIPE_WIDTH = IMAGES['pipe'][0].get_width()
PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
BACKGROUND_WIDTH = IMAGES['background'].get_width()

PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])

class GameState:
    def __init__(self):
        self.playermark = self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH/3* 0.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.basex = 0
        # self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe()
        newPipe2 = getRandomPipe()
        newPipe3 = getRandomPipe()
        newPipe4 = getRandomPipe()
        newPipe5 = getRandomPipe()
        newPipe6 = getRandomPipe()
        self.upperPipes = [
            {'x': SCREENWIDTH * 0.33, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH * 0.495, 'y': newPipe2[0]['y']},
            {'x': SCREENWIDTH * 0.66, 'y': newPipe3[0]['y']},
            {'x': SCREENWIDTH * 0.825, 'y': newPipe4[0]['y']},
            {'x': SCREENWIDTH * 0.99, 'y': newPipe5[0]['y']},
            {'x': SCREENWIDTH * 1.155, 'y': newPipe6[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH * 0.33, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH * 0.495, 'y': newPipe2[1]['y']},
            {'x': SCREENWIDTH * 0.66, 'y': newPipe3[1]['y']},
            {'x': SCREENWIDTH * 0.825, 'y': newPipe4[1]['y']},
            {'x': SCREENWIDTH * 0.99, 'y': newPipe5[1]['y']},
            {'x': SCREENWIDTH * 1.155, 'y': newPipe6[1]['y']},
        ]
        self.typePipes = [
            newPipe1[2],
            newPipe2[2],
            newPipe3[2],
            newPipe4[2],
            newPipe5[2],
            newPipe6[2],
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4*SCREENWIDTH/288/3
        self.playerVelY    =  0    # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY =  10*SCREENHEIGHT/512   # max vel along Y, max descend speed
        self.playerMinVelY =  -8*SCREENHEIGHT/512   # min vel along Y, max ascend speed
        self.playerAccY    =   1*SCREENHEIGHT/512   # players downward accleration
        self.playerFlapAcc =  -9*SCREENHEIGHT/512   # players speed on flapping
        self.playerFlapped = False # True when player flaps

    def frame_step(self, input_actions, start, level):
        pygame.event.pump()

        reward = 0.1
        terminal = False
        clear = 0

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')
        if start:
            # input_actions[0] == 1: do nothing
            # input_actions[1] == 1: flap the bird
            if input_actions[1] == 1:
                if self.playery > -2 * PLAYER_HEIGHT:
                    self.playerVelY = self.playerFlapAcc
                    self.playerFlapped = True
                    #SOUNDS['wing'].play()

            # check for score
            playerMidPos = self.playerx + PLAYER_WIDTH / 2
            for pipe in self.upperPipes:
                pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
                if pipeMidPos <= playerMidPos < pipeMidPos + 2*SCREENWIDTH/288/3:
                    self.score += 1
                    clear = 1
                    pygame.mixer.music.load(SOUNDS['cheer'])
                    pygame.mixer.music.play()
                    reward = 1

            # playerIndex basex change
            if (self.loopIter + 1) % 3 == 0:
                self.playerIndex = next(PLAYER_INDEX_GEN)
            self.loopIter = (self.loopIter + 1) % 30
            self.basex = (self.basex - self.pipeVelX) % (SCREENWIDTH * 2)

            # player's movement
            if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
                self.playerVelY += self.playerAccY/2
            if self.playerFlapped:
                self.playerFlapped = False
            self.playery += min(self.playerVelY, BASEY - self.playery - PLAYER_HEIGHT)/2
            if self.playery < 0:
                self.playery = 0

            # move pipes to left
            for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
                uPipe['x'] += self.pipeVelX/2
                lPipe['x'] += self.pipeVelX/2

            # add new pipe when first pipe is about to touch left of screen
            if 0 < self.upperPipes[0]['x'] < -self.pipeVelX/2:
                newPipe = getRandomPipe()
                self.upperPipes.append(newPipe[0])
                self.lowerPipes.append(newPipe[1])
                self.typePipes.append(newPipe[2])

            # remove first pipe if its out of the screen
            if self.upperPipes[0]['x'] < -PIPE_WIDTH:
                self.upperPipes.pop(0)
                self.lowerPipes.pop(0)
                self.typePipes.pop(0)
                # newPipe = getRandomPipe()
                # self.upperPipes.append(newPipe[0])
                # self.lowerPipes.append(newPipe[1])
                # self.typePipes.append(newPipe[2])

            # check if crash here
            isCrash= checkCrash({'x': self.playerx, 'y': self.playery,
                                'index': 0},
                                self.upperPipes, self.lowerPipes, self.typePipes)
            if isCrash:
                pygame.mixer.music.load(SOUNDS['die'])
                pygame.mixer.music.play()
                terminal = True
                #self.__init__()
                reward = -1
                self.playermark = 1

        # draw true sprites
        SCREEN.blit(IMAGES['background'], (-self.basex/2,0))

        for uPipe, lPipe, typep in zip(self.upperPipes, self.lowerPipes, self.typePipes):
            SCREEN.blit(IMAGES['pipe'][typep*2+0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][typep*2+1], (lPipe['x'], lPipe['y']))
            SCREEN.blit(IMAGES['pipe'][2], (uPipe['x'], 0))
            SCREEN.blit(IMAGES['pipe'][4], (lPipe['x'], SCREENHEIGHT-IMAGES['pipe'][4].get_height()))

        # SCREEN.blit(IMAGES['base'], (-self.basex, BASEY))
        # print score so player overlaps the score
        showScore(self.score, level)
        #SCREEN.blit(IMAGES['player'][level*5+self.playermark],
        if level <15:
            pic = 0
        elif level <30:
            pic = 1
        elif level <45:
            pic = 2
        else:
            pic = 3

        SCREEN.blit(IMAGES['player'][pic],
                    (self.playerx, self.playery))

        SCREEN.blit(IMAGES['back'],(SCREENWIDTH-40-IMAGES['back'].get_width(), SCREENHEIGHT-40-IMAGES['back'].get_height()))
        SCREEN.blit(IMAGES['stop'], (SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width(), SCREENHEIGHT-40-IMAGES['stop'].get_height()))
        SCREEN.blit(IMAGES['start'], (SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width(), SCREENHEIGHT-40-IMAGES['start'].get_height()))
        if terminal:
            showRst(self.score)
            f = open('score.txt', 'r')
            t = int(f.readline())
            f.close()
            f = open('score.txt', 'w')
            f.write(str(t+1) + '\n')
            f.write(str(self.score) + '\n')
            f.close()

        pygame.display.update()
        image_data = None
        FPSCLOCK.tick(FPS)
        return image_data, reward, terminal, self.upperPipes, self.lowerPipes, self.typePipes, self.score, clear

    def changePipe(self, dy, w):
        self.upperPipes[w]['y'] += dy
        self.lowerPipes[w]['y'] += dy
        if  not (int(20*SCREENHEIGHT/512 + BASEY*0.2 - PIPE_HEIGHT) < self.upperPipes[w]['y'] < int(90*SCREENHEIGHT/512 + BASEY*0.2 - PIPE_HEIGHT)):
            self.upperPipes[w]['y'] -= dy
            self.lowerPipes[w]['y'] -= dy

def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapYs = [20, 30, 40, 50, 60, 70, 80, 90]

    index = random.randint(0, len(gapYs)-1)
    gapY = int(gapYs[index]*SCREENHEIGHT/512)

    gapY += int(BASEY * 0.2)
    pipeX = SCREENWIDTH + 10*SCREENWIDTH/288


    return [
        {'x': pipeX, 'y': gapY - PIPE_HEIGHT},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE},  # lower pipe
        0,
    ]

def showRst(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()
    
    Xoffset = SCREENWIDTH/2+30
    Yoffset = SCREENHEIGHT/2 - (40 + IMAGES['numbers'][digit].get_height())
    SCREEN.blit(IMAGES['end'], ((SCREENWIDTH-IMAGES['end'].get_width())/2, (SCREENHEIGHT-IMAGES['end'].get_height())/2))
    i = 0
    for digit in scoreDigits:
      i = i+1
    if i==1:
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset + 40, Yoffset + 14))
            Xoffset += IMAGES['numbers'][digit].get_width()
    else:
        for digit in scoreDigits:
            SCREEN.blit(IMAGES['numbers'][digit], (Xoffset + 30, Yoffset + 14))
            Xoffset += IMAGES['numbers'][digit].get_width()

def showScore(score, level):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()
    
    scorewidth = IMAGES['score'].get_width()
    scoreheight = IMAGES['score'].get_height()
    
    Xoffset = SCREENWIDTH -40-scorewidth
    Yoffset = 40 + (IMAGES['score'].get_height() - IMAGES['numbers'][digit].get_height())/2
    if(level > 8):
        SCREEN.blit(IMAGES['score'], (Xoffset, 40))
    else:
        SCREEN.blit(IMAGES['score0'], (Xoffset, 40))

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset+ 20, Yoffset))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes, typePipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return True
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])

        for uPipe, lPipe, typep in zip(upperPipes, lowerPipes, typePipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][typep*2+0]
            lHitmask = HITMASKS['pipe'][typep*2+1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)
            if uCollide or lCollide:
                return True

    return False

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False
