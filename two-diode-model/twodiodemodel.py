# -*- coding: utf-8 -*-
"""
Author:     Tobias Ried, 2022

Purpose:    Calculate current density-voltage characteristic J(U) in A/m**2 with two-diode-model
            Calculate power-voltage characteristic P(U)
            Calculate solar cell characteristics U_oc, J_sc, U_MPP, J_MPP, S_MPP, FF, eta

Requires:   constants.py
            bandgap.py
            effective_masses.py (which itself uses bandgap.py)
            mobilities.py (which itself uses carrier_concentrations.py (which itself uses constants.py and bandgap.py))
            diffusion_coefficients.py (which itself uses mobilities.py)
"""

from constants import q_e, h_P, k_B, T_STC, U_Te_STC
import bandgap as bg
import effective_masses as em
import mobilities as mu
import diffusion_coefficients as dc
import math as m
import numpy as np
import scipy.optimize as sp_o
#==============================================================================

class SiCell:
    """
    Silicon solar cell class
    """

    J_ph = -10.0e-20                    # A/m**2        -350.0
    accuracy = 1.0e-9                   # relative
    U_min = - 0.5                       # V
    U_max = 1.5                         # V

# typical Si-cell values:
    N_d = 1.0e12                        # m^-3
    N_a = 1.0e24                        # m^-3
    J_s1_typical = 1.0e-8               # A/m**2
    J_s2_typical = 1.0e-5               # A/m**2
    R_s_typical = 0.5e-4                # Ohm*m**2
    R_p_typical = 3000.0e-4             # Ohm*m**2
    E_g_STC = 1.12464597487             # eV (Paessler2002)
    m_c_eff_300 = 1.09                  # @ 300K
    m_v_eff_300 = 1.15                  # @ 300K
    W = 180e-6                          # m
    tau = 50.0e-6                       # s
    S = 6.0                             # m/s

# standard initial / fit values:
    T_ini = T_STC                       # K
    U_Te_T_ini = U_Te_STC               # eV
    J_s1_T_ini = J_s1_typical
    J_s2_T_ini = J_s2_typical
#    c_s1 = 0.0
#    c_s2 = 0.0
    E_g_T_ini = E_g_STC
    m_c_eff_T_ini = m_c_eff_300
    m_v_eff_T_ini = m_v_eff_300
    R_s = R_s_typical
    R_p = R_p_typical

# standard simulation values:
    T_sim = T_STC + 75.0
    U_Te_T_sim = k_B * T_sim

# standard fit options:
    fit_J_sx_on = 0
    fit_tau_on = 0

# standard active effects:
    J_sx_on = 0
    E_g_on = 0
    m_x_eff_on = 0
    D_x_on = 0
    mu_x_on = 0



    def set_values(self, J_ph, J_s1, J_s2, R_s, R_p, T_ini, T_sim):
        """
        
        """

#       set initial / fit values:
        self.J_ph = J_ph
        self.J_s1_T_ini = J_s1
        self.J_s2_T_ini = J_s2
        self.R_s = R_s
        self.R_p = R_p
        self.T_ini = T_ini
        self.U_Te_T_ini = k_B * T_ini
