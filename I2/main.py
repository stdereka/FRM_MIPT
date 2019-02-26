from utils import *
from data_processing import *
import os
import pandas as pd


print('Stage 0. Reading data...\n')

data = {}
for i, name in enumerate(os.listdir('data')):
    data[i] = {}
    d = data[i]
    d['data'] = read_dat_file(os.path.join('data', name), ['lambda', 'trans'])
    params = get_params_from_file_name(name)
    d['T'], d['d'], d['left_bound'], d['right_bound'] = params


print('Stage 1. Drawing transparency graphs...\n')

for i in data:
    m = data[i]
    plot_transparency_curves([m], 'results/' + str(m['T']) + '_' + str(m['d']) + '.pdf')

plot_transparency_curves([data[4]], 'results/40C.pdf')
plot_transparency_curves([data[6], data[0], data[5], data[4]], 'results/0.2nm.pdf', legend_param='T', unit='C')
plot_transparency_curves([data[6], data[2], data[1], data[3]], 'results/70C.pdf', legend_param='d', unit='nm')


print('Stage 2. Building Delandre table...\n')

progr1 = pd.read_csv('progr1.csv')
progr2 = pd.read_csv('progr2.csv')
progr1['nu'] = 1/(progr1['lambda']*1e-7)
progr2['nu'] = 1/(progr2['lambda']*1e-7)


print('Stage 3. Applying linear extrapolation method...\n')

print('Progression v"=1:')
linear_extrapolation(progr1, ((0, 24), (60, 180)), 'results/linear_v_1.pdf')
print()
print('Progression v"=0:')
linear_extrapolation(progr2, ((0, 30), (60, 180)), 'results/linear_v_0.pdf')
print()


print('Stage 4. Applying parabolic extrapolation method...\n')

print('Progression v"=1:')
parabolic_extrapolation(progr1, 1.5, ((0, 30), (15000, 20000)), 'results/parabolic_v_1.pdf')
print()

print('Progression v"=0:')
parabolic_extrapolation(progr2, 0.5, ((0, 30), (15000, 20000)), 'results/parabolic_v_0.pdf')
print()

print('Stage 5. Computing edge frequency...')
edge_frequency(progr2, 'results/edge.pdf')
print()

print('Stage 6. Computing dissociation energy using Shponer extrapolation method...')
shponer_extrapolation((progr1, progr2), 'results/shponer.pdf')
print()

print('Stage 7. Drawing Morze curve...')
plot_morze(3476.5, 2.155, 'results/morze.pdf')
print()
