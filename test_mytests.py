import main as m

def test_inputs():
    #By testing if the CheckInputs function is working correctly, I also test if DropTwoBalls responds correctly to invalid inputs. 

    #potential values for each type of variable, where the first one is a valid value. For velocity every potential value is valid
    x1 = [1,-1, 20, "string"] #valid value, outside of bounds, or not integer or float
    x2 = [4, 1] #valid value, or overlaps with x1
    r1 = [0.5, -0.5, 0, 20] #valid value, negative, zero, or too large
    m1 = [1, -1,0] #valid value, negative or zero
    BoxWidth = [10, -10] #valid value, or lower than left wall
    tmax = [20, -3, 0] #valid value, negative or zero
    FirstIteration = True #variable to check if the first iteration has been done
    #iterate through all options for each variable to check if it gives an error
    for i in range(len(x1)):
        for j in range(len(x2)):
            for k in range(len(r1)):
                for l in range(len(m1)):
                    for n in range(len(BoxWidth)):
                        for o in range(len(tmax)):
                            result = m.CheckInputs(x1[i],3,0,0,x2[j],3,0,0,r1[k],0.5,m1[l],1,BoxWidth[n],10,tmax[o]) #check the output for the values each iteration
                            if FirstIteration== True:
                                FirstIteration = False #After this it is no longer the first iteration
                                assert result == None #if the first value for everything gets taken there should not be an error
                            else:
                                assert result == "Error" #For all other iterations it should give an error, as it always uses at least 1 invalid value. 
                                        
  
def test_movement():
    x, y, vy = m.Movement(x=1,y=8,vx=1,vy=0,Dt=0.1, g = -10) #check if movement is working correctly
    assert x == 1.1 and vy == -1 and y == 7.9

def test_wallcollision():
    x, v = m.CollisionWall(x=1, v=1, r= 0.5, size=10) #check if nothing happens if there is no collision
    assert x == 1 and v == 1
    x, v = m.CollisionWall(x=0,v=-1,r=1, size=10) #check if collision happens correctly if there is collision
    assert x == 1 and v == 1

def test_ballcollision():
    v1n, v2n = m.BallCollision(v1=1, v2=2, m1=1, m2=1) #test if collision between two balls happens correctly
    assert v1n == 2 and v2n == 1

def test_separation():
    x1, y1, x2, y2 = m.Separate(x1=5,y1=7,x2=6,y2=7,r1=1,r2=1,BoxWidth=10,BoxHeight=10, distance=-1) #test if the separation of 2 balls happens correctly
    assert x1 == 4.5 and y1 == 7 and x2 == 6.5 and y2 == 7
    x1, y1, x2, y2 = m.Separate(x1=8,y1=7,x2=9,y2=7,r1=1,r2=1,BoxWidth=10,BoxHeight=10, distance=-1) #test if the separation of 2 balls happens correctly if 1 of the balls phases into the wall
    assert x1 == 7 and y1 == 7 and x2 == 9 and y2 == 7

def test_animate():
    result = m.Animate([],[],[],[],0.1,0.5,0.5,10,10) #check if the function gives an error if empty arrays are given
    assert result == "Error"
    result = m.Animate([3,4],[1,2],[1,2],[4,3,2],0.1,0.5,0.5,10,10) #Check if the function gives an error if the length of the array for the x coordinate of a ball is different from the length of the array of the y coordinate.
    assert result == "Error"