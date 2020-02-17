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
        self._tortue = Mower(self)
        self._stopped = True
    
    def getDimensions(self):
        return [largeur,hauteur]
        
    def show(self):
        if not self._stopped:
            self._tortue.moving(dt,self)
            self.after(1,self.show)

class Mower():
    def __init__(self,can):
        [dimX,dimY] = can.getDimensions()
        self._size = min(dimX,dimY)/50
        self._x = 260
        self._y = 10
        self._v = (dimX**2+dimY**2)/18000
        self._vx = self._v*np.sqrt(3)/2
        self._vy = self._v/2
        self._dimX = dimX
        self._dimY = dimY
        self._tortue = can.create_oval(self._x - self._size, self._y - self._size, self._x + self._size, self._y + self._size, outline='grey',width=4,fill='red')
        self._murs = walls
        self._nbMurs = len(self._murs)
    
    def moving(self,dt,can):
        distRebond = -1
        for i in range(self._nbMurs):
            [mx1,my1] = self._murs[i-1]
            [mx2,my2] = self._murs[i]
            [x1,y1] = [self._x,self._y]
            [x2,y2] = [self._x + self._vx*dt,self._y + self._vy*dt]
            x0 = ((my1*mx2-mx1*my2)*(x2-x1)-(mx2-mx1)*(x2*y1-x1*y2))/((y2-y1)*(mx2-mx1)-(my2-my1)*(x2-x1))
            y0 = ((my1*mx2-mx1*my2)*(y2-y1)-(my2-my1)*(x2*y1-x1*y2))/((y2-y1)*(mx2-mx1)-(my2-my1)*(x2-x1))
            if (y2-y1)*(mx2-mx1)-(my2-my1)*(x2-x1) != 0:
                if mx1 != mx2:
                    if x0 > min(x1,x2) and x0 <= max(x1,x2) and x0 > min(mx1,mx2) and x0 <= max(mx1,mx2):
                        distRebondTmp = (x0-x1)**2+(y0-y1)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = mx1
                            my1R = my1
                            mx2R = mx2
                            my2R = my2
                else:
                    if y0 > min(y1,y2) and y0 < max(y1,y2) and y0 > min(my1,my2) and y0 < max(my1,my2):
                        distRebondTmp = (x0-x1)**2+(y0-y1)**2
                        if distRebond < 0 or distRebondTmp < distRebond:
                            distRebond = distRebondTmp
                            dx = 0
                            dy = 0
                            xR = x0
                            yR = y0
                            mx1R = mx1
                            my1R = my1
                            mx2R = mx2
                            my2R = my2
        if distRebond == -1:
            dx = self._vx*dt
            dy = self._vy*dt
            can.create_line(self._x,self._y,self._x + dx,self._y + dy,width=10)
            self._x += dx
            self._y += dy
            can.move(self._tortue,dx,dy)
        else:
            vectIntX = my2R - my1R
            vectIntY = -(mx2R - mx1R)
            if self._vx*vectIntX + self._vy*vectIntY > 0:
                vectIntX = -vectIntX
                vectIntY = -vectIntY
            angle = np.pi*random()
            newVx = self._v*np.cos(angle)
            newVy = self._v*np.sin(angle)
            if newVx*vectIntX + newVy*vectIntY < 0:
                newVx = -newVx
                newVy = -newVy
            self._vx = newVx
            self._vy = newVy
            
## Calls
fenetre = FenPrincipale()
fenetre.mainloop()
