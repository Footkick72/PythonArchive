import pygame
import pickle
import colorsys

screen_width,screen_height=400,600
gravity=-0.002
thrust=0
velocity=0
ticks=60
land_velocity=10.0/ticks
good_land_velocity=5.0/ticks
fuel=10
init_fuel=fuel
start_game_fuel=fuel
try:
    user_file=open('lander_user_file.txt')
    users=pickle.load(user_file)
    user_file.close()
except:
    users={}

pygame.init()
screen=pygame.display.set_mode([screen_width,screen_height])

lander=pygame.image.load('/Users/daniel/Desktop/moon_lander2.png')
lander_rect=lander.get_rect(center=[screen_width/2+25,50])
lander_mask=pygame.mask.from_surface(lander)
landery=lander_rect.centery
init_landery=landery
moon=pygame.image.load('/Users/daniel/Desktop/moon.png')
moon_rect=moon.get_rect(midbottom=screen.get_rect().midbottom)
moon_mask=pygame.mask.from_surface(moon)
control_rect=pygame.Rect(50,screen_height-300,10,200)
control_lever=pygame.Rect(0,0,30,15)
control_lever.center=control_rect.center
control_outline=pygame.Rect(0,0,control_rect.width+4,control_rect.height+4)
control_outline.center=control_rect.center
fuel_guage=pygame.Rect(25,105,100,10)
init_fuel_width=fuel_guage.width
fuel_outline=pygame.Rect(0,0,fuel_guage.width+2,fuel_guage.height+2)
fuel_outline.center=fuel_guage.center

clock=pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.music.load('/Users/daniel/Documents/lander_music.mp3')
pygame.mixer.music.play()

XS_font=pygame.font.Font(None,25)
S_font=pygame.font.Font(None,50)
M_font=pygame.font.Font(None,75)
L_font=pygame.font.Font(None,100)
XL_font=pygame.font.Font(None,150)

running=True
selected=False
restart=True

def update_display():
    pygame.display.flip()
    pygame.event.peek()

def draw():
    screen.fill([0,0,0])
    screen.blit(moon,moon_rect)
    lander_rect.bottom=int(round(landery))
    screen.blit(lander,lander_rect)
    print_message('Velocity: %imps'%(velocity*ticks),XS_font,[160,160,160],topleft=[25,25])
    print_message('Height: %im'%(moon_rect.top-landery+3),XS_font,[160,160,160],topleft=[25,50])
    print_message('Level: %i'%level,XS_font,[160,160,160],topleft=[25,75])
    x=lander_rect.midbottom
    pygame.draw.polygon(screen,[255,128,0],[[x[0]-5,x[1]-5],[x[0]+5,x[1]-5],[x[0],x[1]+thrust*10000-5]],0)
    pygame.draw.rect(screen,[50,50,50],control_outline,0)
    pygame.draw.rect(screen,[255,0,0],control_rect,0)
    pygame.draw.rect(screen,[128,128,128],control_lever,0)
    pygame.draw.rect(screen,[160,160,160],fuel_outline,0)
    color=list(colorsys.hsv_to_rgb(float(fuel)/init_fuel*120/360,1,1))
    for i in range(3):
        color[i]=int(round(color[i]*255))
    pygame.draw.rect(screen,color,fuel_guage,0)
    update_display()

def print_message(string,font,color,**keywords):
    message=font.render(string,1,color)
    rect=message.get_rect(**keywords)
    screen.blit(message,rect)

def get_username():
    global running
    username_rect=pygame.Rect(0,0,100,20)
    username_rect.center=[screen_width/2,screen_height/2-50]
    username=['u','s','e','r','n','a','m','e']
    selected=False
    while True:
        screen.fill([255,255,255])
        pygame.draw.rect(screen,[200,200,200],username_rect,0)
        print_message('Enter username.',XS_font,[0,0,0],center=[screen_width/2,screen_height/2+100])
        print_message(''.join(username),XS_font,[128,128,128],center=username_rect.center)
        update_display()
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if username_rect.collidepoint(pygame.mouse.get_pos()):
                    selected=True
                    username=[]
            if event.type==pygame.KEYDOWN:
                if selected:
                    if event.key==pygame.K_RETURN:
                        return ''.join(username)
                    if event.key==pygame.K_BACKSPACE:
                        username=username[:len(username)-1]
                    else:
                        if len(username)<11:
                            username.append(translate(event))

def translate(event):
    letters=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    if pygame.key.name(event.key) in letters:
        return pygame.key.name(event.key)
    else:
        return ' '

username=get_username()
try:
    level=users[username]
except:
    level=1
while running:
    if restart:
        if start_game_fuel!=fuel:
            pygame.time.delay(5000)
        fuel=start_game_fuel*(0.9**(level-1))
        init_fuel=fuel
        restart=False
        landery=init_landery
        velocity=0
        selected=False
        control_lever.center=control_rect.center
    if selected:
        control_lever.centery=pygame.mouse.get_pos()[1]
    if control_lever.centery<control_rect.midtop[1]:
        control_lever.centery=control_rect.midtop[1]
    if control_lever.centery>control_rect.midbottom[1]:
        control_lever.centery=control_rect.midbottom[1]
    thrust=float(control_rect.midbottom[1]-control_lever.centery)/control_rect.height
    thrust*=-1.5*gravity
    velocity+=gravity
    velocity+=thrust
    landery-=velocity
    draw()
    fuel-=thrust
    fuel_guage.width=fuel*(init_fuel_width/init_fuel)
    if fuel<=0:
        control_lever.centery=control_rect.midbottom[1]
        selected=False
        fuel_guage.width=0
    offset_x,offset_y=(lander_rect.left-moon_rect.left),(lander_rect.top-moon_rect.top)
    if (moon_mask.overlap(lander_mask,(offset_x,offset_y))!=None):
        if -velocity<=good_land_velocity:
            level+=1
            restart=True
            print_message('Great landing. I hear NASA is hiring.',XS_font,[255,255,255],center=[screen.get_rect().centerx,screen.get_rect().centery-50])
            update_display()
        elif good_land_velocity<-velocity<=land_velocity:
            level+=1
            restart=True
            print_message('A bit bumpy, but you got the job done.',XS_font,[255,255,255],center=[screen.get_rect().centerx,screen.get_rect().centery-50])
            update_display()
        else:
            print_message('You destroyed a billion-dollar spacecraft!',XS_font,[255,255,255],center=[screen.get_rect().centerx,screen.get_rect().centery-50])
            update_display()
            while running:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        running=False
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if control_lever.collidepoint(pygame.mouse.get_pos()):
                selected=True
        if event.type==pygame.MOUSEBUTTONUP:
            selected=False
    clock.tick(ticks)
users[username]=level
user_file=open('lander_user_file.txt','w')
pickle.dump(users,user_file)
user_file.close()
pygame.quit()
