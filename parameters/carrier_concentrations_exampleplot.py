# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Plot intrinsic carrier concentration n_i with different models in cm^-3
            Plot electron n and hole concentration p in cm^-3

Requires:   carrier_concentrations.py
"""

import carrier_concentrations as cc
import numpy as np
import matplotlib.pyplot as mpl_p
#==============================================================================

T_axis = np.arange(100., 605., 5.)

N_D = 1.0e18    #9e19
N_A = 1.0e6     #1e20

NiMorinMaitaO = cc.MorinMaita()
NiPutleyMitchellO = cc.PutleyMitchell()
NiBarberO = cc.Barber()
NiSlotboomO = cc.Slotboom()
NiWasserabO = cc.Wasserab()
NiGreen1990O = cc.Green1990()
NiSproulGreen1991O = cc.SproulGreen1991()
NiSproulGreen1993O = cc.SproulGreen1993()
NiMisiakosTsamakisO = cc.MisiakosTsamakis()
NiKimmerleO = cc.Kimmerle()

n_i_MorinMaita_list = []
n_i_PutleyMitchell_list = []
n_i_Barber_list = []
n_i_Slotboom_list = []
n_i_Wasserab_list = []
n_i_Green1990_list = []
n_i_SproulGreen1991_list = []
n_i_SproulGreen1993_list = []
n_i_MisiakosTsamakis_list = []
n_i_Kimmerle_list = []

for T_sim in T_axis:
    n_i_MorinMaita = NiMorinMaitaO.n_i(T_sim)
    n_i_MorinMaita_list.append(n_i_MorinMaita * 1.0e-6)
    n_i_PutleyMitchell = NiPutleyMitchellO.n_i(T_sim)
    n_i_PutleyMitchell_list.append(n_i_PutleyMitchell * 1.0e-6)
    n_i_Barber = NiBarberO.n_i(T_sim)
    n_i_Barber_list.append(n_i_Barber * 1.0e-6)
    n_i_Slotboom = NiSlotboomO.n_i(T_sim)
    n_i_Slotboom_list.append(n_i_Slotboom * 1.0e-6)
    n_i_Wasserab = NiWasserabO.n_i(T_sim)
    n_i_Wasserab_list.append(n_i_Wasserab * 1.0e-6)
    n_i_Green1990 = NiGreen1990O.n_i(T_sim)
    n_i_Green1990_list.append(n_i_Green1990 * 1.0e-6)
    n_i_SproulGreen1991 = NiSproulGreen1991O.n_i(T_sim)
    n_i_SproulGreen1991_list.append(n_i_SproulGreen1991 * 1.0e-6)
    n_i_SproulGreen1993 = NiSproulGreen1993O.n_i(T_sim)
    n_i_SproulGreen1993_list.append(n_i_SproulGreen1993 * 1.0e-6)
    n_i_MisiakosTsamakis = NiMisiakosTsamakisO.n_i(T_sim)
    n_i_MisiakosTsamakis_list.append(n_i_MisiakosTsamakis * 1.0e-6)
    n_i_Kimmerle = NiKimmerleO.np(T_sim, N_D, N_A)[0]
    n_i_Kimmerle_list.append(n_i_Kimmerle * 1.0e-6)

#----------------------------------------------------------------------------- 
# plotting results:
fig1 = mpl_p.figure(1)
ax1 = fig1.add_subplot(111)
ax1.set_xlabel(r'Temperatur  $T / K$')
ax1.set_ylabel(r'Intrinsische Ladungsträgerdichte $n_i / \frac{1}{cm^3}$')
ax1.semilogy(NiMisiakosTsamakisO.T_MisiakosTsamakis, NiMisiakosTsamakisO.n_i_MisiakosTsamakis, 'ko', label=r'$n_{i, exp}$ Misiakos et al. (1993)')
ax1.semilogy(T_axis, n_i_MorinMaita_list, 'bs', label=r'$n_i$ Morin et al. (1954)')
ax1.semilogy(T_axis, n_i_PutleyMitchell_list, 'b*', label=r'$n_i$ Putley et al. (1958)')
ax1.semilogy(T_axis, n_i_Barber_list, 'b2', label=r'$n_i$ Barber (1967)')
ax1.semilogy(T_axis, n_i_Slotboom_list, 'b.', label=r'$n_i$ Slotboom (1976)')
ax1.semilogy(T_axis, n_i_Wasserab_list, 'b--', label=r'$n_i$ Wasserab (1977)')
ax1.semilogy(T_axis, n_i_Green1990_list, 'g.', label=r'$n_i$ Green (1990)')
ax1.semilogy(T_axis, n_i_SproulGreen1991_list, 'g--', label=r'$n_i$ Sproul et al. (1991)')
ax1.semilogy(T_axis, n_i_SproulGreen1993_list, 'g', label=r'$n_i$ Sproul et al. (1993)')
ax1.semilogy(T_axis, n_i_MisiakosTsamakis_list, 'b', label=r'$n_i$ Misiakos et al. (1993)')
ax1.semilogy(T_axis, n_i_Kimmerle_list, 'r.', label=r'$n_i$ Kimmerle (2011)')
ax1.legend()
mpl_p.ylim(1.0, 1.0e16)
mpl_p.xlim(100.0, 600.0)
mpl_p.show()
