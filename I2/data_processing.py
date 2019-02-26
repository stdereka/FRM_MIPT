from utils import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import scipy.stats as st
from scipy.optimize import curve_fit, root
import scipy.integrate as integrate


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
        plt.ylim(0, 70)
        if legend_param:
            legend_list.append(legend_param + '=' + str(mes[legend_param]) + unit)

    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel('$\lambda, nm$')
    plt.ylabel('$Transmittance, \%$')

    if legend_param:
        plt.legend(legend_list)

    plt.savefig(output)
    # plt.show()
    plt.close()


def linear_extrapolation(progr, lim, output):
    x = progr['number'].values[1:]
    nu = progr['nu'].values
    y = np.array([nu[i + 1] - nu[i] for i in range(len(x))])
    print('Pearson(delta_G, v_plus_1)={:.2}'.format(st.pearsonr(x, y)[0]))
    straight = lambda x, a, b: a * x + b
    pval, pcov = curve_fit(f=straight, xdata=x, ydata=y, p0=[1, 1])
    err = np.diag(pcov)**0.5
    a, b = pval
    omega = b
    omega_x = -a / 2
    pval, np.diag(pcov) ** 0.5
    straight_line = lambda x: straight(x, pval[0], pval[1])
    print_error('omega', omega, err[1])
    print_error('omega_x', omega_x, err[0]/2)
    xminor_locator = MultipleLocator(1)
    yminor_locator = MultipleLocator(4)
    xmajor_locator = MultipleLocator(5)
    ymajor_locator = MultipleLocator(20)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)
    plt.plot(x, y, 'bs')
    plt.plot(np.arange(lim[0][0], lim[0][1]+1, 0.1), straight_line(np.arange(lim[0][0], lim[0][1]+1, 0.1)), 'k')
    plt.xlim(lim[0])
    plt.ylim(lim[1])
    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel(r'$v+1$')
    plt.ylabel(r'$\Delta G_{v+\frac{1}{2}}, см^{-1}$')
    plt.savefig(output)
    # plt.show()
    plt.close()


def parabolic_extrapolation(progr, podgon, lim, output):
    omeg = 214.5
    x, y = progr['number'].values + 0.5, progr['nu'].values + podgon * omeg
    not_straight = lambda x, a, b, c: a * x ** 2 + b * x + c
    pval, pcov = curve_fit(f=not_straight, xdata=x, ydata=y, p0=[1, 1, 1])
    omega = pval[1]
    omega_x = -pval[0]
    t_e = pval[2]
    err = np.diag(pcov) ** 0.5
    print_error('omega', omega, err[1])
    print_error('omega_x', omega_x, err[0])
    print_error('T_e', t_e, err[2])
    not_straight_line = lambda x: not_straight(x, pval[0], pval[1], pval[2])
    xminor_locator = MultipleLocator(1)
    yminor_locator = MultipleLocator(200)
    xmajor_locator = MultipleLocator(5)
    ymajor_locator = MultipleLocator(1000)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)
    plt.plot(x, y, 'bs')
    plt.plot(np.arange(lim[0][0], lim[0][1]+1, 0.1), not_straight_line(np.arange(lim[0][0], lim[0][1]+1, 0.1)), 'k')
    plt.xlim(lim[0])
    plt.ylim(lim[1])
    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel(r'$v+\frac{1}{2}$')
    plt.ylabel(r'$\nu, см^{-1}$')
    plt.savefig(output)
    #plt.show()
    plt.close()


def shponer_extrapolation(progrs, output):
    progr1, progr2 = progrs
    v_plus_1 = progr1['number'].values[1:]
    nu = progr1['nu'].values
    delta_G = np.array([nu[i + 1] - nu[i] for i in range(len(v_plus_1))])
    _v_plus_1 = progr2['number'].values[1:]
    nu = progr2['nu'].values
    _delta_G = np.array([nu[i + 1] - nu[i] for i in range(len(_v_plus_1))])
    X, Y = np.hstack((v_plus_1 - 0.5, _v_plus_1 - 0.5)), np.hstack((delta_G, _delta_G))
    not_straight = lambda x, a, b, c: a * x ** 2 + b * x + c
    pval, pcov = curve_fit(f=not_straight, xdata=X, ydata=Y, p0=[1, 1, 1])
    not_straight_line = lambda x: not_straight(x, pval[0], pval[1], pval[2])
    rt = root(not_straight_line, 30).x[0]
    D_0 = integrate.quad(not_straight_line, 0, rt)[0]
    print('D_0={:.5}'.format(D_0))
    xminor_locator = MultipleLocator(1)
    yminor_locator = MultipleLocator(5)
    xmajor_locator = MultipleLocator(5)
    ymajor_locator = MultipleLocator(25)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)
    plt.plot(X, Y, 'bs')
    plt.plot(np.arange(0, 30, 0.1), not_straight_line(np.arange(0, 30, 0.1)), 'k')
    plt.xlim(0, 30)
    plt.ylim(0, 130)
    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel(r'$v+\frac{1}{2}$')
    plt.ylabel(r'$\Delta G_{v+\frac{1}{2}}, см^{-1}$')
    plt.savefig(output)
    plt.close()


def edge_frequency(progr, output):
    nu = progr['nu'].values
    delta_G = np.array([nu[i + 1] - nu[i] for i in range(len(nu) - 1)])
    nu = nu[:-1]
    not_straight = lambda x, a, b, c: a * x ** 2 + b * x + c
    pval, pcov = curve_fit(f=not_straight, xdata=delta_G, ydata=nu, p0=[1, 1, 1])
    err = np.diag(pcov)**0.5
    not_straight_line = lambda x: not_straight(x, pval[0], pval[1], pval[2])
    print_error('v_edge', pval[2], err[2])
    xminor_locator = MultipleLocator(1)
    yminor_locator = MultipleLocator(100)
    xmajor_locator = MultipleLocator(5)
    ymajor_locator = MultipleLocator(500)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)
    plt.plot(delta_G, nu, 'bs')
    plt.plot(np.arange(70, 95, 0.1), not_straight_line(np.arange(70, 95, 0.1)), 'k')
    plt.xlim(70, 95)
    plt.ylim(17500, 18800)
    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    plt.xlabel(r'$\Delta \nu, см^{-1}$')
    plt.ylabel(r'$\nu, см^{-1}$')
    plt.savefig(output)
    plt.close()


def plot_morze(d, beta, output=None):
    morze = lambda r: d*(1-np.exp(-beta*r))**2
    x = np.arange(-0.4, 6, 0.01)
    xminor_locator = MultipleLocator(0.2)
    yminor_locator = MultipleLocator(300)
    xmajor_locator = MultipleLocator(1)
    ymajor_locator = MultipleLocator(1500)
    ax = plt.subplot()
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.yaxis.set_minor_locator(yminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.yaxis.set_major_locator(ymajor_locator)
    plt.plot(x, morze(x))
    plt.xlim(-0.5, 5)
    plt.ylim(0, 6000)
    plt.ylabel(r'$U(r-r_e), sm^{-1}$')
    plt.xlabel(r'$r-r_e, \AA$')
    plt.grid(which='minor', ls='--', lw=0.5, c='grey')
    plt.grid(which='major', ls='-', lw=0.5, c='k')
    #plt.show()
    plt.savefig(output)

