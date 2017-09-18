import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.style.use('ggplot')

theta = np.arange(0, 10, 0.01)
k     = 1

def integ(u,phi):
  def f(uphi,theta):
    u = uphi[0]
    phi=uphi[1]
    return [-u**2*(np.sin(phi)-k),u*np.cos(phi)-1]
  return odeint(f,[u,phi],theta)

def u2r(u):
  return list(map(lambda u: 1/u , u))

if __name__ == '__main__':
  integral = lambda i,j : integ(i,-0.05*j) #-np.pi/2+0.01*j)
  for i in range(10):
    for j in range(20):
      p = integral(i,j)
      plt.plot(p[:,1],u2r(p[:,0]))
      print((i,j))
  plt.show()


