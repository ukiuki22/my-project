#Strogatz p207 6.5.14 glider
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

plt.style.use('ggplot')

#equation
def func(v_theta, t):
    v     = v_theta[0] #+0.1
    theta = v_theta[1]
    D = 0.1
    return [-np.sin(theta)-D*v**2,(-np.cos(theta)+v**2)/v]

#execute
def v_theta(init):
    t = np.arange(0, 6, 0.01)
    v_theta = odeint(func, init, t)
    return v_theta

#uv空間に射影
def map2uv(init):
    glider=v_theta(init)
    v     = glider[:,0]
    theta = glider[:,1]
    U = list(map(lambda v,th:v*np.cos(th) , v,theta))
    V = list(map(lambda v,th:v*np.sin(th) , v,theta))
    return [U,V]

def map2xy(init):
    glider=map2uv(init)
    add = lambda x,y:x+y*0.01
    X = list(scanl(add,0,glider[0]))
    Y = list(scanl(add,1,glider[1]))
    return [X,Y]

#source: https://stackoverflow.com/questions/14423794/equivalent-of-haskell-scanl-in-python
def scanl(f, base, l):
    for x in l:
        base = f(base, x)
        yield base

def plot_some_initial_XY(init_v,length,iteration):
    gliders = [map2xy([init_v+length*i,0]) for i in range(iteration)]
    for i in range(iteration):
        plt.plot(gliders[i][0],gliders[i][1])
    return plt.show()

#    plot_some_initial_UV(1.0,0.1,20)
def plot_some_initial_UV(init_v,length,iteration):
    gliders = [map2uv([init_v+length*i,0]) for i in range(iteration)]
    for i in range(iteration):
        plt.plot(gliders[i][0],gliders[i][1])
    return plt.show()

# v_theta 複数の初期条件を同時にプロット
#   plot_some_initial_vt(1,0.1,20)
def plot_some_initial_vth(init_v,length,iteration):
    gliders=[v_theta([init_v+length*i,0]) for i in range(iteration)]
    for i in range(iteration):
        plt.plot(gliders[i][:,1],gliders[i][:,0])
    return plt.show()

if __name__ == '__main__':
    plot_some_initial_XY(0.6,0.4,6)
