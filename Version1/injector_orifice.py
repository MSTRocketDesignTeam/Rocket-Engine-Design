import math
import numpy as np
from matplotlib import pyplot as plt

#http://edge.rit.edu/edge/P18102/public/Engine%20Specifications/Propulsion/Injector/Injector
#Liquid Rocket Engine Injectors
#Good for range of temperatures and pressures of nitrus oxide with assumption of 2 phase liquid injected, Z is a bitch
#(255K, 2.533Mpa)-(283, 4.13Mpa)
#Z calulated by averaging a curve between .8 and .9 reduced temperature

def injector_orifice(m_dot_f, m_dot_o, f_rho, o_rho, f_temp, o_temp , cha_press, cha_d, delta_p, rows, initial, mult, o_num, f_num, cd, inj_class):
    o_a, o_d = two_phase_orifice(m_dot_o, cd, delta_p, o_rho, cha_press)
    f_a, f_d = incompressible_orifice(m_dot_f, cd, delta_p, f_rho, cha_press)
    print(f_d)
    print(o_d)

    injector_rows(cha_d, rows, initial, mult, inj_class)

def two_phase_orifice(m_dot, cd, dp, rho, p):  # Imcompressable flow
    dp = p*dp
    pr = p/7270000
    z = -16.438*(pr**6)+44.625*(pr**5)-44.889*(pr**4)+20.313*(pr**3)-3.9608*(pr**2)-0.3575*pr+.9999
    area = ((m_dot)/(cd*math.sqrt(2*dp*rho)))*39.37**2/9
    diameter = math.sqrt(area*4/math.pi)
    return area, diameter

def incompressible_orifice(m_dot, cd, dp, rho, p):
    dp = dp * p
    area = ((m_dot)/(cd*math.sqrt(2*dp*rho)))*39.37**2/18
    diameter = math.sqrt(area*4/math.pi)
    return area, diameter


def injector_rows(cha_d, rows, initial, mult, inj_class):
    xarr = np.empty(0, float)
    yarr = np.empty(0, float)
    cha_r = cha_d/2
    rowarr = np.linspace(0, cha_r, rows+1)
    rowarr = np.delete(rowarr, 0)
    print(rowarr)
    rarr = np.linspace(0, cha_r, 100)
    phi = np.linspace(0, 2*math.pi, 120)
    half_range = rowarr[0] / 2
    for i in range(0, rows):
        r = rowarr[i]
        range_phi = 360 / (i*mult+initial+1)
        half_phi = range_phi/2
        for h in range(0, len(phi)-1):
            x = r * math.cos(phi[h])
            y = r * math.sin(phi[h])
            xarr = np.append(xarr, np.array([x]), axis=0)
            yarr = np.append(yarr, np.array([y]), axis=0)
        print(r-half_range)

    plt.scatter(xarr, yarr)
    plt.show()