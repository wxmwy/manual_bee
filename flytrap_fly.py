import wrapped_flytrap as game
import numpy as np
import pygame
import sys
import flytrap_utils
import random
from collections import deque

ACTIONS = 2 # number of valid actions
game_state = game.GameState()
IMAGES, SOUNDS, HITMASKS = flytrap_utils.load()
SCREENWIDTH  = 1920 #288
SCREENHEIGHT = 1080 #512

def hitbtn(x, y):

    if int(SCREENWIDTH-40-IMAGES['back'].get_width()) <= x <= int(SCREENWIDTH-40) and int(SCREENHEIGHT-40-IMAGES['back'].get_height()) <= y <= int(SCREENHEIGHT-40):
         if HITMASKS['back'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['back'].get_height())]:
            return 1
    elif int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width()) <= x <= int(SCREENWIDTH-40-IMAGES['back'].get_width()) and int(SCREENHEIGHT-40-IMAGES['stop'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['stop'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['stop'].get_height())]:
            return 2
    elif int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width()) <= x <= int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width()-40) and int(SCREENHEIGHT-40-IMAGES['start'].get_height()) <= y <= int(SCREENHEIGHT-40):
        if HITMASKS['start'][x-int(SCREENWIDTH-40-IMAGES['back'].get_width()-40-IMAGES['stop'].get_width()-40-IMAGES['start'].get_width())][y-int(SCREENHEIGHT-40-IMAGES['start'].get_height())]:
            return 3
    return 0

def hitPixel(x, y, u0, l0, t0):
    uHitmask = HITMASKS['pipe'][t0*2+0]
    lHitmask = HITMASKS['pipe'][t0*2+1]
    try:
        if uHitmask[x-int(u0['x'])][y-int(u0['y'])]:
            return True
    except IndexError:
        try:
            if lHitmask[x-int(l0['x'])][y-int(l0['y'])]:
                return True
        except IndexError:
            return False
    return False

def hit(x, y, u, l, ty):
    for i in range(0, len(u)):
        if(hitPixel(x, y, u[i], l[i], ty[i])):
            return i
    return -1

def main():
    start = False
    level = 9
    # start training
    t = 0
    py = 0
    drag = False
    which = -1
    # get the first state by doing nothing and preprocess the image to 80x80x4
    game_state.__init__()
    do_nothing = np.zeros(ACTIONS)
    do_nothing[0] = 1
    x_t, r_0, terminal, u, l,ty,score,clear = game_state.frame_step(do_nothing, start, level)
    die = True
    while not terminal:
        t = np.zeros(ACTIONS)
        t[0] = 1
        t[1] = 0
        if start:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        t[0] = 0
                        t[1] = 1
                elif event.type == pygame.K_UP:
                    t[0] = 1
                    t[1] = 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    try:
                        tmpt = hitbtn(pos[0], pos[1])
                    except Exception:
                        tmpt = 0
                    if tmpt != 0:
                        if tmpt == 1:
                            terminal = True
                            die = False
                            pygame.mixer.music.load(SOUNDS['start'])
                            pygame.mixer.music.play()
                        elif tmpt == 2:
                            start = False
                            pygame.mixer.music.load(SOUNDS['stop'])
                            pygame.mixer.music.play()
            x_t, r_0, terminal, u, l,ty,score,clear = game_state.frame_step(t, start, level)
            if clear == 1:
                level = 0
            level = level + 1
        else:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if not drag:
                        try:
                            tmpt = hitbtn(pos[0], pos[1])
                        except Exception:
                            tmpt = 0
                        if tmpt != 0:
                            if tmpt == 1:
                                terminal = True
                                die = False
                                pygame.mixer.music.load(SOUNDS['start'])
                                pygame.mixer.music.play()
                            elif tmpt == 3:
                                start = True
                                pygame.mixer.music.load(SOUNDS['start'])
                                pygame.mixer.music.play()
                        else:   
                            which = hit(pos[0], pos[1], u, l, ty)
                            if -1 != which:
                                py = pos[1]
                                drag = True
                                pygame.mixer.music.load(SOUNDS['change'])
                                pygame.mixer.music.play()
                elif event.type == pygame.MOUSEMOTION:
                    if drag:
                        pos = pygame.mouse.get_pos()
                        game_state.changePipe(pos[1]-py, which)
                        py = pos[1]
                        _, _, terminal, u, l, ty, score,clear = game_state.frame_step(do_nothing, start, level)
                        if clear == 1:
                            level = 0
                        level = level + 1
                elif event.type == pygame.MOUSEBUTTONUP:
                    drag = False
    while die:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    die = False
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                try:
                    tmpt = hitbtn(pos[0], pos[1])
                except Exception:
                    tmpt = 0
                if tmpt == 1:
                    terminal = True
                    die = False
                    pygame.mixer.music.load(SOUNDS['start'])
                    pygame.mixer.music.play()