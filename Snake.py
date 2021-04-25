import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox
pygame.font.init()

width = 500
height = 500

cols = 25
rows = 20


class cube():
    rows = 20
    w = 500
    def __init__(self, start, direction_x=1, direction_y=0, color=(255,212,59)):
        self.pos = start
        self.direction_x = direction_x
        self.direction_y = direction_y # "L", "R", "U", "D"
        self.color = color

    def move(self, direction_x, direction_y):
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.pos  = (self.pos[0] + self.direction_x, self.pos[1] + self.direction_y)
            

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]
        
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1,dis-2,dis-2))
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)
        


class snake():
    body = []
    turns = {}
    
    def __init__(self, color, pos):
        #pos is given as coordinates on the grid ex (1,5)
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.direction_x = 0
        self.direction_y = 1
    
    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_x = -1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x,self.direction_y]
                elif keys[pygame.K_RIGHT]:
                    self.direction_x = 1
                    self.direction_y = 0
                    self.turns[self.head.pos[:]] = [self.direction_x,self.direction_y]
                elif keys[pygame.K_UP]:
                    self.direction_x = 0
                    self.direction_y = -1
                    self.turns[self.head.pos[:]] = [self.direction_x,self.direction_y]
                elif keys[pygame.K_DOWN]:
                    self.direction_x = 0
                    self.direction_y = 1
                    self.turns[self.head.pos[:]] = [self.direction_x,self.direction_y]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                c.move(c.direction_x,c.direction_y)
        
        
    def reset(self,pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.direction_x = 0
        self.direction_y = 1

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.direction_x, tail.direction_y

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        self.body[-1].direction_x = dx
        self.body[-1].direction_y = dy
    
    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)



def redrawWindow():
    global win
    win.fill((0,0,0))
    drawGrid(width, rows, win)
    s.draw(win)
    snack.draw(win)
    pygame.display.update()
    pass



def drawGrid(w, rows, surface):
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))
    
def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, ((width/2 - label.get_width()/2), height/2 - label.get_height()/2 ))

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(1,rows-1)
        y = random.randrange(1,rows-1)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
               continue
        else:
               break

    return (x,y)

#This is where the game start and running 
def main():
    global s, snack, win
    win = pygame.display.set_mode((width,height))
    s = snake((255,212,59), (10,10))
    s.addCube()
    snack = cube(randomSnack(rows,s), color=(48,105,152))
    run = True
    clock = pygame.time.Clock()
    lose = False
    wall = False
    bite = False

    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        headPos = s.head.pos
        #if the snake hit the wall
        if headPos[0] >= 20 or headPos[0] < 0 or headPos[1] >= 20 or headPos[1] < 0:
            score = len(s.body)
            s.reset((10, 10))
            lose = True
            wall = True

        #if the snake eats the snack
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows,s), color=(48,105,152))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):
                score = len(s.body)
                s.reset((10,10))
                lose = True
                bite = True
                break

        while lose:
            if wall:
                message = "You hit the wall. Score: "+ str(score)
            elif bite:
                message = "You bit yourself. Score: "+ str(score)
            draw_text_middle(win, message, 45, (255,0,0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    lose = False
                    wall = False
                    bite = False
        
        redrawWindow()

main()