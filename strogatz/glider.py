#Strogatz p207 6.5.14 glider
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#equation
def func(v_theta, t):
    v     = v_theta[0]
    theta = v_theta[1]
    return [-np.sin(theta),(-np.cos(theta)+v**2)/v]

init = [1,0]
t = np.arange(0, 10, 0.01)

#execute
v_theta = odeint(func, init, t)
#v     = v_theta[:,0]
#theta = v_theta[:,1]

#show
#fig = plt.figure()
plt.plot(v_theta[:,1],v_theta[:,0])
plt.show()
