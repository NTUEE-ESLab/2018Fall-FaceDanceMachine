import os
import pygame as pg
from FaceDanceMachine import FaceDanceMachine
from Similarity import Similarity

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d"%(30,0)

def main():
    similarity = Similarity()

    pg.init() 

    display_width = 740
    display_height = 480

    clock = pg.time.Clock()
    gameDisplay = pg.display.set_mode([display_width,display_height])
    pg.display.set_caption('Face Dance Machine') 
    
    faceDanceMachine = FaceDanceMachine(gameDisplay, similarity)
    faceDanceMachine.run()
    pg.quit()

if  __name__ == '__main__':
    main()
