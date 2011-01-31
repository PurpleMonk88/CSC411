    # Formulas from C. Pickover
   
from scipy import *
from pylab import *
    
# Creating the grid of coordinates x,y 
x,y = ogrid[-1.:1.:.01, -1.:1.:.01]

z = 3*y*(3*x**2-y**2)/4 + .5*cos(6*pi * sqrt(x**2 +y**2) + arctan2(x,y))

hold(True)
# Creating image
imshow(z, origin='lower', extent=[-1,1,-1,1])

# Plotting contour lines
contour(z, origin='lower', extent=[-1,1,-1,1])

xlabel('x')
ylabel('y')
title('A spiral !')

# Adding a line plot slicing the z matrix just for fun. 
plot(x[:], z[50, :])

savefig('spiral')
