import csv
import numpy as np
import matplotlib.pyplot as plt

filename = 'lab1.csv'
data = []
with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';')
    for row in csvreader:
        data.append(row)
new_data = [[float(x.replace("'", "")) for x in sublist] for sublist in data]
print(len(new_data))
x_e = np.array([x[0] for x in new_data])
matrixx = np.array([x[1] for x in new_data])
print('мои значения х из лабы',x_e, len(x_e))
matrix_b = matrixx.T
print('полученные ускорения или b',matrixx)

t = np.arange(0, len(x_e) * 0.05, 0.05)
print(t,len(t))
# матрица
dt=0.05
cc=-2/(dt**2)
c=1/(dt**2)
n=len(x_e)
matrix_a = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i==j and (i==0 or i==n-1):
            matrix_a[i][j] = 1
        elif i == j and j!=1:
            matrix_a[i][j] = cc
        elif i == j - 1 or i == j + 1:
           matrix_a[i][j] = c
for row in matrix_a:
    print(row)

matrix_a_inv=np.linalg.inv(matrix_a)
rx= np.round(matrix_a_inv, 3)
x = np.dot(rx, matrixx)
print('полученные х', x)
x+=[1]
print(len(x),x,len(t),t)
plt.plot(x, t, label='Теоретический результат')
#plt.plot(x_e, t, label='Экспериментальный результат')
plt.show()