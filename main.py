import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1 = 0.5, r2 = 0.5, LeftWall = 0, RightWall = 10, Floor = 0, Ceiling = 10, m1 = 1, m2 = 1):
    g = 9.81        #gravitational acceleration
    Dt = 0.005       #time step
    t = 0           #starttime of the simulation
    tmax = 5       #total run time of the simulation

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
        t = t+Dt            #time step
        vy1 = vy1 - g*Dt    #gravity applied
        vy2 = vy2 - g*Dt
        x1 = x1 + vx1       #movement of the balls
        x2 = x2 + vx2
        y1 = y1 + vy1
        y2 = y2 + vy2
        
    
        x1,vx1 = CheckCollisions(x1,vx1,r1,LeftWall,RightWall)  #checks if ball 1 hits a wall
        x2,vx2 = CheckCollisions(x2,vx2,r2,LeftWall,RightWall)  #checks if ball 2 hits a wall
        y1,vy1 = CheckCollisions(y1,vy1,r1,Floor,Ceiling)       #checks if ball 1 hits a floor or ceiling
        y2,vy2 = CheckCollisions(y2,vy2,r2,Floor,Ceiling)       #checks if ball 2 hits a floor or ceiling

        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 #distance between the 2 balls
        if distance <= 0: #if the balls hit eachother the function BallCollision is applied
            x1, y1, x2, y2 = Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling,distance)
            vx1, vy1, vx2, vy2 = BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2,m1,m2)

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

    
def BallCollision(x1,x2,y1,y2,vx1,vy1,vx2,vy2,m1,m2):
    if x1 == x2 and y1 < y2:
        Phi = np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    elif x1 == x2 and y1 >= y2:
        Phi = -np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    else:
        Phi = np.arctan((y2-y1)/(x2-x1))    #angle between middle point of the 2 balls when they collide

    if x1 > x2 and y1 > y2:
        Phi += np.pi

    v1 = np.sqrt(vx1**2 + vy1**2)           #total velocity of ball 1
    v2 = np.sqrt(vx2**2 + vy2**2)           #total velocity of ball 2
    if vx1 == 0 and vy1 < 0:
        Theta1 = -np.pi/2    #if vx1 equals0 the calculation for theta doesn't work since it devides by 0. In this case phi should be 90 degrees
    elif vx1 == 0 and vy1 >= 0:
        Theta1 = np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    else:
        Theta1 = np.arctan(vy1/vx1)             #movement angle of ball 1
    if vy1 < 0 and vx1 < 0:
        Theta1 += np.pi

    if vx2 == 0 and vy2 < 0:
        Theta2 = -np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    elif vx2 == 0 and vy2 >= 0:
        Theta2 = np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    else:
        Theta2 = np.arctan(vy2/vx2)             #movement angle of ball 2
    if vy2 < 0 and vx2 < 0:
        Theta2 += np.pi
    #formulas to calculate the new velocities after collision
    vx1 = ((v1*np.cos(Theta1 - Phi)*(m1-m2) + 2*m2*v2 * np.cos(Theta2 - Phi))/(m1 + m2))*np.cos(Phi) + v1 * np.sin(Theta1 - Phi) * np.cos(Phi + np.pi/2)
    vy1 = ((v1*np.cos(Theta1 - Phi)*(m1-m2) + 2*m2*v2 * np.cos(Theta2 - Phi))/(m1 + m2))*np.sin(Phi) + v1 * np.sin(Theta1 - Phi) * np.sin(Phi + np.pi/2)
    vx2 = ((v2*np.cos(Theta2 - Phi)*(m2-m1) + 2*m1*v1 * np.cos(Theta1 - Phi))/(m1 + m2))*np.cos(Phi) + v2 * np.sin(Theta1 - Phi) * np.cos(Phi + np.pi/2)
    vy1 = ((v2*np.cos(Theta2 - Phi)*(m2-m1) + 2*m1*v1 * np.cos(Theta1 - Phi))/(m1 + m2))*np.sin(Phi) + v2 * np.sin(Theta1 - Phi) * np.sin(Phi + np.pi/2)

    return vx1, vy1, vx2, vy2 #returns the new velocities

def Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling, distance):
    if x1 == x2 and y1 < y2:
        Phi = np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    elif x1 == x2 and y1 >= y2:
        Phi = -np.pi/2    #if x1 equals x2 the calculation for phi doesn't work since it devides by 0. In this case phi should be 90 degrees
    else:
        Phi = np.arctan((y2-y1)/(x2-x1))    #angle between middle point of the 2 balls when they collide
    x1 += np.cos(Phi)*0.5*distance
    y1 += np.sin(Phi)*0.5*distance
    x2 -= np.cos(Phi)*0.5*distance
    y2 -= np.sin(Phi)*0.5*distance 

    if x1 + r1 > RightWall or x1 - r1 < LeftWall:
        x2 -= np.cos(Phi)*distance #x2 is moved
        x1 -= np.cos(Phi)*0.5*distance #x1 is moved back to where it didn't collide with the wall
    if x2 + r2 > RightWall or x2 - r2 < LeftWall:
        x1 += np.cos(Phi)*distance
        x2 += np.cos(Phi)*0.5*distance
    if y1 + r1 > Ceiling or y1 - r1 < Floor:
        y2 -= np.cos(Phi)*distance
        y1 -= np.sin(Phi)*0.5*distance
    if y2 + r2 > Ceiling or y2 - r2 < Floor:
        y1 += np.cos(Phi)*distance
        y2 += np.sin(Phi)*0.5*distance
    return x1, y1, x2, y2


def Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2,LeftWall, RightWall, Floor, Ceiling):
    fig, ax = plt.subplots()
    ax.axis([LeftWall,RightWall,Floor,Ceiling]) #sets axes to the walls, floor and ceiling of the box
    ax.set_aspect("equal")      #sets the axes to the same scale
    point1, = ax.plot(0,1, marker="o", markersize = 50*r1, label = "ball 1")    #marker for ball 1 is made
    point2, = ax.plot(0,1, marker="o", markersize = 50*r2, label = "ball 2")    #marker for ball 2 is made
    plt.legend(loc = "upper right", markerscale = 0.5)  #the legend is made

    def update(frame): #function to update the dot every timeframe, this funcion is called in the animate function
        point1.set_data([x1pos[frame]],[y1pos[frame]])  #set the location of ball 1 to a certain timeframe
        point2.set_data([x2pos[frame]],[y2pos[frame]])  #set the location of ball 2 to a certain timeframe
        return point1, point2,  #returns the new locations of the balls
         
    ani = animation.FuncAnimation(fig, update, interval=Dt*5000,frames=len(x1pos), repeat = False) #animates the ball using the update function
    plt.show()

DropTwoBalls(x1=2,y1=0.5,vx1=0.5,vy1=0,x2=8,y2=0.5,vx2=0.03,vy2 =0) 