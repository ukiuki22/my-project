import matplotlib.pyplot as plt
import numpy as np

k_max,m_max = 1e-8,1e-8 # 1/m

sigma_a = 4.5e-4
N       = 3.6e-4
f       = 5.3e-9
cs      = 10.4e4

A,B,C = (sigma_a/cs)**2 ,(N/cs)**2 ,(f/cs)**2
print(np.sqrt(A),np.sqrt(B),np.sqrt(C))

plt.style.use('ggplot')
xrange = np.linspace(0, k_max, 100)
yrange = np.linspace(0, m_max, 100)
k, m = np.meshgrid(xrange,yrange)

#軸の設定
plt.axis([0, 1, 0, 1])
plt.gca().set_aspect('equal', adjustable='box')

#描画
isJ = -(k**2 + m**2 - A - C ) 
isF = B*k**2 + C*m**2 - A*C 
isD = -(k**2 + m**2 - A)**2 + 4*(B*k**2 + C*m**2 - A*C)

plt.contour(k, m, isJ)#, [0])
plt.contour(k, m, isF)#, [0])
plt.contour(k, m, isD)#, [0])
plt.show()