#       set simulation values:
        self.T_sim = T_sim
        self.U_Te_T_sim = k_B * T_sim



    def set_fit_options(self, fit_J_sx_on, fit_tau_on):
        """
        
        """

        self.fit_J_sx_on = bool(fit_J_sx_on)
        self.fit_tau_on = bool(fit_tau_on)



    def set_active_effects(self, J_sx_on, E_g_on, m_x_eff_on, D_x_on, mu_x_on):
        """
        
        """

        self.J_sx_on = bool(J_sx_on)
        self.E_g_on = bool(E_g_on)
        self.m_x_eff_on = bool(m_x_eff_on)
        self.D_x_on = bool(D_x_on)
        self.mu_x_on = bool(mu_x_on)
        self.activate_effects()



    def activate_effects(self):
        """
        
        """

        # call required methods:
        if self.E_g_on == False:
            self.e_g(self.T_ini, self.T_ini)    #self.E_g_T_sim = self.E_g_T_ini
        if self.E_g_on == True:
            self.e_g(self.T_ini, self.T_sim)
        if self.m_x_eff_on == True:
            self.m_x_eff(self.T_ini, self.T_sim)
        if self.D_x_on == True and self.mu_x_on == False:
            self.d_x(self.T_ini, self.T_sim)
        if self.mu_x_on == True:
            self.mu_x(self.T_ini, self.T_sim)
        self.j_sx()



    def e_g(self, T_ini, T_sim):
        """
        
        """

        E_g_O = bg.Eg()
        self.E_g_T_ini = E_g_O.eg_models(T_ini)[-1]     # [-1] = E_g_Paessler2002
        self.E_g_T_sim = E_g_O.eg_models(T_sim)[-1]



    def m_x_eff(self, T_ini, T_sim):
        """
        
        """

        m_x_eff_O = em.EffectiveMasses()
        self.m_c_eff_T_ini = m_x_eff_O.m_x(T_ini)[0]
        self.m_v_eff_T_ini = m_x_eff_O.m_x(T_ini)[1]
        self.m_c_eff_T_sim = m_x_eff_O.m_x(T_sim)[0]
        self.m_v_eff_T_sim = m_x_eff_O.m_x(T_sim)[1]



    def d_x(self, T_ini, T_sim):
        """
        
        """

        # data from "D. B. M. Klaassen, A UNIFIED MOBILITY MODEL FOR DEVICE SIMULATION I + II (1992), SSE Vol. 35, pp.953...967." 
        # or from "Gerhard Fasching, Werkstoffe fuer die Elektrotechnik (1994), p.271"
        mue_e_300K = 1414.0 * 1.0e-4    # Klaassen - Phosphorous    #1450.0 * 1.0e-4                     # m**2/Vs
        mue_h_300K = 470.5 * 1.0e-4     # Klaassen - Boron          #500.0 * 1.0e-4                      # m**2/Vs
        
        self.D_e_T_ini = k_B * T_ini * mue_e_300K
        self.D_h_T_ini = k_B * T_ini * mue_h_300K
        self.D_e_T_sim = k_B * T_sim * mue_e_300K
        self.D_h_T_sim = k_B * T_sim * mue_h_300K



    def mu_x(self, T_ini, T_sim):
        """
        
        """

        Mu_O = mu.Klaassen()
        self.mu_As_b_T_ini, self.mu_P_b_T_ini, self.mu_B_b_T_ini = Mu_O.mu_i_bulk(T_ini, self.N_d*1.0e-6, self.N_a*1.0e-6)
        self.mu_As_b_T_sim, self.mu_P_b_T_sim, self.mu_B_b_T_sim = Mu_O.mu_i_bulk(T_sim, self.N_d*1.0e-6, self.N_a*1.0e-6)



    def j_sx(self):
        """
        
        """

        if self.J_sx_on == False or self.T_sim == self.T_ini:
            self.J_s1 = self.J_s1_T_ini
            self.J_s2 = self.J_s2_T_ini
        if self.J_sx_on == True and self.D_x_on == False:
            c_s1 = self.J_s1_T_ini / (self.T_ini**3 * m.exp(-self.E_g_T_ini / self.U_Te_T_ini))
            c_s2 = self.J_s2_T_ini / (m.sqrt(self.T_ini**5) * m.exp(-self.E_g_T_ini / (2.0 * self.U_Te_T_ini)))
            self.J_s1 = c_s1 * self.T_sim**3 * m.exp(-self.E_g_T_sim / self.U_Te_T_sim)
            self.J_s2 = c_s2 * m.sqrt(self.T_sim**5) * m.exp(-self.E_g_T_sim / (2.0 * self.U_Te_T_sim))
        if self.J_sx_on == True and self.D_x_on == True and self.mu_x_on == False:
            c_s1 = self.J_s1_T_ini / (self.T_ini**3 * m.exp(-self.E_g_T_ini / self.U_Te_T_ini) * m.sqrt(self.D_e_T_ini / self.tau) * ((1 + m.sqrt(self.D_e_T_ini) * m.tanh(self.W / m.sqrt(self.D_e_T_ini * self.tau)) / (m.sqrt(self.tau) * self.S)) / (m.sqrt(self.D_e_T_ini)/(m.sqrt(self.tau) * self.S + m.tanh(self.W / m.sqrt(self.D_e_T_ini * self.tau))))))
            c_s2 = self.J_s2_T_ini / (m.sqrt(self.T_ini**5) * m.exp(-self.E_g_T_ini / (2.0 * self.U_Te_T_ini)))
            self.J_s1 = c_s1 * (self.T_sim**3 * m.exp(-self.E_g_T_sim / self.U_Te_T_sim) * m.sqrt(self.D_e_T_sim / self.tau) * ((1 + m.sqrt(self.D_e_T_sim) * m.tanh(self.W / m.sqrt(self.D_e_T_sim * self.tau)) / (m.sqrt(self.tau) * self.S)) / (m.sqrt(self.D_e_T_sim) / (m.sqrt(self.tau) * self.S + m.tanh(self.W / m.sqrt(self.D_e_T_sim * self.tau))))))
            self.J_s2 = c_s2 * m.sqrt(self.T_sim**5) * m.exp(-self.E_g_T_sim / (2.0 * self.U_Te_T_sim))
        if self.J_sx_on == True and self.D_x_on == True and self.mu_x_on == True:
            c_s1 = self.J_s1_T_ini / (self.T_ini**3 * m.exp(-self.E_g_T_ini / self.U_Te_T_ini) * m.sqrt(self.U_Te_T_ini * self.mu_As_b_T_ini / self.tau) * ((1 + m.sqrt(self.U_Te_T_ini * self.mu_As_b_T_ini) * m.tanh(self.W / m.sqrt(self.U_Te_T_ini * self.mu_As_b_T_ini * self.tau)) / (m.sqrt(self.tau) * self.S)) / (m.sqrt(self.U_Te_T_ini * self.mu_As_b_T_ini) / (m.sqrt(self.tau) * self.S + m.tanh(self.W / m.sqrt(self.U_Te_T_ini * self.mu_As_b_T_ini * self.tau))))))
            c_s2 = self.J_s2_T_ini / (m.sqrt(self.T_ini**5) * m.exp(-self.E_g_T_ini / (2.0 * self.U_Te_T_ini)))
            self.J_s1 = c_s1 * (self.T_sim**3 * m.exp(-self.E_g_T_sim / self.U_Te_T_sim) * m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim / self.tau) * ((1 + m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim) * m.tanh(self.W / m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim * self.tau)) / (m.sqrt(self.tau) * self.S)) / (m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim) / (m.sqrt(self.tau) * self.S + m.tanh(self.W / m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim * self.tau))))))
            self.J_s2 = c_s2 * m.sqrt(self.T_sim**5) * m.exp(-self.E_g_T_sim / (2.0 * self.U_Te_T_sim))
        if self.fit_J_sx_on == True and self.fit_tau_on == False:
            c_s1 = self.J_s1_T_ini / (self.T_ini**3 * m.exp(-self.E_g_T_ini / self.U_Te_T_ini))
            c_s2 = self.J_s2_T_ini / (m.sqrt(self.T_ini**5) * m.exp(-self.E_g_T_ini / (2.0 * self.U_Te_T_ini)))
            self.J_s1 = c_s1 * self.T_sim**3 * m.exp(-self.E_g_T_sim / self.U_Te_T_sim)
            self.J_s2 = c_s2 * m.sqrt(self.T_sim**5) * m.exp(-self.E_g_T_sim / (2.0 * self.U_Te_T_sim))
        if self.fit_J_sx_on == False and self.fit_tau_on == True:
            c_s1 = (32.0 * m.pi**3.0 * q_e * k_B**3) / (self.N_a * h_P**6.0)
            self.J_s1 = c_s1 * (self.T_sim**3 * (self.m_c_eff_T_sim * self.m_v_eff_T_sim)**1.5 * m.exp(-self.E_g_T_sim / self.U_Te_T_sim) * m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim / self.tau) * ((1 + m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim) * m.tanh(self.W / m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim * self.tau)) / (m.sqrt(self.tau) * self.S)) / (m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim) / (m.sqrt(self.tau) * self.S + m.tanh(self.W / m.sqrt(self.U_Te_T_sim * self.mu_As_b_T_sim * self.tau))))))
        if self.fit_tau_on == True and self.fit_J_sx_on == True:
            print('Make up your mind what parameters you want to fit!')



    def j_unbounded(self, U):
        """
        
        """

        return self.J_ph + self.J_s1 * (m.exp(U / self.U_Te_T_sim) - 1.0) + self.J_s2 * (m.exp(U / (2.0 * self.U_Te_T_sim)) - 1.0) + U / self.R_p 



    def dj_unbounded(self, U):
        """
        
        """

        return self.J_s1 / self.U_Te_T_sim * m.exp(U / self.U_Te_T_sim) + self.J_s2 / (2.0 * self.U_Te_T_sim) * m.exp(U / (2.0 * self.U_Te_T_sim)) + 1.0 / self.R_p



    def j_bounded(self, U):
        """
        
        """

        if U < self.U_min:
            return self.j_unbounded(self.U_min) + self.dj_unbounded(self.U_min) * (U - self.U_min) 
        elif U > self.U_max:
            return self.j_unbounded(self.U_max) + self.dj_unbounded(self.U_max) * (U - self.U_max) 
        else:
            return self.j_unbounded(U)



    def dj_bounded(self, U):
        """
        
        """

        if U < self.U_min:
            return self.dj_unbounded(self.U_min)
        elif U > self.U_max:
            return self.dj_unbounded(self.U_max)
        else:
            return self.dj_unbounded(U)



    def j(self, U):
        """
        
        """

        if self.R_s == 0.0:
            return self.j_bounded(U)
        U_R_s = self.j_bounded(U) * self.R_s
        J = U_R_s / self.R_s
        Ji = self.j_bounded(U - U_R_s) - J
        while (abs(Ji / J) > self.accuracy):
            deriv = -self.dj_bounded(U - U_R_s) - 1.0 / self.R_s
            U_R_s -= Ji / deriv
            J = U_R_s / self.R_s
            Ji = self.j_bounded(U - U_R_s) - U_R_s / self.R_s

        return J



    def dj(self, U):
        """
        
        """

        J = self.j(U)
        J_s1_ = 1.0 / self.U_Te_T_sim * self.J_s1 * m.exp((U - J * self.R_s) / self.U_Te_T_sim)
        J_s2_ = 0.5 / self.U_Te_T_sim * self.J_s2 * m.exp((U - J * self.R_s) / (2.0 * self.U_Te_T_sim))

        return (J_s1_ + J_s2_ + 1.0 / self.R_p) / (1.0 + self.R_s / self.R_p + self.R_s * J_s1_ + self.R_s * J_s2_)



    def p(self,U):
        """
        
        """

        return U * self.j(U)



    def dp(self,U):
        """
        
        """

        return self.j(U) + U * self.dj(U)



    def u_oc(self):
        """
        
        """

        U_oc = sp_o.fsolve(self.j, 0.62)

        return U_oc



    def j_sc(self):
        """
        
        """

        return self.j(0)



    def mpp(self):
        """
        
        """

        U_MPP = sp_o.fsolve(self.dp, 0.5)
        J_MPP = self.j(U_MPP)
        S_MPP = U_MPP * J_MPP

        return U_MPP, J_MPP, S_MPP



#==============================================================================
# for your convenience
    def characteristics(self):
        """
        
        """

        U_oc = self.u_oc()
        J_sc = self.j(0)
        U_MPP, J_MPP, S_MPP = self.mpp()
        FF = S_MPP / (U_oc * J_sc) * 100
        eta = U_MPP * J_MPP / 1000.0            # only valid @ STC conditions

        return np.array([U_oc, J_sc, U_MPP, J_MPP, S_MPP, FF, eta])



    def j_u_curve(self, U_list):
        """
        
        """

        J_list = []
        for U in U_list:
            J_list.append(self.j(U))

        return np.array(J_list)



    def p_u_curve(self, U_list):
        """
        
        """

        P_list = []
        for U in U_list:
            P_list.append(self.p(U))

        return np.array(P_list)
