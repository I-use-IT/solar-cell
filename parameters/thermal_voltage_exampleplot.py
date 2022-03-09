# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot thermal voltage U_T in mV

Requires:   thermal_voltage.py
"""

import thermal_voltage as tv
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

T_axis = np.arange(0., 605., 5.)

tvO = tv.ThermalVoltage()
U_T_list = []

for T_sim in T_axis:
    U_T = tvO.u_t(T_sim)
    U_T_list.append(U_T*1000)

#------------------------------------------------------------------------------
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Temperatur $T / K$')
ax1.set_ylabel(r'Temperaturspannung $U_T / mV$')
ax1.plot(T_axis, U_T_list, 'b', label=r'Temperaturspannung $U_T$')
ax1.legend()
mpl_p.show()
