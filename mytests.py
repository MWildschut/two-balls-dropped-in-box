import main as m


def test_inputs():
    #standard values for ease
    x1 = 1
    y1 = 8
    vx1 = 0
    vy1 = 0
    x2 = 5
    y2 = 8
    vx2 = 0
    vy2 = 0

    result = m.DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2, LeftWall=10, RightWall= 0, animate = False) #Walls LeftWall is right of RightWall
    assert result == None
    result = m.DropTwoBalls(x1,20,vx1,vy1,x2,y2,vx2,vy2, animate = False) #one of the balls is outside of the box
    assert result == None
    result = m.DropTwoBalls("hey",y1,vx1,vy1,x2,y2,vx2,vy2, animate = False) #one of the inputs is a string
    assert result == None
    result = m.DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2,r1 = -0.5, animate = False) #one of the radii is negative
    assert result == None
    result = m.DropTwoBalls(x1,y1,vx1,vy1,x2,y2,vx2,vy2,m1 = -1, animate = False) #one of the masses is negative
    assert result == None
