import sys
import wrapped_main as game
import pygame
import bee_fly as bee
import flytrap_fly as flytrap
import mountain_fly as mountain
import spider_fly as spider

which = [0,0]
game_state = game.GameState()
start = False

while True:
    game_state.__init__()
    game_state.framestep(which)
    if start:
        f = open('score.txt', 'w')
        f.write('0' + '\n')
        f.write('0' + '\n')
        f.close()
        if which[0] == 1:
            pygame.mixer.music.load('sounds/m1.mp3')
            pygame.mixer.music.play()
            flytrap.main()
        elif which[0] == 2:
            pygame.mixer.music.load('sounds/m2.mp3')
            pygame.mixer.music.play()
            spider.main()
        elif which[0] == 3:
            pygame.mixer.music.load('sounds/m3.mp3')
            pygame.mixer.music.play()
            mountain.main()
        elif which[0] == 4:
            pygame.mixer.music.load('sounds/m4.mp3')
            pygame.mixer.music.play()
            bee.main()
        start = False
        which = [0,0]
    else:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                which = game.hit(pos[0], pos[1], which)
                if(which[1] == 1):
                    start = True
                    # start game
                else:
                    game_state.framestep(which)