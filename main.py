## Imports
from tkinter import * 
import random as rd
import numpy as np
from math import *
import time

## Settings
dt = 0.03
width = 800
height = 500
mowerSize = 10
pathWidth = 10 #Mower's path width
#walls = [(50,400),(50,450),(750,450),(750,50),(650,50),(650,400)]
walls = [(50,250),(50,450),(750,450),(750,50),(250,50),(250,250)]
#walls = [(50,50),(50,450),(750,450),(750,50)]
colorBeforeCut = '#020'
colorAfterCut = '#060'
defaultSpeed = 500

'''
listCoords = []
listCoordsOnWall= []
'''

## Classes
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Tondeuse dans un jardin')
        self._garden = Garden(self,width=width,height=height)
        self._bottomCommands = Frame(self)
        self._rightCommands = Frame(self)
        self._start = Button(self._bottomCommands,text='Démarrer',command=self._garden.start)
        self._stop = Button(self._bottomCommands,text='Stop',command=self._garden.stop)
        self._quit = Button(self._bottomCommands,text='Quitter',command=self.quit)
        self._speedScale = Scale(self._rightCommands,label='Vitesse',command=self._garden.updateMowerSpeed,from_=0,to=5000)
        self._speedScale.set(defaultSpeed)
        self._clearButton = Button(self._rightCommands,text='Effacer',command=self._garden.clear)
        
        self._rightCommands.pack(padx=10,pady=10,side=RIGHT)
        self._speedScale.pack(side=TOP,pady=50)
        self._clearButton.pack(side=TOP,pady=50)

        self._garden.pack(padx=10,pady=10)

        self._bottomCommands.pack(padx=10,pady=10)
        self._start.pack(side=LEFT)
        self._stop.pack(side=LEFT)
        self._quit.pack(side=LEFT)

        #Binding events
        self._garden.bind("<Button-1>",self._garden.popTurtle)

    def quit(self):
        self.destroy()


