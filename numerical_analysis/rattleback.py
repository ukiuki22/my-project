# rattle back

# patamaters@cgs
a,b,c = 5,2,1
m     = 10
delta = 0.1 #radian
gamma = 0.25 #contact point / a
mu    = 0.1
g     = 98 #cm/s/s

I1 = 0.2*m*a*a
I2 = 0.2*m*b*b
I3 = 0.2*m*c*c

J = delta *m*a*b
a2 = gamma * a

# u_dot = -(g-a2*(omega2))
