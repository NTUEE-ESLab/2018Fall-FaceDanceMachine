import os
import pygame as pg
import numpy as np
import random
from pygameCamera import Camera
from utils import *
import threading

class FaceDanceMachine:

    def __init__(self, display, similarity):
        """ Constructor function """
        self.black = (0,0,0)
        self.display = display
        self.camera = Camera(self.display)
        self.similarity = similarity
        self.imgs, self.buttons = loadGameImgNButtons()

    def welcome(self):
        self.display.fill(self.black)
        loadNblit('welcome.png',self.display,0,0,740,480)
        pg.display.update()
        
        while True:  
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()      
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            if 455<=mouse[0]<=695 and 290<=mouse[1]<=410 and click[0]==1:
                break

    def menu(self):
        self.display.fill(self.black)
        loadNblit('level1.png',self.display,168,72,404,337)
        loadNblit('level2.png',self.display,168,72,404,337)
        loadNblit('level3.png',self.display,168,72,404,337)
        pg.display.update()
        
        while True:  
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()                    
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            if 245<=mouse[0]<=495 and 64<=mouse[1]<=160 and click[0]==1:
                self.level = 1
                print("level 1 ...")
                break
            elif 245<=mouse[0]<=495 and 192<=mouse[1]<=288 and click[0]==1:
                self.level = 2
                print("level 2 ...")
                break
            elif 245<=mouse[0]<=495 and 320<=mouse[1]<=416 and click[0]==1:
                self.level = 3
                print("level 3 ...")
                break

    def countDown(self):
        imgs = loadCountDownImgs()
        countDownImg = [load_image(str(index)+'.png',576,480) for index in range(4)]
        start = pg.time.get_ticks()
        
        while True:
            sec = (pg.time.get_ticks()-start)/1000  
            index = int(sec)
            if index > 3:
                break
            self.display.fill(self.black)
            self.display.blit(pg.transform.flip(self.camera.capture(), True, False), (0,0))
            self.display.blit(countDownImg[index], (32,0))
            for i in range(5):
                target = (i+index) if ((i+index)<5) else (i+index-5)
                self.display.blit(imgs[target], (640, 96*i))
            pg.display.update()
    
    def game(self):
        score = 0
        count = 0
        next = [True for i in range(self.level)]
        pos = [(0, (2-i)*144) for i in range(self.level)]
        mission = [ 0 for i in range(self.level)]
        start = pg.time.get_ticks()
        self.result, self.sim = -1, 0

        while True:
            
            #time up
            if (pg.time.get_ticks()-start) > 100000:
                exit = self.end(score)
                if exit:
                    return False
                else:
                    return True

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()                    
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            #pause
            if 640<=mouse[0]<=740 and 160<=mouse[1]<=256 and click[0]==1:
                print("pause")
                exit = self.pause()
                if exit:
                    return False
            #exit
            if 640<=mouse[0]<=740 and 288<=mouse[1]<=384 and click[0]==1:
                return False
            frame = self.camera.capture() #pygame surface
            self.display.fill(self.black)
            self.display.blit(pg.transform.flip(frame, True, False),(0,0))
            show_text("Score", self.display, 660, 90)
            show_text(str(score), self.display, 680, 120)
            self.display.blit(self.buttons[0], (640, 160))
            self.display.blit(self.buttons[1], (640, 288))
            
            #face
            if count%50==0:
                t = threading.Thread(target=self.job, args=(frame, mission, ))
                t.start()
            if count%50 == 49:
                t.join()
            for i in range(self.level):
                if next[i]:
                    next[i] = False
                    pos[i] = (0, (2-i)*144)
                    mission[i] = random.randint(0,9)
                self.display.blit(self.imgs[mission[i]], pos[i])
                pos[i]= (pos[i][0]+2, pos[i][1])
                if self.result == mission[i]:
                    self.display.blit(self.imgs[10], pos[i])
                    score += int(100*self.sim)
                    next[i] = True
                if pos[i][0] > 480:
                    next[i]=True
            count += 1
            pg.display.update()
    
    def job(self, frame, mission):
        print("Thread start...")
        cv_frame = self.camera.pg2cv(frame)
        self.result, self.sim = self.similarity.face_dance(cv_frame, mission)
        print("Thread finish...")

    def pause(self):
        buttons = loadPauseButtons()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()                    
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            #play
            if 100<=mouse[0]<=300 and 190<=mouse[1]<=310 and click[0]==1:
                return False
            #exit
            if 440<=mouse[0]<=640 and 190<=mouse[1]<=310 and click[0]==1:
                return True
            self.display.fill(self.black)
            self.display.blit(buttons[0], (100, 190))
            self.display.blit(buttons[1], (440, 190))
            pg.display.update()
    
    def exit(self):
        self.display.fill(self.black)
        loadNblit('bye_3.png',self.display,82,0,576,480) 
        pg.display.update()
        print("exitting ...")
        pg.time.wait(1000)
    
    def end(self, score):
        self.display.fill(self.black)
        buttons = loadEndButtons()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()                    
            mouse = pg.mouse.get_pos()
            click = pg.mouse.get_pressed()
            #replay
            if 100<=mouse[0]<=300 and 260<=mouse[1]<=460 and click[0]==1:
                return False
            #exit
            if 440<=mouse[0]<=640 and 260<=mouse[1]<=460 and click[0]==1:
                return True
            self.display.fill(self.black)
            show_text("Score: " + str(score), self.display, 100, 100, 80)
            self.display.blit(buttons[0], (100, 260))
            self.display.blit(buttons[1], (440, 260))
            pg.display.update() 

    def run(self):
        self.welcome()
        replay = True
        while replay:
            self.menu()
            self.countDown()
            replay = self.game()
        self.exit()
        print("success")
        self.camera.stop() 
