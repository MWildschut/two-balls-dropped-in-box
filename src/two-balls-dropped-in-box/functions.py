import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def CheckInputs(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1,r2,m1,m2,BoxWidth,BoxHeight,tmax):
    """
    A function to check if the inputs of the DropTwoBalls function ar valid

    Parameters --- see Help(main.DropTwoBalls)
    """
    variables = [x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1,r2,m1,m2,BoxWidth,BoxHeight,tmax]
    
    for i in range(len(variables)):
        if type(variables[i]) != int and type(variables[i]) != float:
            print("Error: Input values should be integers or floats.")
            return "Error"
    if BoxWidth < 0 or BoxHeight < 0:
        #Checks if the boundaries have appropriate values
        print("Error: BoxWidth and BoxHeight need to be positive")
        return "Error"
    if x1 - r1 < 0 or x2 - r2 < 0 or x1 + r1 > BoxWidth or x2 + r2 > BoxWidth or y1 - r1 < 0 or y2 - r2 < 0 or y1 + r1 > BoxHeight or y2 + r2 > BoxHeight:
        #Checks if both of the balls are within the box
        print("Error: one of the balls is outside of the box")
        return "Error"
    if r1 <= 0 or r2 <= 0 or m1 <= 0 or m2 <=0:
        print("Error: the radius and mass of a ball cannot be 0 or smaller than 0")
        return "Error"
    if np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 < 0:
        print("Error: the balls cannot overlap")
        return "Error"
    if tmax <= 0:
        print("Error: the total runtime cannot be zero or negative")
        return "Error"

def Movement(x,y,vx,vy,Dt, g = -9.81):
    """
    A function to simulate the movement of a ball. It will return the new position and velocity of the ball.
    
    Parameters:
        x(float): The x coordinate of the ball
        y(float): The y coordinate of the ball
        vx(float): The velocity of the ball in the x direction
        vy(float): The velocity of the ball in the y direction
        Dt(float): The timestep between two calculations
    """
    #Movement for each ball
    vy += g*Dt             
    x += vx*Dt       
    y += vy*Dt
    return x, y, vy
    
def CollisionWall(x, v, r, size):
    """
    A function to calculate if the ball hits a wall in either the x or y direction and make it bounce accordingly

    Parameters:
        x(float): The coordinate of the ball on the chosen axis
        v(float): The velocity of the ball on the chosen axis
        r(float): The radius of the ball
        size(float): The size of the box in direction of the chosen axis
    """
    #if the ball touches a boundary it turns the ball around and places it within the box so it doesn't phase through the wall
    if x - r <= 0: 
        v = abs(v) 
        x = r   
    if x + r >= size:
        v = -1* abs(v)   #velocity turns negative
        x = size - r
    return x, v         #the new values of the coordinate and the velocity in that direction are returned
 
def BallCollision(v1,v2,m1,m2):
    """
    A function to calculate the new velocities of the balls in either the x or y direction using the law of conservation of moments

    Parameters:
        v1(float): The velocity of the first ball on the chosen axis
        v2(float): The velocity of the secont ball on the chosen axis
        m1(float): The mass of the first ball
        m2(float): The mass of the second ball
    """
    #new velocities are calculated using the law of conservation of moments
    v2n = (2*m1*v1 + m2*v2-m1*v2)/(m1+m2) 
    v1n = (m1*v1 + m2*v2 - m2*v2n)/m1
    return v1n, v2n #returns the new velocities

def Separate(x1,y1,x2,y2,r1,r2,BoxWidth,BoxHeight, distance):
    """
    A function to seperate balls when they collide so they don't get stuck together

    Parameters:
        x1(float): x coordinate of the center of ball 1
        y1(float): y coordinate of the center of ball 1
        x2(float): x coordinate of the center of ball 2
        y2(float): y coordinate of the center of ball 2
        r1(float): radius of ball 1
        r2(float): radius of ball 2
        BoxWidth(float): Hidth of the box
        BoxHeigth(float): Height of the box
        distance(float): The distance between the edges of the balls.
    """
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

    #moving the balls in case one of the balls gets pushed outside of a boundary. In this case the ball moves back to where it started and the other ball moves the entire distance.
    if x1 + r1 > BoxWidth or x1 - r1 < 0: #ball 1 phases into a wall
        x2 -= np.cos(Phi)*0.5*distance 
        x1 -= np.cos(Phi)*0.5*distance 
    if x2 + r2 > BoxWidth or x2 - r2 < 0: #ball 2 phases into a wall
        x1 += np.cos(Phi)*0.5*distance 
        x2 += np.cos(Phi)*0.5*distance
    if y1 + r1 > BoxHeight or y1 - r1 < 0: #ball 1 phases into the floor or ceiling
        y2 -= np.cos(Phi)*0.5*distance
        y1 -= np.sin(Phi)*0.5*distance
    if y2 + r2 > BoxHeight or y2 - r2 < 0: #ball 2 phases into the floor or ceiling
        y1 += np.cos(Phi)*0.5*distance
        y2 += np.sin(Phi)*0.5*distance
    return x1, y1, x2, y2

def Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2, BoxWidth, BoxHeight):
    """
    This function generates the animation after all the calculations are done
    
    Parameters:
        x1pos(array): An array of all the x positions of ball 1
        y1pos(array): An array of all the y positions of ball 1
        x2pos(array): An array of all the x positions of ball 2
        y2pos(array): An array of all the y positions of ball 2
        Dt(float): The timestep between 2 calculations
        BoxWidth(float): The width of the box
        BoxHeight(float): The height of the box
    """
    #check inputs
    if len(x1pos) != len(y1pos) or len(x2pos) != len(y2pos):
        return "Error"
    if len(x1pos) == 0 or len(y1pos) == 0 or len(x2pos) == 0 or len(y2pos) == 0:
        return "Error"
    
    #Create the plot
    fig, ax = plt.subplots()
    ax.axis([0,BoxWidth,0,BoxHeight]) 
    ax.set_aspect("equal")      
    plt.xlabel("x(m)")
    plt.ylabel("y(m)")

    #Gets the scale of the axes to represent the size of the ball accurately
    M = ax.transData.get_matrix()
    xscale = M[0,0]

    #Creates the point on the plot for the balls
    point1, = ax.plot(x1pos[0],y1pos[0], marker="o", markersize = r1*xscale, label = "ball 1")   
    point2, = ax.plot(x2pos[0],y2pos[0], marker="o", markersize = r2*xscale, label = "ball 2")    
    plt.legend(loc = "upper right", markerscale = 0)  #the legend is made
    

    interval = 60 #time interval between 2 frames, if every frame gets plotted the framerate is too high for my computer to generate in real time
    delay = interval/(Dt*1000) #the amount of steps that need to be skipped for the animation to run in real time
    def update(frame): 
        """function to update the dot every frame, this funcion is called in the animate function"""
        n = int(frame * delay) #which value for the positions of the balls needs to be used
        point1.set_data([x1pos[n]],[y1pos[n]])  #set the location of ball 1 to a certain frame
        point2.set_data([x2pos[n]],[y2pos[n]])  #set the location of ball 2 to a certain frame
        return point1, point2
         
    ani = animation.FuncAnimation(fig, update, interval = interval, frames=int(len(x1pos)/delay), repeat = False) #animates the ball using the update function
    plt.show()