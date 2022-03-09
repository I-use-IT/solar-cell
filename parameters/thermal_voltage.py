# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate thermal voltage U_T in V

Requires:   constants.py
"""

from constants import q_e, k_B_J
#==============================================================================

class ThermalVoltage:
    """
    Thermal voltage class
    """

    def u_t(self, T_sim):
        """
        Purpose:    Calculate thermal voltage U_T in V

        Model:      Standard definition

        Requires:   Elementary charge q_e in C
                    Botzmann constant k (herein k_B_J) in J/K

        Input:      Simulation temperature T_sim in K

        Output:     Thermal voltage U_T in V
        """

        U_T = k_B_J * T_sim / q_e

        return U_T
