# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot effective carrier masses m_c, m_v in multiplicative partivas of the free electron rest mass in 1.

Requires:   effective_masses.py
"""

import effective_masses as em
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

T_axis = np.arange(1., 605., 5.)

mO = em.EffectiveMasses()
m_c_list = []
m_v_list = []

for T_sim in T_axis:
    m_c_list.append(mO.m_x(T_sim)[0])
    m_v_list.append(mO.m_x(T_sim)[1])

#------------------------------------------------------------------------------
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Temperatur $T / K$')
ax1.set_ylabel(r'Effektive Massen $m_{c/v}^{\ast} / m_e$')
ax1.plot(mO.T_Green, mO.m_c_Green, 'ko', label=r'$m_c^{\ast}$ Messwerte aus Green (1990)')
ax1.plot(mO.T_Green, mO.m_v_Green, 'kD', label=r'$m_v^{\ast}$ Messwerte aus Green (1990)')
ax1.plot(T_axis, m_c_list, 'b-', label=r'Effektive Leitungsband-Elektronenmasse $m_c^{\ast}$')
ax1.plot(T_axis, m_v_list, 'r--', label=r'Effektive Valenzband-Loechermasse $m_v^{\ast}$')
ax1.legend()
mpl_p.show()
