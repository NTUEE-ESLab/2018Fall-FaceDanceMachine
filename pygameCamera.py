import cv2
import pygame as pg
import pygame.camera as pgcam
import numpy as np

class Camera():
    def __init__(self, display):
        pgcam.init()
        self.clist = pgcam.list_cameras()
        print(self.clist)
        if not self.clist:
            raise ValueError("sorry no camera detected")
        
        self.camera = pgcam.Camera(self.clist[0], (640,480))
        self.screen = pg.surface.Surface((640,480), 0, display)
        self.camera.start()
        print("camera set")

    def capture(self):
        return self.camera.get_image(self.screen)
    
    def pg2cv(self, frame):
        img = pg.surfarray.pixels3d(frame)
        img = np.rot90(img, -1)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def stop(self):
        self.camera.stop()
