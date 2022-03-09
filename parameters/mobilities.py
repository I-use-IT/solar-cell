# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate carrier mobilities mu_As_b, mu_P_b, mu_B_b in m^2/Vs

Requires:   carrier_concentrations.py (which itself uses constants.py and bandgap.py)
"""

import carrier_concentrations as cc
#==============================================================================

class Klaassen:
    """D. B. M. Klaassen (Philips) 1992 model
    Ref.: A UNIFIED MOBILITY MODEL FOR DEVICE SIMULATION I + II (1992), SSE Vol. 35, 953...967

    Sufficient accuracy from 50...500K
    Call method 'mu_i_bulk' with *args 'T_sim, N_D, N_A' to calculate total bulk mobility in m^2/Vs

    GENERAL NOTE
    i takes value 'e(lectrons)' from As & P or 'h(oles)' from B   
    I takes value 'D(onor)' from As & P or 'A(cceptor)' from B
    """

# experimental data on majority e & h mobilities as functions of impurity concentrations N @ 300K         p954    table 1
    mu_max_As_300K = 1417.0e-4          # m^2/Vs
    mu_max_P_300K = 1414.0e-4           # m^2/Vs
    mu_max_B_300K = 470.5e-4            # m^2/Vs
    mu_min_As_300K = 52.2e-4            # m^2/Vs
    mu_min_P_300K = 68.5e-4             # m^2/Vs
    mu_min_B_300K = 44.9e-4             # m^2/Vs
    #mu_1_As = 43.4e-4                   # m^2/Vs
    #mu_1_P = 56.1e-4                    # m^2/Vs
    #mu_1_B = 29.0e-4                    # m^2/Vs
    N_ref_1_As = 9.68e22                # m^-3
    N_ref_1_P = 9.2e22                  # m^-3
    N_ref_1_B = 2.23e23                 # m^-3
    #N_ref_2_As = 3.43e26                # m^-3
    #N_ref_2_P = 3.41e26                 # m^-3
    #N_ref_2_B = 6.1e26                  # m^-3
    alpha_1_As = 0.68                   # 1
    alpha_1_P = 0.711                   # 1
    alpha_1_B = 0.719                   # 1
    #alpha_2_As = 2.                     # 1
    #alpha_2_P = 1.98                    # 1
    #alpha_2_B = 2.                      # 1
# determined parameters (from figure 1 & 2) for majority e & h mobilities         p962
    theta_e = 2.285                     # 1
    theta_h = 2.247                     # 1
# P_i(N_I,c)-function: determined optimal parameter set         p957
    f_CW = 2.459                        # 1
    f_BH = 3.828                        # 1
# normalized effective masses m_x/m_0
    m_e = 1.                            # 1
    m_h = 1.258                         # 1
# G(P)          p955    table 2
    s1 = 0.89233                        # 1
    s2 = 0.41372                        # 1
    s3 = 0.19778                        # 1
    s4 = 0.28227                        # 1
    s5 = 0.005978                       # 1
    s6 = 1.80618                        # 1
    s7 = 0.72169                        # 1
# F(P)          p955    table 2
    r1 = 0.7643                         # 1
    r2 = 2.2999                         # 1
    r3 = 6.5502                         # 1
    r4 = 2.367                          # 1
    r5 = -0.01552                        # 1    r5(Sentaurus) = -0.8552    r5(Klaassen) = -0.01552
    r6 = 0.6478                         # 1
# Z_I(N_I)  ultra high concentration effects --> "clustering" function      p956
# As & P
    c_D = 0.21                          # 1
    N_ref_D = 4.0e26                    # m^-3
# B
    c_A = 0.5                           # 1
    N_ref_A = 7.2e26                    # m^-3

# polynomial fit für G_min and P_min (see Mobilitaet.xls)
# P_min=sum(q_i*(T/m)^i)
    q1 = 0.0922                         # 1
    q2 = 0.3553                         # 1
    q3 = -0.1927                        # 1
    q4 = 0.0847                         # 1
    q5 = -0.0148                        # 1
# G_min=sum(k_i*(T/m)^i)
    k1 = -0.036                         # 1
    k2 = 0.222                          # 1
    k3 = -0.1321                        # 1
    k4 = 0.0533                         # 1
    k5 = -0.0089                        # 1



    def mu_i_L(self, T_sim):
        """
        Calculate lattice mobility with 'Klaassen (Philips)' 1992 model (II eqn 1) in m^2/Vs
        """

        mu_As_L = self.mu_max_As_300K * (300. / T_sim)**self.theta_e
        mu_P_L = self.mu_max_P_300K * (300. / T_sim)**self.theta_e
        mu_B_L = self.mu_max_B_300K * (300. / T_sim)**self.theta_h

        return mu_As_L, mu_P_L, mu_B_L



    def mu_i_DAj(self, T_sim, N_Ds, N_As, n, p, c):
        """
        Calculate mobility in dependence of all other bulk scattering mechanisms with 'Klaassen (Philips)' 1992 model in m^2/Vs
        """

    # Z_I(N_I) in 1: clustering function (I eqn 14)
        Z_D__N_I = 1. + (1. / (self.c_D + (self.N_ref_D / N_Ds)**2.))    # = Z_As__N_I = Z_P__N_I
        Z_A__N_I = 1. + (1. / (self.c_A + (self.N_ref_A / N_As)**2.))    # = Z_B__N_I

    # N_I in m^-3: carrier concentrations (I eqn 15)
        N_D = Z_D__N_I * N_Ds
        N_A = Z_A__N_I * N_As

    # N_(i,sc) in m^-3: two body scattering density (I eqn 18)
        # Sentaurus
        N_e_sc = N_Ds + N_As + p
        N_h_sc = N_Ds + N_As + n
        #======================================================================
        # # Klaassen:
        # N_e_sc = N_D + N_A + p
        # N_h_sc = N_D + N_A + n
        #======================================================================

    # P_i(N_I,c)-function (I eqn 16, A3, 8, comment p957 top)
        P_CW_e = 3.97e17 * ((T_sim / 300.)**3. / (Z_D__N_I**3. * N_e_sc))**(2./3.)
        P_CW_h = 3.97e17 * ((T_sim / 300.)**3. / (Z_A__N_I**3. * N_h_sc))**(2./3.)

        P_BH_e = (1.36e26 / c) * self.m_e * (T_sim / 300.)**2.
        P_BH_h = (1.36e26 / c) * self.m_h * (T_sim / 300.)**2.

        P_e = 1. / (self.f_CW / P_CW_e + self.f_BH / P_BH_e)
        P_h = 1. / (self.f_CW / P_CW_h + self.f_BH / P_BH_h)

    # F(P): electron hole scattering (I eqn 12)
        F__P_e = (self.r1 * P_e**self.r6 + self.r2 + self.r3 / self.m_h) / (P_e**self.r6 + self.r4 + self.r5 / self.m_h)
        F__P_h = (self.r1 * P_h**self.r6 + self.r2 + self.r3 * self.m_h) / (P_h**self.r6 + self.r4 + self.r5 * self.m_h)

    # extrapolation P-function for P < P_min (see Mobilitaet.xls by Achim Kimmerle)
        P_min_e = self.q1 + self.q2 * (T_sim / (300. * self.m_e)) + self.q3 * (T_sim / (300. * self.m_e))**2. + self.q4 * (T_sim / (300. * self.m_e))**3. + self.q5 * (T_sim / (300. * self.m_e))**4.
        P_min_h = self.q1 + self.q2 * (T_sim / (300. * self.m_h)) + self.q3 * (T_sim / (300. * self.m_h))**2. + self.q4 * (T_sim / (300. * self.m_h))**3. + self.q5 * (T_sim / (300. * self.m_h))**4.
        G_min_e = self.k1 + self.k2 * (T_sim / (300. * self.m_e)) + self.k3 * (T_sim / (300. * self.m_e))**2. + self.k4 * (T_sim / (300. * self.m_e))**3. + self.k5 * (T_sim / (300. * self.m_e))**4.
        G_min_h = self.k1 + self.k2 * (T_sim / (300. * self.m_h)) + self.k3 * (T_sim / (300. * self.m_h))**2. + self.k4 * (T_sim / (300. * self.m_h))**3. + self.k5 * (T_sim / (300. * self.m_h))**4.
        
    # G(P): minority impurity scattering (I eqn 9)
        if P_e < P_min_e:
            G__P_e = G_min_e
        else:
            G__P_e = 1. - self.s1 / (self.s2 + (T_sim / (300. * self.m_e))**self.s4 * P_e)**self.s3 + self.s5 / (((300. * self.m_e) / T_sim)**self.s7 * P_e)**self.s6

        if P_h < P_min_h:
            G__P_h = G_min_h
        else:
            G__P_h = 1. - self.s1 / (self.s2 + (T_sim / (300 * self.m_h))**self.s4 * P_h)**self.s3 + self.s5 / (((300. * self.m_h) / T_sim)**self.s7 * P_h)**self.s6

    # N_(i,sc,eff): effective two body scattering density (I eqn 21)
        N_e_sc_eff = N_D + G__P_e * N_A + p / F__P_e
        N_h_sc_eff = N_A + G__P_h * N_D + n / F__P_h  

    # majority impurity scattering including screening
    # mu_(i,N): (II eqn 2a)
        mu_As_N = self.mu_max_As_300K**2. * (T_sim / 300.)**(3. * self.alpha_1_As - 1.5) / (self.mu_max_As_300K - self.mu_min_As_300K)
        mu_P_N = self.mu_max_P_300K**2. * (T_sim / 300.)**(3. * self.alpha_1_P - 1.5) / (self.mu_max_P_300K - self.mu_min_P_300K)
        mu_B_N = self.mu_max_B_300K**2. * (T_sim / 300.)**(3. * self.alpha_1_B - 1.5) / (self.mu_max_B_300K - self.mu_min_B_300K)

    # mu_(i,c): (II eqn 2b)
        mu_As_c = self.mu_max_As_300K * self.mu_min_As_300K * (T_sim / 300.)**0.5 / (self.mu_max_As_300K - self.mu_min_As_300K)
        mu_P_c = self.mu_max_P_300K * self.mu_min_P_300K * (T_sim / 300.)**0.5 / (self.mu_max_P_300K - self.mu_min_P_300K)
        mu_B_c = self.mu_max_B_300K * self.mu_min_B_300K * (T_sim / 300.)**0.5 / (self.mu_max_B_300K - self.mu_min_B_300K)

    # mu_(i,D+A+j)__(N_D,N_A,n,p): (I eqn 20)
        mu_As_DAj = mu_As_N * (N_e_sc / N_e_sc_eff) * (self.N_ref_1_As / N_e_sc)**self.alpha_1_As + mu_As_c * (c / N_e_sc_eff)
        mu_P_DAj = mu_P_N * (N_e_sc / N_e_sc_eff) * (self.N_ref_1_P / N_e_sc)**self.alpha_1_P + mu_P_c * (c / N_e_sc_eff)
        mu_B_DAj = mu_B_N * (N_h_sc / N_h_sc_eff) * (self.N_ref_1_B / N_h_sc)**self.alpha_1_B + mu_B_c * (c / N_h_sc_eff)

        return  mu_As_DAj, mu_P_DAj, mu_B_DAj



    def mu_i_bulk(self, T_sim, N_D, N_A):
        """
        Calculate total bulk mobility with 'Klaassen (Philips)' 1992 model in m^2/Vs
        """

    # n_i2_Fermi, n, p    
        NiKimmerleO = cc.Kimmerle()
        """
        input of N_D and N_A in cm^-3.
        output of n_i, n and p in m^-3.
        """
        unused_n_i2, n, p = NiKimmerleO.np(T_sim, N_D, N_A)
        unused_n_i = unused_n_i2**0.5
        c = n + p

    # lattice mobility and mobility in dependence of all other bulk scattering mechanisms
        mu_As_L, mu_P_L, mu_B_L = self.mu_i_L(T_sim)
        mu_As_DAj, mu_P_DAj, mu_B_DAj = self.mu_i_DAj(T_sim, N_D*1.0e6, N_A*1.0e6, n, p, c)

    # total bulk mobility
        mu_As_b = 1. / ((1. / mu_As_L) + (1. / mu_As_DAj))
        mu_P_b = 1. / ((1. / mu_P_L) + (1. / mu_P_DAj))
        mu_B_b = 1. / ((1. / mu_B_L) + (1. / mu_B_DAj))

        return mu_As_b, mu_P_b, mu_B_b
