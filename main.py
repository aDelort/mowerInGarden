## Imports
from tkinter import * 
from random import *
import numpy as np

## Settings
dt = 0.1
largeur = 800
hauteur = 500

## Classes
class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._garden = Garden(self,width=largeur,height=hauteur,bg='green')
        self._commands = Frame(self)
        self._start = Button(self._commands,text='Démarrer',command=self.start)
        self._stop = Button(self._commands,text='Stop',command=self.stop)
        self._quit = Button(self._commands,text='Quitter',command=self.quit)
    
        self._garden.pack(padx=10,pady=10)
        self._commands.pack(padx=10,pady=10)
        self._start.pack(side=LEFT)
        self._stop.pack(side=LEFT)
        self._quit.pack(side=LEFT)


    def start(self):
        if self._garden._stopped:
            self._garden._stopped = False
            self._garden.show()

    def stop(self):
        self._garden._stopped = True

    '''def deleteAll(self):
        self._garden.deleteTraces()
        self.stop()'''

    def quit(self):
        self.destroy()

class Garden(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self._mower = Mower()
        self._turtle = self.create_oval(self._mower._x - self._mower._size, self._mower._y - self._mower._size, self._mower._x + self._mower._size, self._mower._y + self._mower._size, outline='grey',width=4,fill='red')
        self._stopped = True
        self._walls = [(0,250),(0,500),(800,500),(800,0),(250,0),(250,250)]
        self._nbWalls = len(self._walls)
        for i in range(self._nbWalls):
            self.create_line(self._walls[i-1],self._walls[i],width=10)
    
    def getDimensions(self):
        return [largeur,hauteur]
        
    def show(self):
        if not self._stopped:
            self.moveMower(dt)
            self.after(1,self.show)


    def moveMower(self,dt):
        distRebond = -1
        for i in range(self._nbWalls):
            #Coordinates of a wall
            x3,y3,x4,y4 = self._walls[i-1]+self._walls[i] #A CHANGER C MOCHE
            wall = Segment(x3,y3,x4,y4)

            #Fictive mower path (if there is no wall)
            path = Segment(self._mower._x,self._mower._y,self._mower._x + self._mower._vx*dt,self._mower._y + self._mower._vy*dt)

            #Calcul of the eventual intersection between the wall and the path of the mower
            x0,y0 = path.intersection(wall)

            if not path.parallel(wall):
                if not wall.vertical():
                    if path.intersects(wall,True):
                        distRebondTmp = (x0-self._mower._x)**2+(y0-self._mower._y)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = x3
                            my1R = y3
                            mx2R = x4
                            my2R = y4
                else:
                    if path.intersects(wall,False):
                        distRebondTmp = (x0-self._mower._x)**2+(y0-self._mower._y)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = x3
                            my1R = y3
                            mx2R = x4
                            my2R = y4
        if distRebond == -1:
            dx = self._mower._vx*dt
            dy = self._mower._vy*dt
            self.create_line(self._mower._x,self._mower._y,self._mower._x + dx,self._mower._y + dy,width=10)
            self._mower._x += dx
            self._mower._y += dy
            self.move(self._turtle,dx,dy)
        else:
            vectIntX = my2R - my1R
            vectIntY = -(mx2R - mx1R)
            if self._mower._vx*vectIntX + self._mower._vy*vectIntY > 0:
                vectIntX = -vectIntX
                vectIntY = -vectIntY
            angle = np.pi*random()
            newVx = self._mower._v*np.cos(angle)
            newVy = self._mower._v*np.sin(angle)
            if newVx*vectIntX + newVy*vectIntY < 0:
                newVx = -newVx
                newVy = -newVy
            self._mower._vx = newVx
            self._mower._vy = newVy

class Mower():
    def __init__(self):
        self._size = min(largeur,hauteur)/50
        self._x = 260
        self._y = 10
        self._v = (largeur**2+hauteur**2)/18000
        self._vx = self._v*np.sqrt(3)/2
        self._vy = self._v/2

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

    '''def set(self):
        pass'''

    def intersection(self,otherSeg):
        #Gives the coordinates of the intersection point with an other segment (segment are extended)
        x3,y3,x4,y4 = otherSeg.getCoord()
        x = ((y3*x4-x3*y4)*(self._x2-self._x1)-(x4-x3)*(self._x2*self._y1-self._x1*self._y2))/((self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1))
        y = ((y3*x4-x3*y4)*(self._y2-self._y1)-(y4-y3)*(self._x2*self._y1-self._x1*self._y2))/((self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1))
        return x,y

    def parallel(self,otherSeg):
        x3,y3,x4,y4 = otherSeg.getCoord()
        return (self._y2-self._y1)*(x4-x3)-(y4-y3)*(self._x2-self._x1) == 0

    def vertical(self):
        return self._x1 == self._x2

    def intersects(self,otherSeg,testX):
        #ENLEVER y0
        (x0,y0) = self.intersection(otherSeg)
        if testX:
            x3,x4 = otherSeg.getX()
            return x0 > min(self._x1,self._x2) and x0 <= max(self._x1,self._x2) and x0 > min(x3,x4) and x0 <= max(x3,x4)
        else:
            y3,y4 = otherSeg.getY()
            return y0 > min(self._y1,self._y2) and y0 < max(self._y1,self._y2) and y0 > min(y3,y4) and y0 < max(y3,y4)

            
## Calls
fenetre = FenPrincipale()
fenetre.mainloop()
