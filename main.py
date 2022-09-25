import importlib.util
import engine_contour
import engine_performance
from math import pi
import subprocess
import sys
import numpy as np
import mach_relationships


# TO DO
# 1) Make contour code write to .csv
# 2) Allow user to pick between bell and conical
# 3) Model parabola of theta e & n vs expansion ratio. Take input expansion to automatically pick correct values
# 4) Account for unequal number of orifices, 10f-5o, maybe deal with deltaP pg. 279
# 5) Use .csv files to do weird temp, pressure, and mach stuff along nozzle centerline
# 6) Allow custom output units
# 7) Make GUI


# Notes
# 1) Equlibrium in CEA means infinit reativity of gases, they keep reacting, frozen means that there is no reaction
# The big point being that eq. is ideal, while frozen is harsh
 

def install(package):
    spec = importlib.util.find_spec(package)
    if spec is None:
        print("no")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    else:
        print('yes')


class Structure:  # structure to make variables easier to categorize
    def __int__(self):
        pass


if __name__ == "__main__":
    #install('matplotlib')
    #install('numpy')
    #install('scipy')


    const = Structure()
    conv = Structure()
    input0 = Structure()
    engine = Structure()
    cea = Structure()
    cal = Structure()

    # Universal Constants/Conversions #
    # ---------------------#

    # Constants
    const.g_0 = 9.81  # Gravitational acceleration (m*s^-2)
    const.r_Prime = 8.314  # Universal gas constant (J*mol^-1*K^-1)

    # Conversions (These are done to make calculations in metric easier)
    conv.psi2pa = 6894.76
    conv.lbf2N = 4.44822
    conv.in2m = 0.0254
    conv.bar2pa = 100000
    conv.lbcft2kgm3 = 16.0185
    conv.gpm2cfm = 0.1337
    conv.cfm2m3m = 0.0283168
    conv.deg2rad = pi/180

    # Inputs #
    # ---------------------#

    # Output Variable Unit Preference #

    # Design Parameters #
    input0.F_o = 500 * conv.lbf2N  # Desired thrust (lbf)
    input0.P_atm = 14.7 * conv.psi2pa  # Ambient pressure (psia)
    input0.L_star = 1.3   # Characteristic chamber length (m) (chamber volume/throat area) (experimental)
    input0.esp_con = 8  # Contraction ratio (chamber area/throat area) (experimental)


    # Engine Geometry #
    input0.alpha = 15 * conv.deg2rad # Conic half angle (deg)
    input0.chamber_shape = False  # True:curved | false:angled
    input0.throat_shape = False  # True:curved | false:angled
    input0.nozzle_shape = False  # True:curved | false:angled
    input0.throat_buffer = False  # True: present | false: not
    engine.chamber_wall_thickness = .25 * conv.in2m  # (in)

    # Injector #
    engine.injector_del_P = 0.20  # Pressure drop across injector   (high for low chamber pressures)
    engine.injector_oxid_N = 20  # Number of oxidizer injector orifices
    engine.injector_fuel_N = 20  # Number of fuel injector orifices
    engine.injector_C_d = .8  # Discharge coefficient (~)  Helps determine performance ahead of time

    # Correction Factors #
    input0.s_f = 0.96  # Thrust correction factor (~)
    input0.s_v = 0.92  # Velocity correction factor (~)

    # NASA CEA Outputs #
    cea.MR = 5.25  # Oxidizer/Fuel Ratio
    cea.P_c = 20.684 * conv.bar2pa  # Chamber pressure
    cea.T_c = 3125.12  # Chamber temperature (K)
    cea.rho_c = 2.0810  # Chamber gas density (kg/m^3)
    cea.dlV_dlPt = -1.01839  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.dlV_dlTp = 1.3841  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.C_p = 4.2984  # Specific heat at constant pressure (kJ/kg*k)
    cea.y = 1.1407  # Ratio of specific heats

    # Engine Performance Calculations #
    # ---------------------#

    cal.R = cea.P_c / (cea.T_c * cea.rho_c)  # Calculates gas constant

    # Way to calculate specific heat at const. volume. Useful if gamma isn't given
    cal.C_v = cea.C_p + cal.R / 1000 * (pow(cea.dlV_dlTp, 2) / cea.dlV_dlPt)
    cal.y = cea.C_p / cal.C_v

    # Calls engine_performance.py
    cal.C_f, cal.C_f_vac, cal.c_star, cal.exp_rat, cal.isp_sl, cal.isp_vac, cal.t_a, cal.t_d, cal.c_a, cal.c_d, \
    cal.c_v, cal.t_p, cal.t_t, cal.e_a, cal.e_d, cal.e_t, cal.e_v, cal.m, cal.m_dot, cal.m_dot_f, cal.m_dot_o = \
        engine_performance.engine_performance(input0.P_atm, input0.esp_con, cea.P_c, cea.y, cal.R, cea.T_c, input0.s_f,
                                              input0.s_v, input0.F_o, input0.L_star, cea.MR)

    # Print statement of outputs
    print("Coefficient of Thrust:              ", cal.C_f)
    print("Coefficient of thrust in vacuum:    ", cal.C_f_vac)
    print("Characteristic Velocity:            ", cal.c_star, "m/s")
    print("Expansion ratio:                    ", cal.exp_rat)
    print("Specific impulse at sea level:      ", cal.isp_sl, "s")
    print("Specific impulse in vacuum:         ", cal.isp_vac, "s")
    print("Throat area:                        ", cal.t_a, "m^2")
    print("Throat diameter:                    ", cal.t_d, "m")
    print("Chamber area:                       ", cal.c_a, "m^2")
    print("Chamber diameter:                   ", cal.c_d, "m")
    print("Chamber volume:                     ", cal.c_v, "m^3")
    print("Throat Pressure:                    ", cal.t_p, "Pa")
    print("Throat temperature:                 ", cal.t_t, "K")
    print("Exit Area:                          ", cal.e_a, "m^2")
    print("Exit diameter:                      ", cal.e_d, "m")
    print("Exit temperature:                   ", cal.e_t, "K")
    print("Exit velocity:                      ", cal.e_v, "m/s")
    print("Exit Mach:                          ", cal.m)
    print("Total mass flow:                    ", cal.m_dot, "kg/s")
    print("Fuel mass flow:                     ", cal.m_dot_f, "kg/s")
    print("Oxidizer mass flow:                 ", cal.m_dot_o, "kg/s")

    # Calls engine_contour.py
    pointx, pointy, norm_x = engine_contour.engine_contour(cal.t_d, cal.c_d, input0.alpha, cal.exp_rat, input0.L_star)


    #  mach_relationships.mach_relationships(pointx, pointy, cal.t_t, cal.t_p, cea.y)
