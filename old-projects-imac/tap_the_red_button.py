import pygame

screen_width=1000
screen_height=1000
button_width=300
button_height=200
running=True
pressed=0
font_size=50
level=1
times=[60,55,50,45,40,35,30,25,20,15]
winning_clicks=200
rect=pygame.Rect(0,0,button_width,button_height)
rect.center=(screen_width/2,screen_height/2)

pygame.init()
screen=pygame.display.set_mode([screen_width, screen_height])

def update_display():
    pygame.display.flip()
    pygame.event.peek()

def draw():
    screen.fill([255,255,255])
    pygame.draw.rect(screen,[255,0,0],rect,0)
    
    p_str='presses: %i'%pressed
    p_font=pygame.font.Font(None,font_size)
    p_print=p_font.render(p_str,1,(0,0,0))
    p_rect=p_print.get_rect(center=rect.center)
    screen.blit(p_print, p_rect)

    t_str='time: %i'%time
    t_print=p_font.render(t_str,1,(0,0,0))
    screen.blit(t_print,[10,50])

    l_str='level: %i'%level
    l_print=p_font.render(l_str,1,(0,0,0))
    screen.blit(l_print,[10,150])
    
    update_display()

def entry_screen():
    global winning_clicks
    screen.fill([0,0,0])
    update_display()
    s_str='Presenting...'
    for i in range(1,151):
        s_font=pygame.font.Font(None,font_size+i)
        s_print=s_font.render(s_str,1,(255,0,0))
        s_rect=s_print.get_rect(center=screen.get_rect().center)
        screen.fill([0,0,0])
        screen.blit(s_print,s_rect)
        update_display()
        pygame.time.delay(10)
    pygame.time.delay(1000)
    m_str='Press the Red Button!!!'
    m_font=pygame.font.Font(None,font_size+50)
    m_print=m_font.render(m_str,1,(255,0,0))
    m_rect=m_print.get_rect(centery=screen.get_rect().centery)
    for i in range (1,(screen_width/2)+1):
        m_rect.centerx=i
        screen.fill([0,0,0])
        screen.blit(m_print,m_rect)
        update_display()
    pygame.time.delay(1000)
    level_intro()
    return

def draw_play_button():
    pygame.draw.rect(screen,[255,0,0],rect,0)
    p_str='Play'
    p_font=pygame.font.Font(None,font_size)
    p_print=p_font.render(p_str,1,(0,0,0))
    p_rect=p_print.get_rect(center=rect.center)
    screen.blit(p_print,p_rect)
    update_display()
    while True:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(pygame.mouse.get_pos()):
                    return
    

def level_intro():
    screen.fill([0,0,0])
    e_str="Can you click %i times in %i seconds?"%(winning_clicks,65-5*level)
    e_font=pygame.font.Font(None,font_size)
    e_print=e_font.render(e_str,1,(255,0,0))
    e_rect=e_print.get_rect(centerx=screen.get_rect().centerx)
    
    r_str='Level %i'%level
    r_font=pygame.font.Font(None,font_size+150)
    r_print=r_font.render(r_str,1,(255,0,0))
    r_rect=r_print.get_rect(center=screen.get_rect().center)
    screen.blit(r_print,r_rect)
    update_display()
    pygame.time.delay(3000)
    
    for i in range(1,(screen_height/2)+1):
        e_rect.centery=i
        screen.fill([0,0,0])
        screen.blit(e_print,e_rect)
        update_display()
    pygame.time.delay(3000)
    screen.fill([0,0,0])
    draw_play_button()
    update_display()
    return

def loss_screen():
    global running
    l_str='You lose!'
    l_font=pygame.font.Font(None,font_size)
    l_print=l_font.render(l_str,1,(255,0,0))
    l_rect=l_print.get_rect(center=screen.get_rect().center)
    screen.blit(l_print,l_rect)
    update_display()
    for i in range(1,256):
        screen.fill([255-i,255-i,255-i])
        screen.blit(l_print,l_rect)
        pygame.time.delay(10)
        update_display()
    
    running=False
    return

def win_screen():
    global running,level,init_time,pressed
    w_str='You win!'
    w_font=pygame.font.Font(None,font_size+150)
    w_print=w_font.render(w_str,1,(255,0,0))
    w_rect=w_print.get_rect(center=screen.get_rect().center)
    screen.blit(w_print,w_rect)
    update_display()
    for i in range(1,256):
        screen.fill([255-i,255-i,255-i])
        screen.blit(w_print,w_rect)
        pygame.time.delay(10)
        update_display()
    pygame.time.delay(2000)
    level+=1
    if level>10:
        t_str='You beat the game!'
        for i in range(1,101):
            t_font=pygame.font.Font(None,font_size+i)
            t_print=t_font.render(t_str,1,(255,0,0))
            t_rect=t_print.get_rect(center=screen.get_rect().center)
            screen.fill([0,0,0])
            screen.blit(t_print,t_rect)
            update_display()
        running=False
    else:
        level_intro()
        pressed=0
        init_time=pygame.time.get_ticks()
    return

entry_screen()
init_time=pygame.time.get_ticks()

while running:
    time=times[level-1]-(pygame.time.get_ticks()-init_time)//1000
    draw()
    if time<=0 and pressed<winning_clicks:
        loss_screen()
    elif time>0 and pressed>=winning_clicks:
        win_screen()
    for event in pygame.event.get():
        if event.type==pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pressed+=1

pygame.quit()
