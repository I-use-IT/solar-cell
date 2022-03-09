# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate bandgap E_g with different models in eV

Requires:   -
"""

import math as m
#==============================================================================

class Eg:
    """
    Bandgap class
    """
    
    # experimental data from "G. G. Mac Farlane et al.: Fine Structure in the Absorption-Edge Spectrum of Si (1958)"
    T_MacFarlane = (4.2, 20., 77., 90., 112., 170., 195., 249., 291., 363., 415.)
    E_g_MacFarlane = (1.1658, 1.1658, 1.1632, 1.1622, 1.1594, 1.1507, 1.1455, 1.1337, 1.1235, 1.103, 1.089)
    
    # experimental data from "M. A. Green: Intrinsic concentration, effective density of states, and effective mass in silicon (1990)"
    # values for 50...300K are obtained from "W. Bludau et. al.: Temperature dependence of the band gap of silicon (1974)"
    T_Green = (4.2, 50., 100., 150., 200., 250., 300., 350., 400., 450., 500.)
    E_g_Green = (1.17, 1.169, 1.1649, 1.1579, 1.1483, 1.1367, 1.1242, 1.1104, 1.0968, 1.0832, 1.0695)

    # original parameters for Varshni model
    # from "Y. P. Varshni: TEMPERATURE DEPENDENCE OF THE ENERGY GAP IN SEMICONDUCTORS (1967)"
    E_g_0K_Var = 1.1557                         # eV
    alpha_Var = 7.021e-4                        # eV/K
    beta_Var = 1108                             # K

    # modified parameters for Varshni model
    # from "Sentaurus Device User Guide C-2009.06"
    E_g_0K_Var_mod = 1.1696                     # eV
    alpha_Var_mod = 4.73e-4                     # eV/K
    beta_Var_mod = 636                          # K

    # original parameters for  W. Bludau et. al. model
    # from "W. Bludau et al.: Temperature dependence of the band gap of silicon (1974)"
    E_g_0K_Blu_1 = 1.17                         # eV
    A_Blu_1 = 1.059e-5                          # eV/K
    B_Blu_1 = -6.05e-7                          # eV/K**2
    E_g_0K_Blu_2 = 1.1785                       # eV
    A_Blu_2 = -9.025e-5                         # eV/K
    B_Blu_2 = -3.05e-7                          # eV/K**2

    # original parameters for Gaensslen model
    # from "http://www.iue.tuwien.ac.at/phd/palankovski/node37.html"
    E_g_0K_Gae = 1.1785                         # eV
    E_1_Gae = -0.02708                          # eV
    E_2_Gae = -0.02745                          # eV

    # original parameters for Green model
    # from ""
    A_Gre_1 = 1.17                              # eV
    B_Gre_1 = 1.059e-5                          # eV/K
    C_Gre_1 = -6.05e-7                          # eV/K**2
    A_Gre_2 = 1.1785                            # eV
    B_Gre_2 = -9.025e-5                         # eV/K
    C_Gre_2 = -3.05e-7                          # eV/K**2
    A_Gre_3 = 1.206                             # eV
    B_Gre_3 = -2.73e-4                          # eV/K
    C_Gre_3 = 0.                                # eV/K**2

    # modified parameters for Green model 
    # from "http://www.iue.tuwien.ac.at/phd/palankovski/node37.html"
    E_g_0K_Gre = 1.17                           # eV
    E_1_Gre = 0.00572                           # eV
    E_2_Gre = -0.06948                          # eV
    E_3_Gre = 0.018                             # eV

    # original parameters for Paessler model
    # from "R. Paessler: Parameter Sets Due to Fittings of Temperature Dependencies of Fundamental Bandgaps in Semiconductors (1999)"
    E_g_0K_Pae1999 = 1.17                           # eV
    alpha_Pae1999 = 0.318e-3                        # eV/K
    theta_p_Pae1999 = 406                           # K
    p_Pae1999 = 2.33                                # -

    # original parameters for Paessler model
    # from "R. Paessler: Dispersion-related description of temperature dependencies of band gaps in semiconductors (2002)" 
    E_g_0K_Pae2002 = 1.17                           # eV
    alpha_Pae2002 = 0.323e-3                        # eV/K
    delta_Pae2002 = 0.51                            # -
    theta_Pae2002 = 446                             # K

    # more modified parameters of some models are existent.
    # e.g. "http://www.iue.tuwien.ac.at/phd/palankovski/node37.html"



    def eg_models(self, T_sim):
        """
        Calculate bandgap E_g for one temperature with different models
        
        Model:      various

        Requires:   Parameters from class Eg

        Input:      Simulation temperature T_sim in K

        Output:     Bandgap E_g in eV
        """

        # Bardeen and Shockley (1950)
        E_g_BarSho = 1.184 - 3.0e-4 * T_sim      # 1.184 = E_g(0 K) not defined in original paper -> self defined!

        # Varshni (1967) with original parameters
        E_g_Var = self.E_g_0K_Var - ((self.alpha_Var * T_sim ** 2) / (self.beta_Var + T_sim))

        # Varshni (1967) with modified parameters
        E_g_Var_mod = self.E_g_0K_Var_mod - ((self.alpha_Var_mod * T_sim ** 2) / (self.beta_Var_mod + T_sim))

        # Bludau et. al. (1974) with original parameters
        if T_sim < 170.0:
            E_g_Blu = self.E_g_0K_Blu_1 + self.A_Blu_1 * T_sim + self.B_Blu_1 * T_sim ** 2
        else:       # valid for T_sim < 300K
            E_g_Blu = self.E_g_0K_Blu_2 + self.A_Blu_2 * T_sim + self.B_Blu_2 * T_sim ** 2

        # Gaensslen (1976-79)
        E_g_Gae = self.E_g_0K_Gae + self.E_1_Gae * (T_sim / 300.) + self.E_2_Gae * ((T_sim / 300.) ** 2)

        # Green (1990) with original parameters
        if T_sim < 170.0:
            E_g_Gre = self.A_Gre_1 + self.B_Gre_1 * T_sim + self.C_Gre_1 * T_sim ** 2.
        elif T_sim < 275.0:
            E_g_Gre = self.A_Gre_2 + self.B_Gre_2 * T_sim + self.C_Gre_2 * T_sim ** 2.
        else:       # valid for T_sim < 415K
            E_g_Gre = self.A_Gre_3 + self.B_Gre_3 * T_sim + self.C_Gre_3 * T_sim ** 2.

        # Green (1990) with modified parameters
        E_g_Gre_mod = self.E_g_0K_Gre + self.E_1_Gre * (T_sim / 300.) + self.E_2_Gre * ((T_sim / 300.) ** 2) + self.E_3_Gre * ((T_sim / 300.) ** 3)

        # Paessler (1999) with original parameters
        E_g_Pae1999 = self.E_g_0K_Pae1999 - ((self.alpha_Pae1999 * self.theta_p_Pae1999 / 2.) * ((1. + (2. * T_sim / self.theta_p_Pae1999) ** self.p_Pae1999) ** (1. / self.p_Pae1999) -1.))

        # Paessler (2002) with original parameters
        E_g_Pae2002 = self.E_g_0K_Pae2002 - self.alpha_Pae2002 * self.theta_Pae2002 * ((1 - 3 * self.delta_Pae2002**2) / (m.exp(self.theta_Pae2002 / T_sim) - 1) + 1.5 * self.delta_Pae2002**2 * ((1 + m.pi**2 / (3 + 3 * self.delta_Pae2002**2) * (2 * T_sim / self.theta_Pae2002)**2 + (0.75 * self.delta_Pae2002**2 - 0.25) * (2 * T_sim / self.theta_Pae2002)**3 + 8. / 3. * (2 * T_sim / self.theta_Pae2002)**4 + (2 * T_sim / self.theta_Pae2002)**6)**(1./6.) - 1))

        return E_g_BarSho, E_g_Var, E_g_Var_mod, E_g_Blu, E_g_Gae, E_g_Gre, E_g_Gre_mod, E_g_Pae1999, E_g_Pae2002 



    def eg_lists(self, T_list):
        """
        Calculate bandgap lists E_g_list for temperature list with different models
        """

        E_g_BarSho_list = []
        E_g_Var_list = []
        E_g_Var_mod_list = []
        E_g_Blu_list = []
        E_g_Gae_list = []
        E_g_Gre_list = []
        E_g_Gre_mod_list = []
        E_g_Pae1999_list = []
        E_g_Pae2002_list = []

        for T_sim in T_list:
            E_g_BarSho, E_g_Var, E_g_Var_mod, E_g_Blu, E_g_Gae, E_g_Gre, E_g_Gre_mod, E_g_Pae1999, E_g_Pae2002 = self.eg_models(T_sim)
            E_g_BarSho_list.append(E_g_BarSho)
            E_g_Var_list.append(E_g_Var)
            E_g_Var_mod_list.append(E_g_Var_mod)
            E_g_Blu_list.append(E_g_Blu)
            E_g_Gae_list.append(E_g_Gae)
            E_g_Gre_list.append(E_g_Gre)
            E_g_Gre_mod_list.append(E_g_Gre_mod)
            E_g_Pae1999_list.append(E_g_Pae1999)
            E_g_Pae2002_list.append(E_g_Pae2002)

        return E_g_BarSho_list, E_g_Var_list, E_g_Var_mod_list, E_g_Blu_list, E_g_Gae_list, E_g_Gre_list, E_g_Gre_mod_list, E_g_Pae1999_list, E_g_Pae2002_list
