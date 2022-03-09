# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Library of (physical) constants for project 'Solar Cell'

Requires:   -
"""

#==============================================================================

# physical constants
# data from "http://physics.nist.gov/cuu/index.html" with CODATA recommendation on the 2018 adjustment of the values of the constants
q_e = 1.602176634e-19       # Elementary charge q_e in C
                            # uncertainties:    exact
m_e = 9.1093837015e-31      # Electron mass m_e in kg
                            # uncertainties:    u(m_e) = 0.000 000 00028 e-31     u_r(m_e) = 3.0 e-10
h_P_J = 6.62607015e-34      # Planck constant h (herein h_P_J) in Js
                            # uncertainties:    exact
h_P = h_P_J/q_e             # Planck constant h (herein h_P) in eVs    
                            # uncertainties:    depends on machine epsilon        (exact value: 4.135 667 696 923 858 ... e-15)
k_B_J = 1.380649e-23        # Botzmann constant k (herein k_B_J) in J/K
                            # uncertainties:    exact
k_B = k_B_J/q_e             # Botzmann constant k (herein k_B) in eV/K
                            # uncertainties:    depends on machine epsilon        (exact value: 8.617 333 262 145 177 ... e-5)

# other conventions
T_STC = 273.15 + 25.0       # STC-temperature in K
U_Te_STC = k_B * T_STC      # STC-(thermal voltage * elementary charge) in eV
