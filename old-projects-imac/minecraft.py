from math import *
import pygame

screen_width,screen_height=1500,1200
viewAngle=90
viewWidth=2*tan(viewAngle/2*pi/180)
viewHeight=viewWidth*(float(screen_height)/screen_width)
campos=[0,0,-5]
camTheta1=0
camTheta2=0
camdir=[0,0,1]
blocks=[]
running=True
faceInfo=[]
velocity=[0,0,0]
w_selected=False
selected_face=None
color=0
colors=[[0,0,0],[255,0,0],[0,255,0],[0,0,255],[255,255,0],[0,255,255],[255,0,255],[192,192,192],[255,128,0]]

pygame.init()
screen=pygame.display.set_mode([screen_width,screen_height])

hotbar_rect=pygame.Rect(0,screen_height-150,100*len(colors),100)
hotbar_rect.centerx=screen.get_rect().centerx

cursor=pygame.image.load('/Users/daniel/Desktop/mouse.png')
cursor_rect=cursor.get_rect(center=screen.get_rect().center)

class Face():
    def __init__(self,faceIndex,points,block,distance):
        self.faceIndex=faceIndex
        self.points=points
        self.block=block
        self.distance=distance

class Block():
    def __init__(self,xyz,color):
        x,y,z=xyz
        self.points=[[x,y,z],[x,y,z+1],[x+1,y,z],[x+1,y,z+1],[x,y+1,z],[x,y+1,z+1],[x+1,y+1,z],[x+1,y+1,z+1]]
        self.faces=[[0,1,3,2],[4,6,7,5],[0,2,6,4],[2,3,7,6],[0,4,5,1],[1,3,7,5]]
        self.color=color

    def faceColor(self,faceNum):
        return self.color

    def getAdjacent(self,index):
        x,y,z=self.points[0]
        if index==0:
            return [x,y-1,z]
        if index==1:
            return [x,y+1,z]
        if index==2:
            return [x,y,z-1]
        if index==3:
            return [x+1,y,z]
        if index==4:
            return [x-1,y,z]
        if index==5:
            return [x,y,z+1]

    def draw(self):
        global faceInfo
        points=[]
        projected=[]
        for point in self.points:
            x,y,z=getpos(point[0],point[1],point[2],camdir[0],camdir[1],camdir[2],campos[0],campos[1],campos[2])
            projected.append(convertCoordinates(x,y,z))
            points.append((x,y,z))
        for faceIndex in range(len(self.faces)):
            face=self.faces[faceIndex]
            faceprojected=[projected[i] for i in face]
            if all(p[0] != None for p in faceprojected):
                center=[0,0,0]
                for p in [points[i] for i in face]:
                    center[0]+=p[0]
                    center[1]+=p[1]
                    center[2]+=p[2]
                center[0]/=4
                center[1]/=4
                center[2]/=4
                distance=hypot(hypot(center[0],center[1]),center[2])
                faceInfo.append(Face(faceIndex,faceprojected,self,distance))

blocks.append(Block([0,2,6],[255,255,0]))
blocks.append(Block([0,3,6],[255,0,255]))
blocks.append(Block([0,4,6],[0,255,255]))
blocks.append(Block([-1,3,6],[0,0,255]))
blocks.append(Block([1,3,6],[255,0,0]))
blocks.append(Block([-1,-1,3],[0,255,0]))
blocks.append(Block([3,6,9],[200,200,200]))

def updateCamDir():
    global camdir
    camdir[0]=sin(camTheta2*pi/180)*cos(camTheta1*pi/180)
    camdir[1]=-sin(camTheta1*pi/180)
    camdir[2]=cos(camTheta1*pi/180)*cos(camTheta2*pi/180)

def draw():
    global faceInfo,selected_face
    faceInfo=[]
    updateCamDir()
    screen.fill([255,255,255])
    for block in blocks:
        block.draw()
    faceInfo.sort(key=lambda x: x.distance,reverse=True)
    selected_face=None
    for face in faceInfo:
        if pt_in_poly(screen.get_rect().center,face.points):
            selected_face=face
        pygame.draw.polygon(screen,face.block.faceColor(face.faceIndex),face.points,0)
        pygame.draw.polygon(screen,[0,0,0],face.points,2)
    pygame.draw.rect(screen,[128,128,128],hotbar_rect,0)
    for colornum in range(len(colors)):
        rect=pygame.Rect(0,0,100,100)
        rect.topleft=hotbar_rect.topleft
        rect.left+=colornum*100
        pygame.draw.rect(screen,[198,198,198],rect,4)
        if colornum==color:
            pygame.draw.rect(screen,[198,198,198],rect,10)
        rect2=pygame.Rect(0,0,50,50)
        rect2.center=rect.center
        pygame.draw.rect(screen,colors[colornum],rect2,0)
    screen.blit(cursor,cursor_rect)
    pygame.display.flip()

