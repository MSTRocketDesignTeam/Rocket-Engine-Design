import engine_performance
import math
import subprocess
import sys


def install(numpy, scipy, matplotlib):
    subprocess.check_call([sys.executable, "-m", "pip", "install", numpy])
    subprocess.check_call([sys.executable, "-m", "pip", "install", scipy])
    subprocess.check_call([sys.executable, "-m", "pip", "install", matplotlib])


class Structure:  # structure to make variables easier to categorize
    def __int__(self):
        pass


if __name__ == "__main__":
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

    # Inputs #
    # ---------------------#

    # Output Variable Unit Preference #

    # Design Parameters #
    input0.F_o = 2000 * conv.lbf2N  # Desired thrust (lbf)
    input0.P_atm = 14.7 * conv.psi2pa  # Ambient pressure (psia)
    input0.L_star = 1.27  # Characteristic chamber length (m) (chamber volume/throat area) (experimental)
    input0.esp_con = 17.1  # Contraction ratio (chamber area/throat area) (experimental)

    # Engine Geometry #
    input0.alpha = 15  # Conic half angle (deg)
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
    cea.P_c = 68.947 * conv.bar2pa  # Chamber pressure
    cea.T_c = 3229.84  # Chamber temperature (K)
    cea.rho_c = 6.7710  # Chamber gas density (kg/m^3)
    cea.dlV_dlPt = -1.01536  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.dlV_dlTp = 1.3145  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.C_p = 3.7762  # Specific heat at constant pressure (kJ/kg*k)
    cea.y = 1.1480  # Ratio of specific heats

    # Engine Performance Calculations #
    # ---------------------#

    cal.R = cea.P_c / (cea.T_c * cea.rho_c)  # Calculates universal gas constant

    # cal.C_v = cea.C_p + cea.T_c * (pow(cea.dlV_dlTp, 2) / cea.dlV_dlPt)
    cal.C_v = cea.C_p + cal.R / 1000 * (pow(cea.dlV_dlTp,  # Same reference as lines 65-66
                                            2) / cea.dlV_dlPt)  # Likely won't include, inaccurate

    cal.y = cea.C_p / cal.C_v

    cal.C_f, cal.C_f_vac, cal.c_star, cal.exp_rat, cal.isp_sl, cal.isp_vac, cal.a_t, cal.d_t, cal.a_c, cal.d_c, \
    cal.c_v, cal.p_t, cal.t_t, cal.a_e, cal.d_e, cal.e_t = engine_performance.engine_performance(
        input0.P_atm, input0.esp_con, cea.P_c, cea.y, cal.R, cea.T_c, input0.s_f, input0.s_v, input0.F_o, input0.L_star)

    print("Coefficient of Thrust:              ", cal.C_f)
    print("Coefficient of thrust in vacuum:    ", cal.C_f_vac)
    print("Characteristic Velocity:            ", cal.c_star, "m/s")
    print("Expansion ratio:                    ", cal.exp_rat)
    print("Specific impulse at sea level:      ", cal.isp_sl, "s")
    print("Specific impulse in vacuum:         ", cal.isp_vac, "s")
    print("Throat area:                        ", cal.a_t, "m^2")
    print("Throat diameter:                    ", cal.d_t, "m")
    print("Chamber area:                       ", cal.a_c, "m^2")
    print("Chamber diameter:                   ", cal.d_c, "m")
    print("Chamber volume:                     ", cal.c_v, "m^3")
    print("Throat Pressure:                    ", cal.p_t, "Pa")
    print("Throat temperature:                 ", cal.t_t, "K")
    print("Exit Area:                          ", cal.a_e, "m^2")
    print("Exit diameter:                      ", cal.d_e, "m")
    print("Exit temperature:                   ", cal.e_t, "K")
