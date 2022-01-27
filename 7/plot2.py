#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_fuel(x, y):
    dist = abs(y - x)
    return (dist * (dist + 1)) / 2


X = np.asarray([0, 0, 0, 0, 0, 99, 99, 99, 99])
#X = np.asarray([16,1,2,0,4,2,7,1,2,14])
y = np.arange(X.min() - 2, X.max() + 3, 0.001)
y = np.arange(43.5, 45, 0.00001)
fuel = np.asarray([np.vectorize(get_fuel)(X, y[idx]).sum() for idx in range(y.shape[0])])
v_line = y[fuel.argmin()]
h_line = fuel[fuel.argmin()]
print(v_line)
print(h_line)
import code
#code.interact(local=locals())
print(np.median(X))
print(X.mean())

df = pd.DataFrame([y, fuel])
df = df.transpose().set_index(0)#transpose and set ratios as index
df.rename(columns={1:'Fuel'}, inplace=True)
fig, ax = plt.subplots()
df.plot(ax=ax, color='black', style='-')
plt.axhline(h_line, alpha=0.5, linestyle=':')
plt.axvline(v_line, alpha=0.5, linestyle=':')
plt.xlabel('Crab Collection Point')
plt.ylabel('Fuel')
plt.suptitle('Part 2:  Fuel Required vs Crab Collection Point (CCP)')
plt.legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
plt.grid(axis='both')
plt.xticks(np.arange(y.min(), y.max() + 1, 1.0))
#plt.yticks(np.arange(fuel.min(), fuel.max() + 1, 1.0))
fig.set_size_inches(12, 8)
plt.savefig("part2_plot.png")
plt.close()

fig, ax = plt.subplots()
df.plot(ax=ax, color='black', style='-')
plt.axhline(h_line, alpha=0.5, linestyle=':')
plt.axvline(v_line, alpha=0.5, linestyle=':')
plt.xlabel('Crab Collection Point')
plt.ylabel('Fuel')
plt.suptitle('Part 2:  Fuel Required vs Crab Collection Point (CCP)')
plt.legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
plt.grid(axis='both')
v_line = int(v_line)
h_line = int(h_line)
plt.xlim(v_line - 3, v_line + 3)
plt.ylim(h_line - 1, h_line + 5)
plt.xticks(np.arange(v_line - 3, v_line + 4, 1.0))
plt.yticks(np.arange(h_line - 1, h_line + 6, 1.0))
fig.set_size_inches(12, 8)
plt.savefig("part2b_plot.png")