def rotate0y(xd,yd,x,y):
    theta=atan2(yd,xd)
    c=cos(theta)
    s=sin(theta)
    return (x*c+y*s,-x*s+y*c)

def rotate0yz(xd,yd,zd,x,y,z):
    xyN=rotate0y(xd,yd,x,y)
    xd=hypot(xd,yd)
    x=xyN[0]
    y=xyN[1]
    xzN=rotate0y(xd,zd,x,z)
    x=xzN[0]
    z=xzN[1]
    return (x,y,z)

def pt_in_poly(pt, poly):
    testX, testY = pt
    last = -1
    answer = False
    for now in xrange(0, len(poly)):
        nowX, nowY = poly[now]
        lastX, lastY = poly[last]
        if (nowY > testY) != (lastY > testY) and (testX < (lastX - nowX) * (testY - nowY)/(lastY - nowY) + nowX):
            answer = not answer
        last += 1
    return answer

def rotate0xy(xd,yd,zd,x,y,z):
    zxyN=rotate0yz(zd,xd,yd,z,x,y)
    x=zxyN[1]
    y=zxyN[2]
    z=zxyN[0]
    return(x,y,z)

def getpos(x,y,z,xd,yd,zd,xc,yc,zc):
    x-=xc
    y-=yc
    z-=zc
    xyzN=rotate0xy(xd,yd,zd,x,y,z)
    if xyzN[2] < 1:
        return (None,None,None)
    return xyzN

def convertCoordinates(x,y,z):
    if x == None:
        return (x,y)
    x/=z
    y/=z
    x*=screen_width/viewWidth
    y*=screen_height/viewHeight
    y=-y
    x+=screen_width/2
    y+=screen_height/2
    return (int(x),int(y))

while running:
#    if w_selected:
#        velocity[0]+=float(camdir[0])/10
#        velocity[2]+=float(camdir[2])/10
#    for i in range(len(velocity)):
#        if i==1:
#            velocity[i]-=0.1
#        else:
#            velocity[i]-=0.05
#        if velocity[i]>0.2:
#            velocity[i]=0.2
#        if velocity[i]<0:
#            velocity[i]=0
#    campos[0]+=velocity[0]
#    campos[1]+=velocity[1]
#    campos[2]+=velocity[2]
    draw()
    mousepos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_w:
                campos[0]+=camdir[0]
                campos[2]+=camdir[2]
#                w_selected=True
            if event.key==pygame.K_s:
                campos[0]-=camdir[0]
                campos[2]-=camdir[2]
            if event.key==pygame.K_a:
                campos[0]-=camdir[2]
                campos[2]+=camdir[0]
            if event.key==pygame.K_d:
                campos[0]+=camdir[2]
                campos[2]-=camdir[0]
            if event.key==pygame.K_SPACE:
                campos[1]+=1
            if event.key==pygame.K_LSHIFT:
                campos[1]-=1
            if event.key==pygame.K_q:
                running=False
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_w:
                w_selected=False
        if event.type==pygame.MOUSEMOTION:
            x_change=int(round(pygame.mouse.get_pos()[0]))-int(round(mousepos[0]))
            y_change=int(round(pygame.mouse.get_pos()[1]))-int(round(mousepos[1]))
            y_change=-y_change
            camTheta2+=float(x_change)/10
            camTheta1-=float(y_change)/10
            pygame.mouse.set_pos(screen.get_rect().center)
            pygame.mouse.set_visible=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if selected_face!=None:
                if event.button==3:
                    blocks.append(Block(selected_face.block.getAdjacent(selected_face.faceIndex),colors[color]))
                if event.button==1:
                    blocks.remove(selected_face.block)
            if event.button==5:
                color+=1
                if color>len(colors)-1:
                    color=0
            if event.button==4:
                color-=1
                if color<0:
                    color=len(colors)-1

pygame.quit()
