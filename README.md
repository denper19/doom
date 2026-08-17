## Setting up the project

setup

## Foreword

Not possible without this EXTREMELY helpful resource... [Raycasting](https://lodev.org/cgtutor/raycasting.html)

## How it works

Doom is a 2D game made to look 3D using raycasting: A technique in which a ray is 'casted' from the players position out into the 2D map until it an object.

This information is then used to compute how far the wall is, how to render it, etc...

A naive implementation of raycasting would involve calculating the ray direction, casting a ray in that direction, and gradually incrementing. At each increment you would then check if the final position of the ray is inside an obstacle, if not, keep incrementing. Expectedly, this takes a long time, has the possibility of missing the obstacle if the increments are too large, and doesn't reliably give you the distance to collision point (where the ray first hits the wall). This could all be remedied IF you increment by a smaller amount, maybe even...infinitely small, but this would then lead to WAYYY longer compute times making it infeasible. 

An alternate solution, and the one that was used, is the DDA algorithm. It's significanlty faster, finds the collision point, and is reliable. DDA is the core of the raycasting engine here. 


