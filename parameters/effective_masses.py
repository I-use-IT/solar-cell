# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate effective carrier masses m_c, m_v in multiplicative partivas of the free electron rest mass in 1

Requires:   bandgap.py
"""

import bandgap as bg
#==============================================================================

class EffectiveMasses:
    """
    Effective masses class
    """

    # experimental data and parameters from "M. A. Green: Intrinsic concentration, effective density of states, and effective mass in silicon (1990)"
    T_Green = (4.2, 50., 100., 150., 200., 250., 300., 350., 400., 450., 500.)
    m_c_Green = (1.06, 1.06, 1.06, 1.07, 1.08, 1.08, 1.09, 1.1, 1.11, 1.12, 1.13)
    m_v_Green = (0.59, 0.69, 0.83, 0.95, 1.03, 1.1, 1.15, 1.19, 1.23, 1.29, 1.29)

    m_lc__4K = 0.9163
    m_tc__4K = 0.1905
    a = 0.4435870
    b = 0.3609528e-2        # K**(-1)
    c = 0.1173515e-3        # K**(-2)
    d = 0.1263218e-5        # K**(-3)
    e = 0.3025581e-8        # K**(-4)
    f = 0.4683382e-2        # K**(-1)
    g = 0.2286895e-3        # K**(-2)
    h = 0.7469271e-6        # K**(-3)
    i = 0.1727481e-8        # K**(-4)



    def m_x(self, T_sim):
        """
        Purpose:    Calculate effective carrier masses m_c, m_v

        Model:      Green (1990)

        Requires:   Parameters from class EffectiveMasses
                    bandgap.py

        Input:      Simulation temperature T_sim in K

        Output:     Effective carrier masses m_c, m_v in multiplicative partivas of the free electron rest mass in 1
        """

        E_g_O = bg.Eg()
        E_g_Paessler2002 = E_g_O.eg_models(T_sim)[-1]
        m_c = (36 * self.m_lc__4K * (E_g_O.E_g_0K_Pae2002 / E_g_Paessler2002 * self.m_tc__4K)**2)**(1./3)
        m_v = ((self.a + self.b * T_sim + self.c * T_sim**2 + self.d * T_sim**3 + self.e * T_sim**4) / (1 + self.f * T_sim + self.g * T_sim**2 + self.h * T_sim**3 + self.i * T_sim**4))**(2./3)

        return m_c, m_v
