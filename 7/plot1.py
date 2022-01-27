#!/usr/bin/python3

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_fuel(x, y):
    return abs(x - y)


X = np.asarray([0, 0, 0, 0, 1, 9, 10, 11, 12])
y = np.arange(X.min() - 2, X.max() + 3, 0.01)
fuel = np.asarray([np.vectorize(get_fuel)(X, y[idx]).sum() for idx in range(y.shape[0])])
v_line = y[fuel.argmin()]
h_line = fuel[fuel.argmin()]
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
plt.suptitle('Part 1:  Fuel Required vs Crab Collection Point (CCP)')
plt.legend(loc='best', shadow=True, fontsize='small', facecolor='#d0d0d0')
plt.grid(axis='both')
fig.set_size_inches(12, 8)
plt.savefig("part1_plot.png")
