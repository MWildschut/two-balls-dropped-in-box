import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def CheckCollisions(x, v, r, wall1, wall2):
    #if the ball touches a boundary it turns the ball around and places it within the box so it doesn't phase through the wall
    if x - r <= wall1:  
        v = -v          
        x = wall1 + r   
    if x + r >= wall2:
        v = -v
        x = wall2 - r
    return x, v         #the new values of the coordinate and the velocity in that direction are returned

    
def BallCollision(v1,v2,m1,m2):
    #new velocities are calculated using the law of conservation of moments
    v2n = (2*m1*v1 + m2*v2-m1*v2)/(m1+m2) 
    v1n = (m1*v1 + m2*v2 - m2*v2n)/m1
    return v1n, v2n #returns the new velocities

def Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling, distance):
    #calculate contact angle between ball 1 and ball 2.
    if x1 == x2 and y1 < y2: 
        Phi = np.pi/2       #if ball 2 is directly above ball 1 the contact angle is pi/2
    elif x1 == x2 and y1 > y2:
        Phi = -np.pi/2      #if ball 2 is directly below ball 1 the contact angle is -pi/2
    else:
        Phi = np.arctan((y2-y1)/(x2-x1))    

    if x2 < x1:
        Phi += np.pi        #arctan only gives angles between pi/2 and -pi/2, so if ball 2 is left of ball 1 the angle should be flipped, so pi is added to it  
    
    #move the balls in the correct direction proportional to the distance between the balls
    x1 += np.cos(Phi)*0.5*distance
    y1 += np.sin(Phi)*0.5*distance
    x2 -= np.cos(Phi)*0.5*distance
    y2 -= np.sin(Phi)*0.5*distance 

    #moving the balls in case one of the balls gets pushed outside of a boundary. In this case the other ball moves the entire distance
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
    #Create the plot
    fig, ax = plt.subplots()
    ax.axis([LeftWall,RightWall,Floor,Ceiling]) 
    ax.set_aspect("equal")      
    plt.xlabel("x(m)")
    plt.ylabel("y(m)")
    #Gets the scale of the axes to represent the size of the ball accurately
    M = ax.transData.get_matrix()
    xscale = M[0,0]
    #Creates the point on the plot for the balls
    point1, = ax.plot(0,1, marker="o", markersize = r1*xscale, label = "ball 1")   
    point2, = ax.plot(0,1, marker="o", markersize = r2*xscale, label = "ball 2")    
    plt.legend(loc = "upper right", markerscale = 0.01*xscale)  #the legend is made

    interval = 60 #time interval between 2 frames, if every frame gets plotted the framerate is too high for my computer to generate in real time
    delay = interval/(Dt*1000) #the amount of steps that need to be skipped for the animation to run in real time
    def update(frame): #function to update the dot every frame, this funcion is called in the animate function
        n = int(frame * delay) #which value for the positions of the balls needs to be used
        point1.set_data([x1pos[n]],[y1pos[n]])  #set the location of ball 1 to a certain frame
        point2.set_data([x2pos[n]],[y2pos[n]])  #set the location of ball 2 to a certain frame
        return point1, point2
         
    ani = animation.FuncAnimation(fig, update, interval = interval, frames=int(len(x1pos)/delay), repeat = False) #animates the ball using the update function
    plt.show()


def DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1 = 0.5, r2 = 0.5, LeftWall = 0, RightWall = 10, Floor = 0, Ceiling = 10, m1 = 1, m2 = 1, animate = True):
    #set standard initial values
    g = -9.81           
    Dt = 0.01           
    t = 0              
    tmax = 20          

    #Empty arrays for the x and y coordinates of both balls 
    x1pos =[]
    y1pos =[]
    x2pos =[]
    y2pos =[]

    datatypes = [type(x1),type(y1),type(vx1),type(vy1),type(x2),type(y2),type(vx2),type(vy2), type(r1), type(r2), type(LeftWall),type(RightWall),type(Floor),type(Ceiling),type(m1),type(m2)]
    for i in range(len(datatypes)):
        if datatypes[i] != int and datatypes[i] != float:
            print("Error: Input values should be integers or floats.")
            return None
    if RightWall < LeftWall or Ceiling < Floor:
        #Checks if the boundaries have appropriate values
        print("Error: RightWall has to be smaller than LeftWall and Floor has to be smaller than Ceiling")
        return None
    if x1 - r1 < LeftWall or x2 - r2 < LeftWall or x1 + r1 > RightWall or x2 + r2 > RightWall or y1 - r1 < Floor or y2 - r2 < Floor or y1 + r1 > Ceiling or y2 + r2 > Ceiling:
        #Checks if both of the balls are within the box
        print("Error: one of the balls is outside of the box")
        return None
    if r1 <= 0 or r2 <= 0 or m1 <= 0 or m2 <=0:
        print("Error: the radius and mass of a ball cannot be 0 or smaller than 0")
        return None

    while t <= tmax:            #repeats untill t = tmax
        t += Dt                 #time step
        #movement and acceleration of the balls
        vy1 += g*Dt             
        vy2 += g*Dt
        x1 += vx1*Dt       
        x2 += vx2*Dt
        y1 += vy1*Dt
        y2 += vy2*Dt
            
        x1,vx1 = CheckCollisions(x1,vx1,r1,LeftWall,RightWall)  #checks if ball 1 hits a wall
        x2,vx2 = CheckCollisions(x2,vx2,r2,LeftWall,RightWall)  #checks if ball 2 hits a wall
        y1,vy1 = CheckCollisions(y1,vy1,r1,Floor,Ceiling)       #checks if ball 1 hits a floor or ceiling
        y2,vy2 = CheckCollisions(y2,vy2,r2,Floor,Ceiling)       #checks if ball 2 hits a floor or ceiling

        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 #distance between the 2 balls
        if distance <= 0: #if the balls hit eachother the function BallCollision is applied
            x1, y1, x2, y2 = Separate(x1,y1,x2,y2,r1,r2,LeftWall,RightWall,Floor,Ceiling, distance) #separates the balls so they don't get stuck together
            vx1, vx2 = BallCollision(vx1,vx2,m1,m2) #calculates collision in the x direction
            vy1, vy2 = BallCollision(vy1,vy2,m1,m2) #calculates collision in the y direction


        #the coordinates of the balls after the calculations are put into the arrays   
        x1pos.append(x1)
        y1pos.append(y1)
        x2pos.append(x2)
        y2pos.append(y2)

    if animate == False:
        return "Done"
    else:
        Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2,LeftWall,RightWall,Floor,Ceiling) #The function to animate the balls is called
    return

