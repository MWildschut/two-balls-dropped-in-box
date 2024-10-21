import main as m


def test_inputs():
    result = m.CheckInputs(x1=1,y1=8,vx1=0,vy1=0,x2=5,y2=8,vx2=0,vy2=0,r1=0.5,r2=0.5,m1=1,m2=1,LeftWall=10,RightWall=0,Floor=0,Ceiling=10) #Walls LeftWall is right of RightWall
    assert result == "Error"
    result = m.CheckInputs(x1 =1,y1=20,vx1=0,vy1=0,x2=5,y2=8,vx2=0,vy2=0,r1=0.5,r2=0.5,m1=1,m2=1,LeftWall=0,RightWall=10,Floor=0,Ceiling=10) #one of the balls is outside of the box
    assert result == "Error"
    result = m.CheckInputs(x1 ="hey",y1=8,vx1=0,vy1=0,x2=5,y2=8,vx2=0,vy2=0,r1=0.5,r2=0.5,m1=1,m2=1,LeftWall=0,RightWall=10,Floor=0,Ceiling=10) #one of the inputs is a string
    assert result == "Error"
    result = m.CheckInputs(x1 =1,y1=8,vx1=0,vy1=0,x2=5,y2=8,vx2=0,vy2=0,r1=-0.5,r2=0.5,m1=1,m2=1,LeftWall=0,RightWall=10,Floor=0,Ceiling=10) #one of the radii is negative
    assert result == "Error"
    result = m.CheckInputs(x1 =1,y1=8,vx1=0,vy1=0,x2=5,y2=8,vx2=0,vy2=0,r1=0.5,r2=0.5,m1=-1,m2=1,LeftWall=0,RightWall=10,Floor=0,Ceiling=10) #one of the masses is negative
    assert result == "Error"
    result = m.CheckInputs(x1 =1,y1=8,vx1=0,vy1=0,x2=1,y2=8,vx2=0,vy2=0,r1=0.5,r2=0.5,m1=1,m2=1,LeftWall=0,RightWall=10,Floor=0,Ceiling=10) #balls are in the same spot

def test_movement():
    x, y, vy = m.Movement(x=1,y=8,vx=1,vy=0,Dt=0.1,g=-10) #check if movement is working correctly
    assert x == 1.1 and vy == -1 and y == 7.9

def test_wallcollision():
    x, v = m.CheckCollisions(x=1, v=1, r= 0.5, wall1=0, wall2=10) #check if nothing happens if there is no collision
    assert x == 1 and v == 1
    x, v = m.CheckCollisions(x=0,v=-1,r=1, wall1=0, wall2=10) #check if collision happens correctly if there is collision
    assert x == 1 and v == 1

def test_ballcollision():
    v1n, v2n = m.BallCollision(v1=1, v2=2, m1=1, m2=1)
    assert v1n == 2 and v2n == 1

def test_separation():
    res_x1, res_y1, res_x2, res_y2 = m.BallCollision(x1= 1,7,2,7,r1=1,r2=1,LeftWall=0,RightWall0=10,Floor=0,Ceiling=10, distance=)