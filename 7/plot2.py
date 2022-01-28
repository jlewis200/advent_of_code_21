#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_fuel(x, y):
    dist = abs(y - x)
    return (dist * (dist + 1)) / 2

def get_fuel2(x, y):
    return abs(y - x)

X = np.asarray([0, 0, 0, 0, 1, 9, 10, 11, 12])
y = np.arange(X.min() - 2, X.max() + 3, 0.01)
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
plt.axhline(h_line)
plt.axvline(v_line)
plt.xlabel('Crab Collection Point')
plt.ylabel('Fuel')
plt.suptitle('Part 2:  Fuel Required vs Crab Collection Point (CCP)')
plt.legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
plt.grid(axis='both')
plt.xticks(np.arange(y.min(), y.max() + 1, 1.0))
fig.set_size_inches(12, 8)
plt.savefig("part2a.png")


fig, ax = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0.12})

df.plot(ax=ax[0], color='black', style='-')
ax[0].axhline(h_line)
ax[0].axvline(v_line)
ax[0].set(ylabel='Fuel', title='Part 1 Fuel Function')
ax[0].legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
ax[0].grid(axis='both')

fuel = np.asarray([np.vectorize(get_fuel2)(X, y[idx]).sum() for idx in range(y.shape[0])])
df = pd.DataFrame([y, fuel])
df = df.transpose().set_index(0)#transpose and set ratios as index
df.rename(columns={1:'Fuel'}, inplace=True)
v_line = y[fuel.argmin()]
h_line = fuel[fuel.argmin()]

df.plot(ax=ax[1], color='black', style='-')
ax[1].axhline(h_line)
ax[1].axvline(v_line)
ax[1].set(ylabel='Fuel', title='Part 2 Fuel Function')
ax[1].legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
ax[1].grid(axis='both')

plt.suptitle('Fuel Function Comparison')
plt.xlabel('Crab Collection Point')
plt.xticks(np.arange(y.min(), y.max() + 1, 1.0))
fig.set_size_inches(12, 8)
plt.savefig("part2b.png")
