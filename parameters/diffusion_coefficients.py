# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate diffusion coefficients Dn, Dp in cm^2/s

Requires:   mobilities.py (which itself uses carrier_concentrations.py (which itself uses constants.py and bandgap.py))
"""

from constants import k_B
import mobilities as mu
#==============================================================================

class D:
    """
    Diffusion coefficients class
    """

    N_D = 1e16
    N_A = 1e16

    # data from " Gerhard Fasching, Werkstoffe fuer die Elektrotechnik, p.271 "
    mue_n_300K_Fas = 1414.0 #Klaassen    #1450                       # cm^2/Vs
    mue_p_300K_Fas = 470.5  #Klaassen    #500                        # cm^2/Vs

    def dn_Fasching(self, T_list):
        """
        Calculates Dn_Fasching for T_axis data
        """

        Dn_Fasching = []
        for T_sim in T_list:
            self.Dn_Fas = k_B * (T_sim) * self.mue_n_300K_Fas
            Dn_Fasching.append(self.Dn_Fas)

        return Dn_Fasching



    def dp_Fasching(self, T_list):
        """
        Calculates Dp_Fasching for T_axis data
        """

        Dp_Fasching = []
        for T_sim in T_list:
            self.Dp_Fas = k_B * (T_sim) * self.mue_p_300K_Fas
            Dp_Fasching.append(self.Dp_Fas)

        return Dp_Fasching



    def mu_x(self, T_sim):
        """
        
        """

        MuObject = mu.Klaassen()
        self.mu_As_b_T_sim, self.mu_P_b_T_sim, self.mu_B_b_T_sim = MuObject.mu_i_bulk(T_sim, self.N_D, 1.)



    def dn_klaassen(self, T_list):
        """
        Calculates Dn_Klaassen for T_axis data
        """

        Dn_Klaassen = []
        for T_sim in T_list:
            self.mu_x(T_sim)
            self.Dn_Kla = k_B * (T_sim) * self.mu_P_b_T_sim*1.0e4
            Dn_Klaassen.append(self.Dn_Kla)

        return Dn_Klaassen


    
    def dp_klaassen(self, T_list):
        """
        Calculates Dp_Klaassen for T_axis data
        """

        Dp_Klaassen = []
        for T_sim in T_list:
            self.mu_x(T_sim)
            self.Dp_Kla = k_B * (T_sim) * self.mu_B_b_T_sim*1.0e4
            Dp_Klaassen.append(self.Dp_Kla)

        return Dp_Klaassen