class Garden(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._turtlePopped = False
        self._stopped = True
        self._walls = walls
        self._nbWalls = len(self._walls)
        self._onWallIndex = -1
        #self._currentLineId = -1
        self._mowerPath = [-1] #List of the id of each line 
        self._grass = self.create_polygon(self._walls,fill=colorBeforeCut)
        self._fence = self.create_polygon(self._walls,fill='',width=10,outline='black')

    def popTurtle(self,event):
        if self._turtlePopped:
            self.delete(self._turtle)
            self._mower.moveTo(event.x,event.y)
        else:
            self._mower = Mower(event.x,event.y,mowerSize)
            self._turtlePopped = True
        self._turtle = self.create_oval(self._mower._x - self._mower._size, self._mower._y - self._mower._size, self._mower._x + self._mower._size, self._mower._y + self._mower._size, outline='grey',width=4,fill='red')

    def start(self):
        if self._stopped and self._turtlePopped:
            self._stopped = False
            self.show()

    def stop(self):
        self._stopped = True

    def clear(self):
        for lineId in self._mowerPath:
            self.delete(lineId)
        self._mowerPath = [-1]

    def updateMowerSpeed(self,speed):
        if self._turtlePopped:
            self._mower._speed = int(speed)
        
    def show(self):
        if not self._stopped:
            t1 = time.time()
            self.moveMower()
            t2 = time.time()
            #print("Temps calcul :",1000*(t2-t1)," x = ",self._mower._x)
            #time.sleep(0.1)
            self.after(max(int(1000*(dt-(t2-t1))),1),self.show)

    def moveMower(self):
        bouncesWall = False
        distBounce = -1
        #Fictive mower path (if there is no wall)
        fictive_dx = self._mower._speed*cos(self._mower._theta)*dt
        #print(fictive_dx)
        fictive_dy = self._mower._speed*sin(self._mower._theta)*dt
        for i in range(self._nbWalls):
            if i != self._onWallIndex:
                #Coordinates of the concerned wall
                x3,y3 = self._walls[i-1]
                x4,y4 = self._walls[i]
                wall = Segment(x3,y3,x4,y4)

                path = Segment(self._mower._x,self._mower._y,self._mower._x + fictive_dx,self._mower._y + fictive_dy)

                if not path.parallel(wall):
                #Calcul of the eventual intersection between the wall and the path of the mower
                    x0,y0,doesCross = path.intersection(wall)
                    if doesCross:
                        distFictiveBounce = (x0-self._mower._x)**2+(y0-self._mower._y)**2
                        if not bouncesWall:
                            #If this wall is the first that mignt be crossed
                            bouncesWall = True
                            distBounce = distFictiveBounce
                        elif distBounce > distFictiveBounce:
                            #Another wall might be crossed : the turtle will bounce on the nearest one
                            distBounce = distFictiveBounce
                        #Coordinates of the bound are saved
                        bound_x = x0
                        bound_y = y0
                        dx = bound_x - self._mower._x
                        dy = bound_y - self._mower._y
                        wallIndex = i

        if not bouncesWall:
            dx,dy = fictive_dx,fictive_dy
        self.move(self._turtle,dx,dy)
        if self._mowerPath[-1] < 0:
            #In that case, a new line is created (the mower starts to cut the grass or has just bounced on a wall)
            self._currentLineX0 = self._mower._x
            self._currentLineY0 = self._mower._y
            # listCoordsOnWall.append((self._currentLineX0,self._currentLineY0))
        else:
            self.delete(self._mowerPath[-1])
        self._mowerPath[-1] = self.create_line(self._currentLineX0,self._currentLineY0,self._mower._x + dx,self._mower._y + dy,width=pathWidth,fill=colorAfterCut)
        #self.lower(self._currentLineId)
        self.lift(self._fence)
        self.lift(self._turtle)

        self._mower._x += dx
        self._mower._y += dy

        # listCoords.append((self._mower._x,self._mower._y))

        if bouncesWall:
            x3,y3 = self._walls[wallIndex-1]
            x4,y4 = self._walls[wallIndex]
            self._mower.changeDirection(x4-x3,y4-y3)
            self._onWallIndex = wallIndex
            self._mowerPath.append(-1)
        else:
            self._onWallIndex = -1 #Indicates that the mower isn't on a wall


class Mower():
    def __init__(self,x,y,size):
        self._size = size
        self._x = x
        self._y = y
        self._speed = defaultSpeed
        self._theta = np.pi/3
        self.updateSpeeds()

    def updateSpeeds(self):
        #Recalculates the the projections of speed (called when theta is changed)
        self._vx = self._speed*np.cos(self._theta)
        self._vy = self._speed*np.sin(self._theta)
        
    def changeDirection(self,vectWallX,vectWallY):#vectWallX and vectWallY are the coordinates of a vector parallel to the wall
        #Calculation of the vector normal to the wall, the one that points toward the garden
        if self._vy*vectWallX - vectWallY*self._vx < 0:
            vectNormalWallX,vectNormalWallY = -vectWallY,vectWallX
        else:
            vectNormalWallX,vectNormalWallY = vectWallY,-vectWallX
        phi = np.arctan2(vectNormalWallY,vectNormalWallX)
        #Calculation of a random angle
        self._theta = phi + np.pi*(rd.random()-0.5)
        self.updateSpeeds()

    def moveTo(self,x,y):
        self._x,self._y = x,y


class Segment():
    def __init__(self,x1,y1,x2,y2):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

    def getCoord(self):
        return (self._x1,self._y1,self._x2,self._y2)

    def getX(self):
        return (self._x1,self._x2)

    def getY(self):
        return (self._y1,self._y2)

    def intersection(self,otherSeg):
        #Gives the coordinates of the intersection point with an other segment (segment are extended)
        #The third output is True if the mower hits the wall
        x3,y3,x4,y4 = otherSeg.getCoord()
        x = ((y3*x4-x3*y4)*(self._x2-self._x1)-(x4-x3)*(self._x2*self._y1-self._x1*self._y2))/((self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1))
        y = ((y3*x4-x3*y4)*(self._y2-self._y1)-(y4-y3)*(self._x2*self._y1-self._x1*self._y2))/((self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1))
        return x,y,(self.contains(x,y) and otherSeg.contains(x,y))

    def parallel(self,otherSeg):
        x3,y3,x4,y4 = otherSeg.getCoord()
        return (self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1) == 0

    def vertical(self):
        return self._x1 == self._x2

    def contains(self,x0,y0):
        if self._x1 != self._x2:
            return x0 > min(self._x1,self._x2) and x0 <= max(self._x1,self._x2)
        else:
            return y0 > min(self._y1,self._y2) and y0 <= max(self._y1,self._y2)

            
## Calls
fenetre = FenPrincipale()
#fenetre.attributes('-zoomed',True)
fenetre.mainloop()

'''
print(listCoords)
str = '********************************************************************'
print(str+'\n'+str)
print(listCoordsOnWall)
'''