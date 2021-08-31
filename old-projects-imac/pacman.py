import pygame
import random

pygame.init()
screen_width,screen_height=1400,750
screen=pygame.display.set_mode([screen_width,screen_height])
counter=0
position1s=[]
position2s=[]
counter_direction='up'
squares=[]
size=50
speed=10
circles=[]
running=True
direction='right'
requested_direction=''
score=0
ghosts=[]

for i in range(10):
    position1s.append(float(i)/10)
    position2s.append(6.28+float(-i)/10)
class Ghost():
    def __init__(self,pos,direction,speed,image_file):
        self.direction=direction
        self.speed=speed
        self.pos=pos
        self.image=pygame.image.load(image_file)
        self.image=pygame.transform.smoothscale(self.image,[size,size])
        self.rect=self.image.get_rect(center=self.pos)
        self.requested_direction=direction
        
    def move(self):
        if random.randint(1, 100)==1:
            self.requested_direction=('up','down','left','right')[random.randint(0,3)]
        for circle in circles:
            if self.rect.center==circle.pos:
                self.direction=self.requested_direction
        if self.direction=='up':
            self.rect.centery-=speed
        if self.direction=='down':
            self.rect.centery+=speed
        if self.direction=='left':
            self.rect.centerx-=speed
        if self.direction=='right':
            self.rect.centerx+=speed
    
    def draw(self):
        screen.blit(self.image,self.rect)

class Circle():
    def __init__(self,pos,speed,size,color):
        self.pos=tuple(pos)
        self.speed=speed
        self.size=size
        self.color=color
        self.eaten=False

    def draw(self):
        pygame.draw.circle(screen,self.color,self.pos,self.size,0)

def update_display():
    pygame.display.flip()
    pygame.event.peek()

def print_message(string,size,corner,center_pos,which_one,color):
    font=pygame.font.Font(None,size)
    message=font.render(string,1,color)
    if which_one=='corner':
        rect=message.get_rect(topleft=corner)
    else:
        rect=message.get_rect(center=center_pos)
    screen.blit(message,rect)

def draw():
    screen.fill([0,0,155])
    for circle in circles:
        if not circle.eaten:
            circle.draw()
    for ghost in ghosts:
        ghost.draw()
    pacman_bbox=[x_pos-size/2,y_pos-size/2,size,size]
    if direction=='right':
        pygame.draw.arc(screen,[255,255,0],pacman_bbox, position1s[counter], position2s[counter], size/2)
    if direction=='up':
        pygame.draw.arc(screen,[255,255,0],pacman_bbox, position1s[counter]+1.5708, position2s[counter]+1.5708, size/2)
    if direction=='left':
        pygame.draw.arc(screen,[255,255,0],pacman_bbox, position1s[counter]+3.1416, position2s[counter]+3.1416, size/2)
    if direction=='down':
        pygame.draw.arc(screen,[255,255,0],pacman_bbox, position1s[counter]-1.5708, position2s[counter]-1.5708, size/2)
    print_message("Score: %i"%score,50,[15,15],None,'corner',(0,0,0))
    update_display()

def move():
    global x_pos,y_pos
    if direction=='up':
        y_pos-=speed
    if direction=='right':
        x_pos+=speed
    if direction=='down':
        y_pos+=speed
    if direction=='left':
        x_pos-=speed
    for ghost in ghosts:
        ghost.move()

def warping():
    global x_pos,y_pos
    if x_pos<=-size/2:
        x_pos=screen_width+size/2
    elif x_pos>=screen_width+size/2:
        x_pos=-size/2
    if y_pos<=-size/2:
        y_pos=screen_height+size/2
    elif y_pos>=screen_height+size/2:
        y_pos=-size/2
    for ghost in ghosts:
        if ghost.rect.centerx<=-size/2:
            ghost.rect.centerx=screen_width+size/2
        elif ghost.rect.centerx>=screen_width+size/2:
            ghost.rect.centerx=-size/2
        if ghost.rect.centery<=-size/2:
            ghost.rect.centery=screen_height+size/2
        elif ghost.rect.centery>=screen_height+size/2:
            ghost.rect.centery=-size/2

def check_collison():
    global running
    for ghost in ghosts:
        if abs(ghost.rect.centerx-x_pos)<=size-1 and abs(ghost.rect.centery-y_pos)<=size-1:
            running=False
            return

for i in range(25, screen_height, 50):
        for x in range(25, screen_width, 50):
            circle=Circle([x,i],5,size/10,[255,255,255])
            circles.append(circle)
ghost=Ghost(circles[len(circles)/2].pos,'up',speed,'/Users/daniel/Desktop/redghost.png')
ghosts.append(ghost)
ghost=Ghost(circles[len(circles)/2].pos,'down',speed,'/Users/daniel/Desktop/blueghost.png')
ghosts.append(ghost)
ghost=Ghost(circles[len(circles)/2].pos,'left',speed,'/Users/daniel/Desktop/greenghost.png')
ghosts.append(ghost)
ghost=Ghost(circles[len(circles)/2].pos,'right',speed,'/Users/daniel/Desktop/yellowghost.png')
ghosts.append(ghost)
x_pos=circles[0].pos[0]
y_pos=circles[0].pos[1]
while running:
    pygame.time.delay(25)
    for circle in list(circles):
        if circle.pos==(x_pos, y_pos):
            if not circle.eaten:
                score+=1
                circle.eaten=True
        if x_pos==circle.pos[0] and y_pos==circle.pos[1]:
            if requested_direction=='left':
                direction='left'
            if requested_direction=='right':
                direction='right'
            if requested_direction=='up':
                direction='up'
            if requested_direction=='down':
                direction='down'
            requested_direction=''
    win=True
    for circle in list(circles):
        if not circle.eaten:
            win=False
    if win:
        running=False
        screen.fill([0,0,0])
        print_message("You Win",150,None,screen.get_rect().center,None,(255,0,0))
        update_display()
        pygame.time.delay(5000)
        break
    move()
    warping()
    draw()
    check_collison()
    if counter_direction=='up':
        counter+=1
    else:
        counter-=1
    if counter==8:
        counter_direction='down'
    if counter==0:
        counter_direction='up'
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                requested_direction='up'
            if event.key==pygame.K_DOWN:
                requested_direction='down'
            if event.key==pygame.K_LEFT:
                requested_direction='left'
            if event.key==pygame.K_RIGHT:
                requested_direction='right'
pygame.quit()
