import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1 = 0.5, r2 = 0.5, LeftWall = 0, RightWall = 10, Floor = 0, Ceiling = 10, m1 = 1, m2 = 1):
    g = -9.81        #gravitational acceleration
    Dt = 0.01       #time step
    t = 0           #starttime of the simulation
    tmax = 10       #total run time of the simulation

    #Empty arrays for the x and y coordinates of both balls 
    x1pos =[]
    y1pos =[]
    x2pos =[]
    y2pos =[]
    
    if x1 - r1 < LeftWall or x2 - r2 < LeftWall or x1 + r1 > RightWall or x2 + r2 > RightWall or y1 - r1 < Floor or y2 - r2 < Floor or y1 + r1 > Ceiling or y2 + r2 > Ceiling:
        #Checks if both of the balls are within the box
        print("Error: one of the balls is outside of the box")
        return

    while t <= tmax:         #repeats untill t = tmax
        t += Dt            #time step
        vy1 += g*Dt    #gravity applied
        vy2 += g*Dt
        x1 += vx1*Dt       #movement of the balls
        x2 += vx2*Dt
        y1 += vy1*Dt
        y2 += vy2*Dt
            
        x1,vx1 = CheckCollisions(x1,vx1,r1,LeftWall,RightWall)  #checks if ball 1 hits a wall
        x2,vx2 = CheckCollisions(x2,vx2,r2,LeftWall,RightWall)  #checks if ball 2 hits a wall
        y1,vy1 = CheckCollisions(y1,vy1,r1,Floor,Ceiling)       #checks if ball 1 hits a floor or ceiling
        y2,vy2 = CheckCollisions(y2,vy2,r2,Floor,Ceiling)       #checks if ball 2 hits a floor or ceiling

        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 #distance between the 2 balls
        if distance <= 0: #if the balls hit eachother the function BallCollision is applied
            x1, y1, x2, y2 = Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling,distance)
            vx1, vx2 = BallCollision(vx1,vx2,m1,m2)
            vy1, vy2 = BallCollision(vy1,vy2,m1,m2)


        #the coordinates of the balls after the calculations are put into the arrays   
        x1pos.append(x1)
        y1pos.append(y1)
        x2pos.append(x2)
        y2pos.append(y2)

    Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2,LeftWall,RightWall,Floor,Ceiling) #The function to animate the balls is called

def CheckCollisions(x, v, r, wall1, wall2):
    if x - r <= wall1:  #Check if the ball hits the boundary
        v = -v          #ball gets turned around
        x = wall1 + r   #makes sure the ball is on the right side of the wall, so it doesn't get stuck
    if x + r >= wall2:
        v = -v
        x = wall2 - r
    return x, v         #the new values of the coordinate and the velocity in that direction are returned

    
def BallCollision(v1,v2,m1,m2):
    v2n = (2*m1*v1 + m2*v2-m1*v2)/(m1+m2) #wet van behoud van momenten
    v1n = (m1*v1 + m2*v2 - m2*v2n)/m1
    return v1n, v2n #returns the new velocities

def Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling, distance):
    if x1 == x2 and y1 < y2:
        Phi = np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    elif x1 == x2 and y1 >= y2:
        Phi = -np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    else:
        Phi = np.arctan((y2-y1)/(x2-x1))    #angle between middle point of the 2 balls when they collide

    if x2 < x1:
        Phi += np.pi #flip
    
    x1 += np.cos(Phi)*0.5*distance
    y1 += np.sin(Phi)*0.5*distance
    x2 -= np.cos(Phi)*0.5*distance
    y2 -= np.sin(Phi)*0.5*distance 

    if x1 + r1 > RightWall or x1 - r1 < LeftWall:
        x2 -= np.cos(Phi)*0.5*distance #x2 is moved
        x1 -= np.cos(Phi)*0.5*distance #x1 is moved back to where it didn't collide with the wall
    if x2 + r2 > RightWall or x2 - r2 < LeftWall:
        x1 += np.cos(Phi)*0.5*distance
        x2 += np.cos(Phi)*0.5*distance
    if y1 + r1 > Ceiling or y1 - r1 < Floor:
        y2 -= np.cos(Phi)*0.5*distance
        y1 -= np.sin(Phi)*0.5*distance
    if y2 + r2 > Ceiling or y2 - r2 < Floor:
        y1 += np.cos(Phi)*0.5*distance
        y2 += np.sin(Phi)*0.5*distance
    return x1, y1, x2, y2

def Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2,LeftWall, RightWall, Floor, Ceiling):
    fig, ax = plt.subplots()
    ax.axis([LeftWall,RightWall,Floor,Ceiling]) #sets axes to the walls, floor and ceiling of the box
    ax.set_aspect("equal")      #sets the axes to the same scale
    plt.xlabel("x(m)")
    plt.ylabel("y(m)")
    M = ax.transData.get_matrix()
    xscale = M[0,0]
    point1, = ax.plot(0,1, marker="o", markersize = r1*xscale, label = "ball 1")    #marker for ball 1 is made
    point2, = ax.plot(0,1, marker="o", markersize = r2*xscale, label = "ball 2")    #marker for ball 2 is made
    plt.legend(loc = "upper right", markerscale = 0.01*xscale)  #the legend is made

    interval = 50
    delay = interval/(Dt*1000)
    def update(frame): #function to update the dot every timeframe, this funcion is called in the animate function
        n = int(frame * delay)
        point1.set_data([x1pos[n]],[y1pos[n]])  #set the location of ball 1 to a certain timeframe
        point2.set_data([x2pos[n]],[y2pos[n]])  #set the location of ball 2 to a certain timeframe
        return point1, point2
         
    ani = animation.FuncAnimation(fig, update, interval = interval, frames=int(len(x1pos)/delay), repeat = False) #animates the ball using the update function
    plt.show()


DropTwoBalls(x1=2,y1=8,vx1=5,vy1=0,x2=5,y2=7,vx2=8,vy2 =0,r1 = 1,m1 = 2) 


