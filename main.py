## Imports
from tkinter import * 
from random import *
import numpy as np

## Settings
dt = 0.1
largeur = 800
hauteur = 500
walls = [[0,250],[0,500],[800,500],[800,0],[250,0],[250,250]]

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

        for nWalls in range(len(walls)):
            self._garden.create_line(walls[nWalls-1],walls[nWalls],width=10)

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
    
    def getDimensions(self):
        return [largeur,hauteur]
        
    def show(self):
        if not self._stopped:
            self.moveMower(dt)
            self.after(1,self.show)

    def moveMower(self,dt):
        self._walls = walls
        self._nbWalls = len(self._walls)
        distRebond = -1
        for i in range(self._nbWalls):
            #Coordinates of a wall
            [x1Wall,y1Wall] = self._walls[i-1]
            [x2Wall,y2Wall] = self._walls[i]

            #Fictive mower path (if there is no wall)
            [x1,y1] = [self._mower._x,self._mower._y]
            [x2,y2] = [self._mower._x + self._mower._vx*dt,self._mower._y + self._mower._vy*dt]

            x0 = ((y1Wall*x2Wall-x1Wall*y2Wall)*(x2-x1)-(x2Wall-x1Wall)*(x2*y1-x1*y2))/((y2-y1)*(x2Wall-x1Wall)-(y2Wall-y1Wall)*(x2-x1))
            y0 = ((y1Wall*x2Wall-x1Wall*y2Wall)*(y2-y1)-(y2Wall-y1Wall)*(x2*y1-x1*y2))/((y2-y1)*(x2Wall-x1Wall)-(y2Wall-y1Wall)*(x2-x1))
            if (y2-y1)*(x2Wall-x1Wall)-(y2Wall-y1Wall)*(x2-x1) != 0:
                if x1Wall != x2Wall:
                    if x0 > min(x1,x2) and x0 <= max(x1,x2) and x0 > min(x1Wall,x2Wall) and x0 <= max(x1Wall,x2Wall):
                        distRebondTmp = (x0-x1)**2+(y0-y1)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = x1Wall
                            my1R = y1Wall
                            mx2R = x2Wall
                            my2R = y2Wall
                else:
                    if y0 > min(y1,y2) and y0 < max(y1,y2) and y0 > min(y1Wall,y2Wall) and y0 < max(y1Wall,y2Wall):
                        distRebondTmp = (x0-x1)**2+(y0-y1)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = x1Wall
                            my1R = y1Wall
                            mx2R = x2Wall
                            my2R = y2Wall
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
    
            
## Calls
fenetre = FenPrincipale()
fenetre.mainloop()
