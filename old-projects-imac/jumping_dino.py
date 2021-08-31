import pygame
import random
import pickle

pygame.init()
screen=pygame.display.set_mode([1000,500])
Image='/Users/daniel/Desktop/googe_dino.png'
IMage=pygame.image.load(Image)
steve=pygame.transform.smoothscale(IMage,[int(IMage.get_size()[0]/5),int(IMage.get_size()[1]/5)])
steve_mask=pygame.mask.from_surface(steve)
dead_steve_image='/Users/daniel/Desktop/dead_steve.png'
dead_steve_loaded=pygame.image.load(dead_steve_image)
dead_steve=pygame.transform.smoothscale(dead_steve_loaded,[int(dead_steve_loaded.get_size()[0]*2),int(dead_steve_loaded.get_size()[1]*2)])
puase_image='/Users/daniel/Desktop/puase_button.png'
puase=pygame.image.load(puase_image)
puase_rect=puase.get_rect(center=[950,50])
play_image='/Users/daniel/Desktop/play_button.png'
play_loaded=pygame.image.load(play_image)
play=pygame.transform.smoothscale(play_loaded,[int(play_loaded.get_size()[0]*3),int(play_loaded.get_size()[1]*3)])
play_rect=play.get_rect(center=screen.get_rect().center)
heart_image='/Users/daniel/Desktop/life.png'
heart_loaded=pygame.image.load(heart_image)
heart=pygame.transform.smoothscale(heart_loaded,[int(heart_loaded.get_size()[0]/2),int(heart_loaded.get_size()[1]/2)])
heart1_rect=heart.get_rect(center=[screen.get_rect().centerx-100,50])
heart2_rect=heart.get_rect(center=[screen.get_rect().centerx,50])
heart3_rect=heart.get_rect(center=[screen.get_rect().centerx+100,50])
heart_rects=[heart1_rect,heart2_rect,heart3_rect]
speed=5
non_cactus_counter=100
def_speed_counter=500
speed_counter=def_speed_counter
life_loss_cooldown=25
life_lost=False
try:
    hi_score_file=open('dino_hi_score.txt','r')
    hi_score=pickle.load(hi_score_file)
    hi_score_file.close()
except:
    hi_score=0
score=0
cacti=[]
def_height=325
height=def_height
jumping=False
running=True
fall_fast=False
dead=False
lives=3

class Cactus():
    def __init__(self,image_file,x_pos):
        self.image=pygame.image.load(image_file)
        self.rect=self.image.get_rect(center=[x_pos,370])
        self.mask=pygame.mask.from_surface(self.image)
        
    def draw(self):
        screen.blit(self.image,self.rect)

def update_display():
    pygame.display.flip()
    pygame.event.peek()
        
def draw(steve_height):
    screen.fill([255,255,255])
    pygame.draw.line(screen,[0,0,0],[0,400],[1000,400],1)
    screen.blit(steve,[50,steve_height])
    print_message('high score: %i'%hi_score,50,[150,50],(0,0,0))
    print_message('score: %i'%(score//3),50,[100,100],(0,0,0))
    for cactus in cacti:
        cactus.draw()
    for i in range(lives):
        screen.blit(heart,heart_rects[i])
    screen.blit(puase,puase_rect)
    update_display()

def print_message(string,size,center_pos,color):
    font=pygame.font.Font(None,size)
    message=font.render(string,1,color)
    rect=message.get_rect(center=center_pos)
    screen.blit(message,rect)

def puase_protocal():
    screen.fill([255,255,255])
    screen.blit(play,play_rect)
    update_display()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    return

while running:
    if lives==0:
        dead=True
        running=False
    if speed>50:
        speed=50
    if jumping:
        height-=4
    if height<=150:
        jumping=False
    if not jumping:
        if height<def_height:
            height+=4
        else:
            height=def_height
    if fall_fast:
        if height<def_height:
            height+=10
        else:
            fall_fast=False
            jumping=False
            height=def_height
    if random.randint(1,200-speed*2)==1:
        if len(cacti)<2:
            cactus=Cactus('/Users/daniel/Desktop/cactus.png',1100)
            cacti.append(cactus)
            non_cactus_counter=100
    steve_pos=steve.get_rect()
    steve_pos.topleft=50,height
    speed_counter-=1
    if speed_counter==0:
        speed+=1
        speed_counter=def_speed_counter
    for cactus in cacti:
        cactus.rect.centerx-=speed
        if cactus.rect.centerx<=-50:
            cacti.remove(cactus)
        offset_x, offset_y = (steve_pos.left - cactus.rect.left), (steve_pos.top - cactus.rect.top)
        if (cactus.mask.overlap(steve_mask, (offset_x, offset_y)) != None):
            if life_loss_cooldown==25:
                lives-=1
                life_lost=True
    if hi_score<score//3:
        hi_score=score//3
    if len(cacti)==0:
        non_cactus_counter-=1
    if non_cactus_counter==0:
        cactus=Cactus('/Users/daniel/Desktop/cactus.png',1100)
        cacti.append(cactus)
        non_cactus_counter=100
    if life_lost:
        life_loss_cooldown-=1
    if life_loss_cooldown==0:
        life_loss_cooldown=25
        life_lost=False
    score+=0.5
    draw(height)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                if height==def_height:
                    jumping=True
            if event.key==pygame.K_UP:
                if height==def_height:
                    jumping=True
            if event.key==pygame.K_DOWN:
                jumping==False
                fall_fast=True
        if event.type==pygame.MOUSEBUTTONDOWN:
            if puase_rect.collidepoint(pygame.mouse.get_pos()):
                puase_protocal()

hi_score_file=open('dino_hi_score.txt','w')
pickle.dump(hi_score,hi_score_file)
hi_score_file.close()
if dead:
    screen.fill([255,255,255])
    pygame.draw.line(screen,[0,0,0],[0,400],[1000,400],1)
    screen.blit(dead_steve,[50,height])
    for cactus in cacti:
        cactus.draw()
    print_message('high score: %i'%hi_score,50,[150,50],(0,0,0))
    print_message('score: %i'%(score//3),50,[100,100],(0,0,0))
    print_message('You lose!',150,screen.get_rect().center,(0,0,0))
    update_display()
pygame.quit()
        
