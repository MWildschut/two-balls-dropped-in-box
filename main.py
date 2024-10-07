import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2):
    r1 = 0.5
    r2 = 0.5
    g = 9.81
    Dt = 0.01
    t = 0
    Wall1 = 0
    Wall2 = 10
    Floor = 0
    x1pos =[]
    y1pos =[]
    x2pos =[]
    y2pos =[]
    


    while t <= 10:
        t = t+Dt
        vy1 = vy1 - g*Dt
        vy2 = vy2 - g*Dt
        x1 = x1 + vx1
        x2 = x2 + vx2
        y1 = y1 + vy1
        y2 = y2 + vy2
        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2)
    
        if x1 - r1 <= Wall1:
            vx1 = -vx1
            x1 = Wall1 + r1

        if x1 + r1 >= Wall2:
            vx1 = -vx1
            x1 = Wall2 - r1

        if x2 - r2 <= Wall1:
            vx2 = -vx2
            x2 = Wall1 + r2

        if x2 + r2 >= Wall2:
            vx2 = -vx2
            x2 = Wall2 - r2

        if y1 - r1 < Floor:
            vy1 = -vy1
            y1 = Floor + r1
    
        if y2 - r2 <= Floor:
            vy2 = -vy2
            y2 = Floor + r2

        if distance <= r1+r2:
            vx1, vy1, vx2, vy2 = BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2)
            
        



        x1pos.append(x1)
        y1pos.append(y1)
        x2pos.append(x2)
        y2pos.append(y2)

    Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2)

def BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2):
    if x1 == x2:
        Phi = 90
    else:
        Phi = np.arctan((y2-y1)/(x2-x1))
    v1 = np.sqrt(vx1**2 + vy1**2)
    v2 = np.sqrt(vx2**2 + vy2**2)
    Theta1 = np.arctan(vy1/vx1)
    Theta2 = np.arctan(vy2/vx2)
    vx1 = v2 * np.cos(Theta2 - Phi)*np.cos(Phi) + v1 * np.sin(Theta1 - Phi) * np.cos(Phi + np.pi/2)
    vy1 = v2 * np.cos(Theta2 - Phi)*np.sin(Phi) + v1 * np.sin(Theta1 - Phi) * np.sin(Phi + np.pi/2)
    vx2 = v1 * np.cos(Theta2 - Phi)*np.cos(Phi) + v2 * np.sin(Theta1 - Phi) * np.cos(Phi + np.pi/2)
    vy1 = v1 * np.cos(Theta2 - Phi)*np.sin(Phi) + v2 * np.sin(Theta1 - Phi) * np.sin(Phi + np.pi/2)
    return vx1, vy1, vx2, vy2 

def Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2):
    fig, ax = plt.subplots()
    ax.axis([0,10,0,10])
    ax.set_aspect("equal")
    point1, = ax.plot(0,1, marker="o", markersize = 50*r1)
    point2, = ax.plot(0,1, marker="o", markersize = 50*r2)

    def update(t):
        point1.set_data([x1pos[t]],[y1pos[t]])
        point2.set_data([x2pos[t]],[y2pos[t]])
        return point1, point2,
         
    ani = animation.FuncAnimation(fig, update, interval=Dt*1000,frames=len(x1pos), repeat = False)
    plt.show()

DropTwoBalls(1,10,1,0,8,7,-1,0)