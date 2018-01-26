import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

L = 1
xs = np.linspace(0,L,100)


def integrate(init,xs,params):
    def func(variables,init):
        [u,v,p,q]=variables
        [b,Du,Dv]=params
        dot_u = p
        dot_v = q
        dot_p = b/Du*p - 1/Du*(u**2/v)
        dot_q = 1/Dv*q - 1/Dv*(u**2/v)
        return[dot_u,dot_v,dot_p,dot_q]
    return odeint(func,init,xs)


def execute(b,Du,Dv):
#shooting method
    iteration = 10
    u, v      = 1 ,1
    du,dv     = 0.001*u,0.001*v

    p_f = lambda u,v: integrate([u,v,0,0],xs,[b,Du,Dv])[-1][2]
    q_f = lambda u,v: integrate([u,v,0,0],xs,[b,Du,Dv])[-1][3]

    for i in range(iteration):
        del_pf_u = ( p_f(u+du,v)-p_f(u,v) ) / du
        del_pf_v = ( p_f(u,v+dv)-p_f(u,v) ) / dv
        del_qf_u = ( q_f(u+du,v)-q_f(u,v) ) / du
        del_qf_v = ( q_f(u,v+dv)-q_f(u,v) ) / dv

        function = np.array ([[p_f(u,v)],[q_f(u,v)]])
        Jacobi   = np.matrix([[del_pf_u,del_pf_v],[del_qf_u,del_qf_v]])

        # print(u,v)
        # print(Jacobi)

        # print(np.linalg.det(Jacobi))

        if (abs(function[0,0])<0.0001 and abs(function[1,0])<0.0001) : break

        if np.linalg.det(Jacobi)==0:
            diff = 0
            u,v = 1e10,1e10
            break

        diff = -np.dot(Jacobi.I,function)
        u,v = u+diff[0,0],v+diff[1,0]

    u0,v0 = u,v

    result = integrate([u0,v0,0,0],xs,[b,Du,Dv])
    ux,vx    =  result[:,0],result[:,1]
    return (ux,vx)

(u,v) = execute(4,2,1)

plt.plot(xs,u)
# plt.plot(xs,v)
plt.show()
