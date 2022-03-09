# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot deviation of chemical potential from the bandgap center mu, mu_m_const in eV

Requires:   chemical_potential.py
"""

import chemical_potential as cp
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

T_axis = np.arange(1., 605., 5.)

muO = cp.ChemicalPotential()
mu_list = []
mu_m_const_list = []

for T_sim in T_axis:
    mu = muO.mu(T_sim)[0]
    mu_list.append(mu)
    mu_m_const = muO.mu(T_sim)[1]
    mu_m_const_list.append(mu_m_const)

#------------------------------------------------------------------------------
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Temperatur $T / K$')
ax1.set_ylabel(r'Chemisches Potential $\Delta\mu / eV$')
ax1.plot(T_axis, mu_m_const_list, 'b', label=r'$\Delta\mu$ mit $m_{c/v}^{\ast} = m_{c/v}^{\ast}(300 K)$')
ax1.plot(T_axis, mu_list, 'r--', label=r'$\Delta\mu$ mit $m_{c/v}^{\ast} = m_{c/v}^{\ast}(T)$')
ax1.legend()
mpl_p.show()
