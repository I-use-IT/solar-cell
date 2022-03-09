# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate deviation of chemical potential from the bandgap center mu, mu_m_const in eV

Requires:   constants.py
            effective_masses.py (which itself uses bandgap.py)
"""

from constants import k_B
import effective_masses as em
import math as m
#==============================================================================

class ChemicalPotential:
    """
    Chemical potential class
    """

    m_e_ast = 1.09  #Green JAP67, 1990              #1.08
    m_h_ast = 1.15                                  #0.56



    def m_ast(self, T_sim):
        """
        Purpose:    Calculate temperature dependent effective carrier masses m_c_ast, m_v_ast

        Model:      Green (1990)

        Requires:   effective_masses.py (which itself uses bandgap.py)

        Input:      Simulation temperature T_sim in K

        Output:     Effective carrier masses m_c_ast, m_v_ast in multiplicative partivas of the free electron rest mass in 1
        """

        m_O = em.EffectiveMasses()
        self.m_c_ast = m_O.m_x(T_sim)[0]
        self.m_v_ast = m_O.m_x(T_sim)[1]



    def mu(self, T_sim):
        """
        Purpose:    Calculate deviation of chemical potential from the bandgap center mu, mu_m_const

        Model:      Standard definition

        Requires:   Parameters from class ChemicalPotential
                    Botzmann constant k (herein k_B) in eV/K

        Input:      Simulation temperature T_sim in K

        Output:     Deviation of chemical potential from the bandgap center mu, mu_m_const in eV
        """

        self.m_ast(T_sim)
        mu = 3./4. * k_B * T_sim * m.log(self.m_v_ast / self.m_c_ast)
        mu_m_const = 3./4. * k_B * T_sim * m.log(self.m_h_ast / self.m_e_ast)

        return mu, mu_m_const
