# ball-dropped-in-box
Mariza Wildschut 5762944
This project will simulate 2 balls of the same mass when dropped in a box.  
The code will calculate how the balls interact with eachother and with the walls, the floor and the ceiling. It will not take friction in account and it will assume completely elastic collision. The interaction between the balls will be calculated using the law of conservation of moments. 
The calculations for this project will be done using numpy, and the visualisation will be done using matplotlib. The animation will run for 10 seconds, unless otherwise specified. 
The input of the code will consist of the initial position and the initial speeds of the balls in the x and y direction, with optional inputs for the radius of the balls, the masses of the balls, the locations of the walls, floor and ceiling and the total runtime. 
The code will generate an animation of the trajectory that the balls take. 

## How to run
To run the program the file "main" should be imported. Then function main.DropTwoBalls(x1,y1,x2,y2,vx1,vy1,vx2,vy2,r1, r2, m1, m2, BoxWidth, BoxHeight, tmax) can be used. This function needs integers or floats as input values for x1, y1, x2 and y2, which are the x and y coordinates of the two balls. The function has optional inputs for the following variables, if nothing is given they will take standard values:
- The intial velocities of the balls: vx1, vy1, vx2 and vy2, with a standard value of 0 m/s.
- The masses and radii of the balls: r1 and r2, with a standard value of 0.5 m and m1 and m2 with a standard value of 1.0 kg.
- The size of the box: BoxWidth and BoxHeight, with a standard value of 10.0 m. 
- The total runtime: tmax, with a standard value of 10 seconds.
The function will then generate an animation with the initial values that were given.