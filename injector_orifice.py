import math

#http://edge.rit.edu/edge/P18102/public/Engine%20Specifications/Propulsion/Injector/Injector
#Liquid Rocket Engine Injectors
#Good for range of temperatures and pressures of nitrus oxide with assumption of 2 phase liquid injected, Z is a bitch
#(255K, 2.533Mpa)-(283, 4.13Mpa)
#Z calulated by averaging a curve between .8 and .9 reduced temperature

def injector_orifice(m_dot_f, m_dot_o, f_rho, o_rho, f_temp, o_temp ,delta_p, injector_cd, f_number, o_number, pressure):
    #orifice_size(m_dot_f, injector_cd, delta_p, f_rho)
    two_phase_orifice(m_dot_o, injector_cd, delta_p, o_rho, pressure)


def two_phase_orifice(m_dot, cd, dp, rho, p):  # Imcompressable flow
    dp = p*dp
    pr = p/7270000
    z = -16.438*(pr**6)+44.625*(pr**5)-44.889*(pr**4)+20.313*(pr**3)-3.9608*(pr**2)-0.3575*pr+.9999
    area = ((m_dot)/(cd*z*math.sqrt(2*dp*rho)))*(39.67**2)/12
    diameter = math.sqrt(area*4/math.pi)
    print(diameter)