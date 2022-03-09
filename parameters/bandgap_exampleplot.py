# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot bandgap E_g with different models in eV

Requires:   bandgap.py
"""

import bandgap as bg
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

T_axis = np.arange(1., 605., 5.)

bgO = bg.Eg()
E_g_BardeenShockley, E_g_Varshni, E_g_Varshni_modified, E_g_Bludau, E_g_Gaensslen, E_g_Green, E_g_Green_modified, E_g_Paessler, E_g_Paessler2 = bgO.eg_lists(T_axis)

#------------------------------------------------------------------------------
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Temperatur $T / K$')
ax1.set_ylabel(r'Energiebandlücke $E_g / eV$')
ax1.plot(bgO.T_MacFarlane, bgO.E_g_MacFarlane, 'ko', label=r'$E_{g, exp}$ MacFarlane et. al. (1958)')
ax1.plot(bgO.T_Green, bgO.E_g_Green, 'ks', label=r'$E_{g, exp}$ Green (1990)')
ax1.plot(T_axis, E_g_BardeenShockley, 'k', label=r'$E_g$ Bardeen, Shockley (1950)')
ax1.plot(T_axis, E_g_Varshni, 'b.-', label=r'$E_g$ Varshni (1967)')
ax1.plot(T_axis, E_g_Varshni_modified, 'b', label=r'$E_g$ Varshni (1967) modified')
ax1.plot(T_axis, E_g_Bludau, 'r--', label=r'$E_g$ Bludau et al. (1974)')
ax1.plot(T_axis, E_g_Gaensslen, 'r.--', label=r'$E_g$ Gaensslen (1976-79)')
ax1.plot(T_axis, E_g_Green, 'g*', label=r'$E_g$ Green (1990)')
ax1.plot(T_axis, E_g_Green_modified, 'g.', label=r'$E_g$ Green (1990) modified')
ax1.plot(T_axis, E_g_Paessler, 'k2', label=r'$E_g$ Paessler (1999)')
ax1.plot(T_axis, E_g_Paessler2, 'orange', label=r'$E_g$ Paessler (2002)')
ax1.legend()
mpl_p.show()
