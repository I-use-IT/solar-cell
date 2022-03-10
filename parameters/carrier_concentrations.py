# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate intrinsic carrier concentration n_i, electron n and hole concentration p with different models in m^-3

Requires:   constants.py
            bandgap.py
"""

from constants import q_e, k_B_J, k_B
import bandgap as bg
import math as m
from numpy import exp, log
#==============================================================================

class MisiakosTsamakis:
    """Konstantinos Misiakos and Dimitris Tsamakis 1993 model
    Ref.: Accurate measurements of the silicon intrinsic carrier density from 78 to 340K (1993), JAP 74, 3293...3297
    
    Sufficient accuracy from 78...340K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    T_MisiakosTsamakis = (77.8, 100.0, 120.75, 137.5, 148.4, 169.7, 195.0, 199.5, 213.0, 239.0, 256.5, 270.6, 281.0, 300.0, 319.5, 340.5)
    n_i_MisiakosTsamakis = (5.0e-20, 2.0e-11, 3.4e-6, 4.6e-3, 0.21, 84, 1.78e4, 4.3e4, 4.16e5, 1.92e7, 1.45e8, 6.7e8, 1.79e9, 9.7e9, 4.51e10, 1.89e11)



    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Misiakos and Tsamakis' 1993 model in m^3
        """

        n_i = 5.29e25 * (T_sim / 300)**2.54 * m.exp(-6726 / T_sim)

        return n_i



class MorinMaita:
    """F. J. Morin and J. P. Maita 1954 model
    Ref.: Electrical Properties of Silicon Containing Arsenic and Boron (1954), Physical Review 96, 28...35
    
    Sufficient accuracy from 0..700K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Morin and Maita' 1954 model in m^3
        """

        n_i = m.sqrt(1.5e33 * T_sim**3 * m.exp(-1.21 / (k_B * T_sim))) * 1.0e6

        return n_i



class PutleyMitchell:
    """E. H. Putley and W. H. Mitchell 1958 model
    Ref.: The Electrical Conductivity and Hall Effect of Silicon (1958), Proc. Phys. Soc. 72, 193...200
    
    Sufficient accuracy from 350..500K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Putley and Mitchel' 1958 model in m^3
        """

        n_i = 3.0e22 * T_sim**1.5 * m.exp(-0.603 / (k_B * T_sim))

        return n_i



class Barber:
    """H. D. Barber 1967 model
    Ref.:EFFECTIVE MASS AND INTRINSIC CONCENTRATION IN SILICON (1967), SSE 10, 1039...1051
    
    Sufficient accuracy from 230...700K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Barber' 1967 model in m^3
        """

        n_i = 1.72e22 * T_sim**1.5 * m.exp(-0.6025 / (k_B * T_sim))

        return n_i



class Slotboom:
    """J. W. Slotboom 1977 model
    Ref.: THE pn-PRODUCT IN SILICON (1977), SSE 20, 279...283
    
    Sufficient accuracy from 280...450K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Slotboom' 1977 model in m^3
        """

        n_i = m.sqrt(9.61e32 * T_sim**3 * m.exp(-1.206 / (k_B * T_sim))) * 1.0e6

        return n_i



class Wasserab:
    """Wasserab 1977 model
    Ref.: Die Temperaturabhaengigkeit der elektronischen Kenngroeszen des eigenleitenden Siliciums (1977), Z. Naturforsch. Teil A 32, 746...749
    
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Wasserab' 1977 model in m^3
        """

        n_i = 5.71e25 * (T_sim / 300)**2.365 * m.exp(-6733 / T_sim)

        return n_i



class Green1990:
    """Martin. A. Green 1990 model
    Ref.: Intrinsic concentration, effective density of states, and effective mass in silicon (1990), JAP 67, 2944...2954
    
    Sufficient accuracy from 200...500K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    uses: bandgap.py
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Green' 1990 model in m^3
        uses: bandgap.py
        """

        self.e_g(T_sim)
        N_c = 2.86e25 * (T_sim / 300.0)**1.58
        N_v = 3.1e25 * (T_sim / 300.0)**1.85
        n_i = m.sqrt( N_c * N_v * m.exp(-self.E_g_Green / (k_B * T_sim)))

        return n_i



    def e_g(self, T_sim):
        """
        Calls module 'bandgap.py' with *args 'T_sim' and calculates bandgap with 'Green' 1990 model in eV
        uses: bandgap.py
        """
        bgO = bg.Eg()
        self.E_g_Green = bgO.eg_models(T_sim)[5]



class SproulGreen1991:
    """A. B. Sproul and M. A. Green 1991 model
    Ref.: Improved value for the silicon intrinsic carrier concentration from 275 to 375K (1991), JAP 70, 846...854
    
    Sufficient accuracy from 275...375K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Sproul and Green' 1991 model in m^3
        """

        n_i = 9.15e25 * (T_sim / 300)**2 * m.exp(-6880 / T_sim)

        return n_i



class SproulGreen1993:
    """A. B. Sproul and M. A. Green 1993 model
    Ref.: Intrinsic carrier concentration and minority-carrier mobility of silicon from 77 to 300K (1993), JAP 73, 1214...1225
    
    Sufficient accuracy from 77...400K
    Call method 'n_i' with *args 'T_sim' to calculate intrinsic carrier concentration in m^3
    uses: bandgap.py
    """

    def n_i(self, T_sim):
        """
        Calculate intrinsic carrier concentration with 'Sproul and Green' 1993 model in m^3
        uses: bandgap.py
        """

        self.e_g(T_sim)
        n_i = 1.64e21 * T_sim**1.706 * m.exp(-self.E_g_Green / (2.0 * k_B * T_sim))

        return n_i



    def e_g(self, T_sim):
        """
        Calls module 'bandgap.py' with *args 'T_sim' and calculates bandgap with 'Green' 1990 model in eV
        uses: bandgap.py
        """

        bgO = bg.Eg()
        self.E_g_Green = bgO.eg_models(T_sim)[5]



class Kimmerle:
    """Kimmerle 2011 model
    Ref.: Herstellung und Charakterisierung hochohmiger Emitter fuer Hocheffizienzsolarzellen (2011), thesis
    
    Call method 'np' with *args 'T_sim, N_D, N_A' to calculate intrinsic, electron and hole carrier concentration in m^3
    input of N_D and N_A in cm^-3
    output of n_i, n and p in m^-3
    """

    def n_i2_fermi(self, T_sim, N_D, N_A):
        """
        Calculate squared intrinsic carrier concentration with 'Kimmerle' 2011 model in cm^-3
        input of N_D and N_A in cm^-3
        output of n_i^2 in cm^-6
        """

        V_T = k_B_J * T_sim / q_e
        if N_D > N_A:
            n = N_D - N_A
        else:
            n = N_A - N_D

    # E_g_Green
        if T_sim < 170:
            A = 1.17                            # eV
            B = 1.059e-5                        # eV/K
            C = -6.05e-7                        # eV/K**2
        elif T_sim < 270:
            A = 1.1785                          # eV
            B = -9.025e-5                       # eV/K
            C = -3.05e-7                        # eV/K**2
        else:       # valid for T_sim < 415K
            A = 1.206                           # eV
            B = -2.73e-4                        # eV/K
            C = 0.0                             # eV/K**2
        E_g_Green = A + B * T_sim + C * T_sim**2.

    # n_i_0
        n_i_0 = 0.9688 * 1.64e15 * T_sim**1.706 * exp(-E_g_Green * 1.6022e-19 / (2. * 1.3806e-23 * T_sim)) # V_T))

    # N_C
        N_C = n_i_0 * (0.9477**1.5 * exp(E_g_Green / V_T))**0.5

    # Fermi_12_inverse
        f = (n / N_C)
        if f == 1.:
            D = -0.5
        else:
            D = log(f) / (1. - f**2.)
        Fermi_12_inverse = D + (3. * m.pi**0.5 * f / 4.)**(2./3.) / (1. + (0.24 + 1.08 * (3. * m.pi**0.5 * f / 4.)**(2./3.))**(-2))

    # BGN Schenk
        g_e = 12.
        g_h = 4.
        a_e = 0.5187
        a_h = 0.4813
        Ryex = 0.01655
        aex = 0.0000003719

        # Normalized carrier densities and temperature
        Vaex = aex**3.
        n_h = N_A * Vaex
        n_e = N_D * Vaex
        n_s = n_e + n_h
        n_p = a_e * n_e + a_h * n_h
        n_i = n_s
        t_0 = V_T / Ryex
        u = n_s**2. / t_0**3.

        # Parameters from Table 2, p. 3689
        b_e = 8.
        b_h = 1.
        c_e = 1.3346
        c_h = 1.2365
        d_e = 0.893
        d_h = 1.153
        P = 7. / 30.

        # Eq. (33)
        D_xc_h = -((4. * m.pi)**3. * n_s**2. * ((48. * n_h / (m.pi * g_h))**(1./3.) + c_h * log(1. + d_h * n_p**P)) + 8. * m.pi * a_h / g_h * n_h * t_0**2. + (8. * m.pi * n_s)**0.5 * t_0**2.5) / ((4. * m.pi)**3. * n_s**2. + t_0**3. + b_h * n_s**0.5 * t_0**2. + 40. * n_s**1.5 * t_0)
        D_xc_e = -((4. * m.pi)**3. * n_s**2. * ((48. * n_e / (m.pi * g_e))**(1./3.) + c_e * log(1. + d_e * n_p**P)) + 8. * m.pi * a_e / g_e * n_e * t_0**2. + (8. * m.pi * n_s)**0.5 * t_0**2.5) / ((4. * m.pi)**3. * n_s**2. + t_0**3. + b_e * n_s**0.5 * t_0**2. + 40. * n_s**1.5 * t_0)

        # Parameters from Table 3, p. 3690
        h_e = 3.91
        h_h = 4.2
        j_e = 2.8585
        j_h = 2.9307
        k_e = 0.012
        k_h = 0.19
        Q_e = 0.75
        Q_h = 0.25

        # Eq. (37)
        D_i_h = -n_i * (1. + u) / ((t_0 * n_s / (2. * m.pi))**0.5 * (1. + h_h * log(1. + n_s**0.5 / t_0)) + j_h * u * n_p**0.75 * (1. + k_h * n_p**Q_h))
        D_i_e = -n_i * (1. + u) / ((t_0 * n_s / (2. * m.pi))**0.5 * (1. + h_e * log(1. + n_s**0.5 / t_0)) + j_e * u * n_p**0.75 * (1. + k_e * n_p**Q_e))

        dE_C_Schenk = -Ryex * (D_xc_e + D_i_e)
        dE_V_Schenk = -Ryex * (D_xc_h + D_i_h)
        dE_C = dE_C_Schenk / V_T
        dE_V = dE_V_Schenk / V_T

    # boltzmannconduction
        bc = exp(Fermi_12_inverse - dE_C)

    # n_i2_Fermi
        n_i2 = n_i_0**2. * f * exp(dE_V) / bc

        return n_i2



    def np(self, T_sim, N_D, N_A):
        """
        Calculate electron and hole concentration with 'Kimmerle' 2011 model in m^-3
        input of N_D and N_A in cm^-3
        output of n_i, n and p in m^-3
        """

        n_i2 = self.n_i2_fermi(T_sim, N_D, N_A)

        if N_D > N_A:
            n = N_D - N_A
            p = n_i2 / n
        else:
            p = N_A - N_D
            n = n_i2 / p

        n_i = n_i2**0.5 * 1.0e6
        n = n * 1.0e6
        p = p * 1.0e6

        return n_i, n, p
