import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.animation as an


r = 0.1
m = 1
y0 = 3
vx0 = 0
vy0 = 0

#def DropInWater(r,m,y0,vx0,vy0):
y = y0
x = 1
vx = vx0
vy = vy0
Dt = 0.01
t = 0
Tmax = 1
g = 9.81
Fg = g * m #gravitational force 
V = 4/3*np.pi*r**3
A = np.pi*r**2
Fb = 0
Cd = 0.47   #drag coefficent of a sphere
Pw = 998    #density of water
Pa = 1.225  #average density of air
ypos = []
xpos = []
T = []
v = np.sqrt(vy0**2 + vx0**2) 

while t < Tmax:
    if y-r >= 0:     #if the ball is in the air
        Fd = 1/2 * Pa * vy**2 * Cd * A  #drag of the ball in the air
        Fb = Pa * V *g #bouyancy of the ball in air (because why not)
        
    elif y+r <= 0:   #if the ball is fully under water
        Fd = 1/2 * Pw * vy**2 * Cd * A    #drag of the ball in the water
        Fb = Pw * V *g     #bouyancy of the ball in water
        
    else:   #if the ball is partially under water
        h = r - y   #height of the ball that is under water
        Vw = ((np.pi*h**2)/3)*(3*r - h)     #volume of the ball that is under water, so the volume of displaced water
        Fb = Pw * Vw *g     #bouyancy of the ball in water

        if vy < 0: #ball is going downward
            if y <= 0:
                Fd = 1/2 * Pw * vy**2 * Cd * A
            else:
                a = np.sqrt(r**2-y**2)
                Aw = np.pi * a**2
                Aa = A - Aw 
                Fdw = 1/2 * Pw * vy**2 * Cd * Aw
                Fda = 1/2 * Pa * vy**2 * Cd * Aa
                Fd = Fda + Fdw
        else: #ball is going upwards or not moving (which results in a drag of 0)
            if y >= 0:
                Fd = 1/2 * Pa * vy**2 * Cd * A
            else:
                a = np.sqrt(r**2-y**2)
                Aa = np.pi * a**2
                Aw = A - Aa 
                Fdw = 1/2 * Pw * vy**2 * Cd * Aw
                Fda = 1/2 * Pa * vy**2 * Cd * Aa
                Fd = Fda + Fdw

    if vy > 0:
        Fb = -Fd    #if the velocity is positive and the ball is moving upwards the drag is downwards, so negative
    Fy = Fb + Fd - Fg
    ay = Fy/m
    vy = vy + ay*Dt                                         #calculation of velocity in the y direction
    y = y + vy                                              #calculation of position in the y direction
    ypos = np.append(ypos, y)                                      #the value of y is added to the array
    T = np.append(T,t)
    v = np.sqrt(vy**2 + vx**2)
    t = t + Dt
print(ypos)



