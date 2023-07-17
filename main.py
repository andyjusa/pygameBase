import pygame.event

from Colors import *
from Base import *

base = r"resources/"

pygame.init()

size = [1500, 300]
screen = pygame.display.set_mode(size)
done = False
clock = pygame.time.Clock()

debugging = True
pressedKeys = []
frameRate = 60
df = 0


def everyTime():
    pass


def RunGame():
    global done
    global df
    while not done:
        everyTime()
        df = clock.tick(frameRate)
        screen.fill(WALLPAPER.rgb)
        loop(pygame.event.get(), screen, df)
        pygame.display.update()


@eventDef(pygame.QUIT)
def onQuit(event):
    global done
    done = True


@eventDef(pygame.TEXTINPUT)
def onTextInput(event):
    pass


RunGame()
pygame.quit()
