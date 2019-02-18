from utils import *
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def plot_transparency_curves(measurements: list, output: str, legend_param: str = None, unit: str = ''):
    legend_list = []
    xminor_locator = MultipleLocator(5)
    yminor_locator = MultipleLocator(2)
    xmajor_locator = MultipleLocator(25)
    ymajor_locator = MultipleLocator(10)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)

    for mes in measurements:
        x, y = mes['data'].values.T
        plt.plot(x, y, linewidth=0.8)
        plt.xlim(mes['left_bound'], mes['right_bound'])
        plt.ylim(0, 100)
        if legend_param:
            legend_list.append(legend_param + '=' + str(mes[legend_param]) + unit)

    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel('$\lambda, nm$')
    plt.ylabel('$Transparency, \%$')

    if legend_param:
        plt.legend(legend_list)

    plt.savefig(output)
    plt.show()
    plt.close()


data = {}
for i, name in enumerate(os.listdir('data')):
    data[i] = {}
    d = data[i]
    d['data'] = read_dat_file(os.path.join('data', name), ['lambda', 'trans'])
    params = get_params_from_file_name(name)
    d['T'], d['d'], d['left_bound'], d['right_bound'] = params


print('Building transparency graphs ...')

for i in data:
    mes = data[i]
    plot_transparency_curves([mes], 'results/' + str(mes['T']) + '_' + str(mes['d']) + '.pdf')

plot_transparency_curves([data[4]], 'results/40C.pdf')
plot_transparency_curves([data[6], data[0], data[5], data[4]], 'results/0.2nm.pdf', legend_param='T', unit='C')
plot_transparency_curves([data[6], data[2], data[1], data[3]], 'results/70C.pdf', legend_param='d', unit='nm')
