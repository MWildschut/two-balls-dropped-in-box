import functions as f
import numpy as np

def DropTwoBalls(x1,y1,x2,y2,vx1 = 0.0,vy1 =0.0,vx2 =0.0,vy2 =0.0,r1 = 0.5, r2 = 0.5, m1 = 1.0, m2 = 1.0, BoxWidth = 10.0, BoxHeight = 10.0,  tmax = 10.0):
    """
    This function generates an animation of two balls dropped in a box. 
    
    Parameters:
        x1(float): The horizontal coordinate of the center of the first ball in meters
        y1(float): The vertical coordinate of the center of the first ball in meters
        x2(float): The horizontal coordinate of the center of the second ball in meters
        y2(float): The vertical coordinate of the center of the second ball in meters
        vx1(float): The initial speed of the first ball in the horizontal direction in m/s (standard 0.0)
        vy1(float): The initial speed of the first ball in the vertical direction in m/s (standard 0.0)
        vx2(float): The initial speed of the second ball in the horizontal direction in m/s (standard 0.0)
        vy2(float): The initial speed of the second ball in the vertical direction in m/s (standard 0.0)
        r1(float): The radius of the first ball in meters (standard 0.5)
        r2(float): The radius of the second ball in meters (standard 0.5)
        m1(float): The mass of the first ball in kg (standard 1.0)
        m2(float): The mass of the second ball in kg (standard 1.0)
        BoxWidth(float): The size of the box in the horizontal direction in meters (standard 10.0)
        BoxHeight(float): The size of the box in the vertical direction in meters (standard 10.0)
        tmax(float): The total runtime of the simulation in seconds (standard 10.0)

    Example: 
    DropTwoBalls(2.0, 3.0, 4.0, 5.0, vx1 = 4.5, vx2 = 3.0, r1 = 1.0, m1 = 3.0, BoxWidth = 7.0)
    This will generate an animation of the two balls using the values given. 
    """

    if f.CheckInputs(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1,r2,m1,m2,BoxWidth,BoxHeight,tmax) == "Error": #checks if inputs are valid. In a function for readability
        return None
    
    #set initial values      
    t = 0              
    Dt = 0.01
       
    #Empty arrays for the x and y coordinates of both balls 
    x1pos =[]
    y1pos =[]
    x2pos =[]
    y2pos =[]

    while t <= tmax:            #repeats untill t = tmax
        t += Dt                 #time step
        #movement and acceleration of the balls
        x1,y1,vy1 = f.Movement(x1,y1,vx1,vy1,Dt)
        x2,y2,vy2 = f.Movement(x2,y2,vx2,vy2,Dt)

        x1,vx1 = f.CollisionWall(x1,vx1,r1,BoxWidth)  #checks if ball 1 hits a wall
        x2,vx2 = f.CollisionWall(x2,vx2,r2,BoxWidth)  #checks if ball 2 hits a wall
        y1,vy1 = f.CollisionWall(y1,vy1,r1,BoxHeight)       #checks if ball 1 hits a floor or ceiling
        y2,vy2 = f.CollisionWall(y2,vy2,r2,BoxHeight)       #checks if ball 2 hits a floor or ceiling

        distance = np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 #distance between the 2 balls
        if distance <= 0: #if the balls hit eachother the function BallCollision is applied
            x1, y1, x2, y2 = f.Separate(x1,y1,x2,y2,r1,r2,BoxWidth,BoxHeight, distance) #separates the balls so they don't get stuck together
            vx1, vx2 = f.BallCollision(vx1,vx2,m1,m2) #calculates collision in the x direction
            vy1, vy2 = f.BallCollision(vy1,vy2,m1,m2) #calculates collision in the y direction

        #the coordinates of the balls after the calculations are put into the arrays   
        x1pos.append(x1)
        y1pos.append(y1)
        x2pos.append(x2)
        y2pos.append(y2)

    f.Animate(x1pos,y1pos,x2pos,y2pos,Dt,r1,r2,BoxWidth,BoxHeight) #The function to animate the balls is called
    return

def DropTwoBallsRandom():
    """
    This function generates random values for the two balls and runs DropTwoBalls using those random values.
    """
    r1 = np.random.uniform(0.25,1.5)
    r2 = np.random.uniform(0.25,1.5)
    x1 = np.random.uniform(r1, 10-r1)
    y1 = np.random.uniform(r1, 10-r1)
    x2 = np.random.uniform(r2, 10-r2)
    y2 = np.random.uniform(r2, 10-r2)
    while np.sqrt((x1-x2)**2 + (y1 - y2)**2) - r1 - r2 < 0:
        x2 = np.random.uniform(r2, 10-r2)
        y2 = np.random.uniform(r2, 10-r2)
    vx1 = np.random.uniform(0.0,5.0)
    vy1 = np.random.uniform(0.0,5.0)
    vx2 = np.random.uniform(0.0,5.0)
    vy2 = np.random.uniform(0.0,5.0)
    m1 = 4/3 * np.pi * r1**2
    m2 = 4/3 * np.pi * r2**2

    DropTwoBalls(x1,y1,x2,y2,vx1,vy1,vx2,vy2,r1,r2,m1,m2)