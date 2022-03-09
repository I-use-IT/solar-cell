# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot current density-voltage characteristic J(U) in A/m**2 for various parameter temperature dependency-combinations with two-diode-model
            Plot power-voltage characteristic P(U)
            Plot solar cell characteristics U_oc, J_sc, U_MPP, J_MPP, S_MPP, FF, eta

Requires:   twodiodemodel.py

===============================================================================
MANUAL:
1.)    set values (J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim)
2.)    set temperature dependent (active) parameters (J_sx_on, E_g_on, m_x_eff_on, D_x_on, mu_x_on)
3.)    call T_SC.set_values(bla), T_SC.set_active_effects(blubb) and then T_SC.j_u_curve(U_list) / T_SC.p_u_curve(U_list) / ...
4.)    plotting results
===============================================================================
"""

import twodiodemodel as tdm
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

U_list = np.arange(0.0, 0.71, 0.005)

T_SC = tdm.SiCell()

#------------------------------------------------------------------------------
# print pre-set values
print('values pre-set in twodiodemodel.py')
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
print('-------------------------------------------------------------------------------------')



#==============================================================================
# 1.)
# set values (convert established units to SI units without prefixes!):

# set initial / fit values:
J_ph = -1.0e-20 * 10.0              # mA/cm**2 * 10.0 = A/m**2        -350
J_s1 = 0.0264241506976 * 1.0e-8     # pA/cm**2 * 1.0e-8 = A/m**2        0.0264236925384
J_s2 = 7.19540025472 * 1.0e-5       # nA/cm**2 * 1.0e-5 = A/m**2        7.19541877525
R_s = 0.241325240977 * 1.0e-4       # Ohm*cm**2 * 1.0e-4 = Ohm*m**2        0.241307648072
R_p = 36297.3993603 * 1.0e-4        # Ohm*cm**2 * 1.0e-4 = Ohm*m**2        36297.4065154
T_ini = 5.00 + 273.15               # K

# set simulation values:
T_sim1 = 5.00 + 273.15              # K
T_sim2 = 60.00 + 273.15             # K



#==============================================================================
# 2.)
# set active effects:        (0 and 1 is valid)
J_sx_on = 0
E_g_on = 0
m_x_eff_on = 0
D_x_on = 0
mu_x_on = 0



#==============================================================================
# 3.)
# calculate J-U_curve(U_list, initial/fit values, active_effects)

#------------------------------------------------------------------------------
# Variante 1
print('----------1a: J_T_sim1 without temperature dependencies----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim1)
T_SC.set_active_effects(J_sx_on, E_g_on, m_x_eff_on, D_x_on, mu_x_on)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim1_00000 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')
#------------------------------------------------------------------------------
print('----------1b: J_T_sim2 without temperature dependencies----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim2)
T_SC.set_active_effects(J_sx_on, E_g_on, m_x_eff_on, D_x_on, mu_x_on)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim2_00000 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')



#------------------------------------------------------------------------------
# Variante 2
print('----------2a: J_T_sim1 with J_sx(T)----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim1)
T_SC.set_active_effects(1, 0, 0, 0, 0)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim1_10000 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')
#------------------------------------------------------------------------------
print('----------2a: J_T_sim2 with J_sx(T)----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim2)
T_SC.set_active_effects(1, 0, 0, 0, 0)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim2_10000 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')



#------------------------------------------------------------------------------
# Variante 3
print('----------3a: J_T_sim1 with J_sx(T), E_g(T), m_x_eff(T), D_x(T) and mu_x(T)----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim1)
T_SC.set_active_effects(1, 1, 1, 1, 1)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim1_11111 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')
#------------------------------------------------------------------------------
print('----------3b: J_T_sim2 with J_sx(T), E_g(T), m_x_eff(T), D_x(T) and mu_x(T)----------')
T_SC.set_values(J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim2)
T_SC.set_active_effects(1, 1, 1, 1, 1)
print('J_ph =', T_SC.J_ph, ', J_s1_T_ini =', T_SC.J_s1_T_ini, ', J_s2_T_ini =', T_SC.J_s2_T_ini, ', R_s =', T_SC.R_s, ', R_p =', T_SC.R_p)
print('T_ini =', T_SC.T_ini, ', U_Te_T_ini =', T_SC.U_Te_T_ini, ', T_sim =', T_SC.T_sim, ', U_Te_T_sim =', T_SC.U_Te_T_sim)
print('active parameters (J_sx, E_g, m_x_eff, D_x, mu_x) =', T_SC.J_sx_on, T_SC.E_g_on, T_SC.m_x_eff_on, T_SC.D_x_on, T_SC.mu_x_on)
J_T_sim2_11111 = T_SC.j_u_curve(U_list)
print('J_s1_T_sim =', T_SC.J_s1, ', J_s2_T_sim =', T_SC.J_s2)
print('-------------------------------------------------------------------------------------')



#==============================================================================
# experimental data from *.dat file (Keithley source meter)
fobj_U_T_sim1 = open('5-00_U.txt','r')
U_T_sim1_str = fobj_U_T_sim1.read()
fobj_U_T_sim1.close()
U_T_sim1_str_list = U_T_sim1_str.splitlines()
U_T_sim1_list = [float(i) for i in U_T_sim1_str_list]

fobj_J_T_sim1 = open('5-00_J.txt','r')
J_T_sim1_str = fobj_J_T_sim1.read()
fobj_J_T_sim1.close()
J_T_sim1_str_list = J_T_sim1_str.splitlines()
J_T_sim1_list = [float(i) for i in J_T_sim1_str_list]

fobj_U_T_sim2 = open('60-00_U.txt','r')
U_T_sim2_str = fobj_U_T_sim2.read()
fobj_U_T_sim2.close()
U_T_sim2_str_list = U_T_sim2_str.splitlines()
U_T_sim2_list = [float(i) for i in U_T_sim2_str_list]

fobj_J_T_sim2 = open('60-00_J.txt','r')
J_T_sim2_str = fobj_J_T_sim2.read()
fobj_J_T_sim2.close()
J_T_sim2_str_list = J_T_sim2_str.splitlines()
J_T_sim2_list = [float(i) for i in J_T_sim2_str_list]



#==============================================================================
# 4.)
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Spannung   $U / V$')
ax1.set_ylabel(r'Stromdichte   $\vec{J} / \frac{A}{m^2}$')
ax1.plot(U_T_sim1_list, J_T_sim1_list, 'ko', label=r'$J(\vartheta_u)$ Messwerte')
ax1.plot(U_T_sim2_list, J_T_sim2_list, 'kD', label=r'$J(\vartheta_o)$ Messwerte')
ax1.plot(U_list, J_T_sim1_00000, 'b', label=r'$J(\vartheta_u)$ simuliert nach Variante 1')
ax1.plot(U_list, J_T_sim2_00000, 'r', label=r'$J(\vartheta_o)$ simuliert nach Variante 1')
ax1.plot(U_list, J_T_sim1_10000, 'g*', label=r'$J(\vartheta_u)$ simuliert nach Variante 2')
ax1.plot(U_list, J_T_sim2_10000, 'c', label=r'$J(\vartheta_o)$ simuliert nach Variante 2')
ax1.plot(U_list, J_T_sim1_11111, 'm', label=r'$J(\vartheta_u)$ simuliert nach Variante 3')
ax1.plot(U_list, J_T_sim2_11111, 'y', label=r'$J(\vartheta_o)$ simuliert nach Variante 3')
mpl_p.xlim(0.0, 0.7)
mpl_p.ylim(0.0, 400.0)
ax1.legend()

fig2 = mpl_p.figure(2)
ax2 = fig2.add_subplot(111)
ax2.set_xlabel(r'Spannung   $U / V$')
ax2.set_ylabel(r'Stromdichte   $\vec{J} / \frac{A}{m^2}$')
ax2.semilogy(U_T_sim1_list, J_T_sim1_list, 'ko', label=r'$J(\vartheta_u)$ Messwerte')
ax2.semilogy(U_T_sim2_list, J_T_sim2_list, 'kD', label=r'$J(\vartheta_o)$ Messwerte')
ax2.semilogy(U_list, J_T_sim1_00000, 'b', label=u'$J(\vartheta_u)$ simuliert nach Variante 1')
ax2.semilogy(U_list, J_T_sim2_00000, 'r', label=r'$J(\vartheta_o)$ simuliert nach Variante 1')
ax2.semilogy(U_list, J_T_sim1_10000, 'g*', label=r'$J(\vartheta_o)$ simuliert nach Variante 2')
ax2.semilogy(U_list, J_T_sim2_10000, 'c*', label=r'$J(\vartheta_o)$ simuliert nach Variante 2')
ax2.semilogy(U_list, J_T_sim1_11111, 'ms', label=r'$J(\vartheta_o)$ simuliert nach Variante 3')
ax2.semilogy(U_list, J_T_sim2_11111, 'ys', label=r'$J(\vartheta_o)$ simuliert nach Variante 3')
mpl_p.xlim(0.0, 0.7)
mpl_p.ylim(1.0e-3, 400.0)

mpl_p.show()
