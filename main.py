import numpy as np

def DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2):
    r1 = 0.5
    r2 = 0.5
    g = 9.81
    Dt = 0.1
    t = np.arrange(0,10,Dt)
    Wall1 = 0
    Wall2 = 10
    Floor = 0


    for i in range(t):
        vy1 = vy1 - g*Dt
        vy2 = vy2 - g*Dt
        x1 = x1 + vx1
        x2 = x2 + vx2
        y1 = y1 + vy1
        y2 = y2 + vy2
        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2)
    
        if x1 - r1 <= Wall1 or x1 + r1 <= Wall2:
        vx1 = -vx1
    
        if x2 - r2 <= Wall1 or x2 + r2 <= Wall2:
        vx2 = -vx2

        if y1 - r1 <= Floor:
        vy1 = -vy1
    
        if y2 - r2 <= Floor:
        vy2 = -vy2
  
        if distance <= r1+r2:
            vx1, vy1, vx2, vy2 = BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2)
    

def BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2):
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

