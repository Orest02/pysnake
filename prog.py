#pysnake game
import time
import pygame
import numpy as np
import random

random.seed()

pygame.init()

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)
textsurface = myfont.render('GAME OVER', False, (255, 0, 0))

scorefont=pygame.font.SysFont('Comic Sans MS', 20)

textcont = scorefont.render('Press space to continue, escape to quit', False, (255, 0, 0))

def put_score(score):
    score_text=scorefont.render('Score: {}'.format(score),False, (0, 30, 250))
    screen.blit(score_text,(220,0))
    pygame.display.flip()

def draw_user_name():
    key=pygame.key.get_pressed()

    

maxx=300
maxy=300

color=(0,200,0)

screen = pygame.display.set_mode((maxx, maxy))
done = False
is_blue = True
x = 120
y = 120

tmax=.5

clock = pygame.time.Clock()

step=10

dirtion=np.array([0,-1]) #-y direction
coord=np.array([x,y])

score=0

snake=[coord]

def move(r,dr,step):
    #time.sleep(1)
    r+=dr*step
    if r[0]<0:
        r[0]+=maxx
    if r[1]<0:
        r[1]+=maxy
    if r[0]>=maxx:
        r[0]-=maxx
    if r[1]>=maxy:
        r[1]-=maxy
    return r

t=t1=0

def center(w):
    return np.array([random.randint(0,maxx/w-1)*w,random.randint(0,maxy/w-1)*w])

def putfood(screen, w, center):
    pygame.draw.rect(screen, (200,50,10), pygame.Rect(center[0],center[1], w, w))

eaten=False

centre=center(step)

def draw_snake(bodies):
    for body in bodies:
        pygame.draw.rect(screen, color, pygame.Rect(body[0],body[1], step, step))

def move_snake(bodies, dr, step):
    head=move(bodies[0].copy(), dr, step)
    ate=False
    for body in bodies:
        if np.array_equal(head,body):
            ate=True
    ans=[head]+bodies[:-1].copy() if len(bodies)>1 else [np.asarray(head)]
    return ans, ate

eatself=False

dirtion1=None

while not done:
    if eatself:
        screen.blit(textsurface,(100,100))
        #time.sleep(1)
        screen.blit(textcont,(25,120))
        Key = pygame.key.get_pressed()
        #print(Key)
        if Key[pygame.K_SPACE]:
            eatself=False
            snake=[coord]
            score=0
            continue
        if Key[pygame.K_ESCAPE]:
            done=True
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        continue
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:  dirtion1 = np.array([0,-1]) 
    if pressed[pygame.K_DOWN]: dirtion1 = np.array([0,1])
    if pressed[pygame.K_LEFT]: dirtion1 = np.array([-1,0])
    if pressed[pygame.K_RIGHT]: dirtion1 = np.array([1,0])
    if pressed[pygame.K_ESCAPE]: done=True
    if pressed[pygame.K_END]: eatself=True
    if type(dirtion1) != type(None) and not np.array_equal(dirtion,-dirtion1): dirtion=dirtion1
    dirtion1=None
    if t-t1>=.05:
        #print(snake)
        screen.fill((0,0,0))
        if np.array_equal(centre,snake[0]):
            eaten=True
        snake, eatself=move_snake(snake,dirtion,step)
        putfood(screen, step, centre)
        if eaten:
            score+=1
            head=move(snake[0].copy(),dirtion,step)
            snake=[head]+snake
            centre=center(step)
            eaten=False
        draw_snake(snake)
        t1=t
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    put_score(score)
    pygame.display.flip()
    t+=clock.tick(25)/1000


