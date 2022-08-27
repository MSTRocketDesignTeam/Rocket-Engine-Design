import engine_preformance


if __name__ == "__main__":
    class Structure:  # structure to make variables easier to categorize
        pass
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
    input0.F_o = 400 * conv.lbf2N  # Desired thrust (lbf)
    input0.P_atm = 14.0 * conv.psi2pa  # Ambient pressure (psia)
    input0.L_star = 1.27  # Characteristic chamber length (m) (chamber volume/throat area) (experimental)
    input0.esp_con = 17.1  # Contraction ratio (chamber area/throat area) (experimental)

    # Engine Geometry #
    input0.alpha = 15  # Conic half angle (deg)
    input0.chamber_shape = False  # True:curved | false:angled
    input0.throat_shape = False  # True:curved | false:angled
    input0.nozzle_shape = False  # True:curved | false:angled
    input0.throat_buffer = False  # True: present | false: not
    engine.chamber_wall_thickness = .25*conv.in2m  # (in)

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
    cea.P_c = 68.947 * conv.bar2pa  # Chamber pressure (bar)
    cea.T_c = 3229.8  # Chamber temperature (K)
    cea.rho_c = 6.7710  # Chamber gas density (kg/m^3)
    cea.dlV_dlPt = -1.01536  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.dlV_dlTp = 1.3145  # Thermodynamic expression (Heat Capacity Ratio Wiki) (Real Gas Relations)
    cea.C_p = 3.7762  # Specific heat at constant pressure (kJ/kg*k)

    # Engine Performance Calculations #
    # ---------------------#

    cal.R = cea.P_c/(cea.T_c*cea.rho_c)  # Calculates universal gas constant

    #cal.C_v = cea.C_p + cea.T_c * (pow(cea.dlV_dlTp, 2) / cea.dlV_dlPt)
    cal.C_v = cea.C_p + cal.R/1000 * (pow(cea.dlV_dlTp, 2) / cea.dlV_dlPt)  # Same reference as lines 65-66

    cal.y = cea.C_p/cal.C_v
    print(cal.y)
    #engine_preformance.engine_preformance()