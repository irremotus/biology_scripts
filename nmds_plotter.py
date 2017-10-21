#!/usr/bin/python3

# MIT License
# 
# Copyright (c) 2017 Kevin A. Schmittle
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns


sns.set(style='ticks', palette='Set2')
sns.despine()


if len(sys.argv) < 2:
    print("Usage:  {prog} <data file> <map file> <title> <x axis> <y axis> <legend title> <output file>".format(
        prog=sys.argv[0]
        ))
    sys.exit(1)


data_filename = sys.argv[1]
map_filename = sys.argv[2]
title = sys.argv[3]
xaxis = sys.argv[4]
yaxis = sys.argv[5]
legend = sys.argv[6]
outname = sys.argv[7]

df = pd.DataFrame()

with open(data_filename, "r") as f:
    header = f.readline().split()
    names = []
    x = []
    y = []
    z = []
    for line in f.readlines():
        parts = line.split()
        names.append(parts[0])
        x.append(float(parts[1]))
        y.append(float(parts[2]))
with open(map_filename, "r") as f:
    header = f.readline().split()
    mapping = {}
    for line in f.readlines():
        parts = line.split()
        mapping[parts[0]] = (parts[1], parts[3])
df['x_axis_data'] = x
df['y_axis_data'] = y
df[legend] = [mapping[name][1] for name in names]

sns.set_style("ticks")

plot = sns.lmplot('x_axis_data',
           'y_axis_data',
           data=df,
           fit_reg=False,
           hue=legend,
           scatter_kws={"marker": "D", "s": 100})

plt.title(title)
plt.xlabel(xaxis)
plt.ylabel(yaxis)


plot.savefig(outname)
