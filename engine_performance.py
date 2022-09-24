from math import pi, sqrt

 # Calls various functions to calculate basic engine performance parameters and generosity
def engine_performance(p_atm, esp_con, p_c, y, r, c_t, s_f, s_v, f_o, l_star, mr):
    c_f = thrust_coefficient(p_atm, p_c, y)
    c_f_vac = thrust_coefficient_vac(esp_con, p_atm, p_c, c_f)
    c_star = characteristic_velocity(y, r, c_t)
    exp_rat = expansion_ratio(y, p_atm, p_c)
    isp_sl = specific_impulse_sl(c_star, c_f, s_v)
    isp_vac = specific_impulse_vac(c_star, c_f_vac, s_v)
    t_a = throat_area(f_o, c_f, p_c, s_f)
    t_d = diameter(t_a)
    c_a = chamber_area(esp_con, t_a)
    d_c = diameter(c_a)
    c_v = chamber_vol(l_star, t_a)
    t_p = throat_pressure(p_c, y)
    t_t = throat_temperature(c_t, y)
    e_a = exit_area(exp_rat, t_a)
    e_d = diameter(e_a)
    e_t = exit_temperature(c_t, p_atm, p_c, y)
    e_v = exit_velocity(y, r, c_t, p_atm, p_c)
    m = exit_mach(e_t, c_t, y)
    m_dot = mass_flow(t_a, p_c, y, r, c_t)
    m_dot_f = fuel_mass_flow(m_dot, mr)
    m_dot_o = oxidizer_mass_flow(m_dot, mr)
    return c_f, c_f_vac, c_star, exp_rat, isp_sl, isp_vac, t_a, t_d, c_a, d_c, c_v, t_p, t_t, e_a, e_d, e_t, e_v, m, \
           m_dot, m_dot_f, m_dot_o


def thrust_coefficient(p_atm, p_c, y):
    # RPE (3-30), calculates thrust coefficient
    c_f = sqrt(
        (2 * (y ** 2) / (y - 1)) * (2 / (y + 1)) ** ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y)))
    return c_f


def thrust_coefficient_vac(esp_con, p_atm, p_c, c_f):
    # RPE (3-30), modified, calculates thrust coefficient in a vacuum
    c_f_vac = c_f + esp_con * (p_atm / p_c)
    return c_f_vac


def characteristic_velocity(y, r, c_t):
    # RPE (3-32), calculates characteristic velocity, (m/s)
    c_star = sqrt(y * r * c_t) / (y * sqrt((2 / (y + 1)) ** ((y + 1) / (y - 1))))
    return c_star


def expansion_ratio(y, p_atm, p_c):
    # RPE (3-25), calculates the expansion ratio of a nozzle
    exp_rat = 1 / ((((y + 1) / 2) ** (1 / (y - 1))) * ((p_atm / p_c) ** (1 / y)) * sqrt(
        ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y))))
    return exp_rat


def specific_impulse_sl(c_star, c_f, s_v):
    # RPE (3-32), calculates specific impulse based at sea level, (s)
    isp_sl = c_star * s_v * c_f / 9.8067
    return isp_sl


def specific_impulse_vac(c_star, c_f_vac, s_v):
    # RPE (3-32), calculates specific impulse based in vacuum, (s)
    isp_vac = c_star * s_v * c_f_vac / 9.8067
    return isp_vac


def diameter(a):
    # Basic geometry, calculates diameter from area, (m^2)
    d = 2 * sqrt(a / pi)
    return d


def throat_area(f_o, c_f, p_c, s_f):
    # RPE (3-31), calculates the throat area of the nozzle, (m^2)
    t_a = f_o / (c_f * p_c * s_f)
    return t_a


def chamber_area(esp_con, t_a):
    # Multiplies throat area and contraction ratio to calculate chamber area, (m^2)
    c_a = esp_con * t_a
    return c_a


def chamber_vol(l_star, t_a):
    # RPE (8-9), Calculates chamber volume, (m^3)
    c_v = l_star * t_a
    return c_v


def throat_pressure(p_c, y):
    # RPE (3-20), calculates throat pressure, (Pa)
    t_p = p_c * (2 / (y + 1)) ** (y / (y - 1))
    return t_p


def throat_temperature(c_t, y):
    # RPE (3-22), calculates throat temperature, (K)
    t_t = (2 * c_t) / (y + 1)
    return t_t


def exit_area(exp_rat, t_a):
    # RPE (3-19), calculates exit area, (m^2)
    e_a = exp_rat * t_a
    return e_a


def exit_temperature(c_t, p_atm, p_c, y):
    # RPE (3-7), calculates exit temperature, (K)
    e_t = c_t * (p_atm / p_c) ** ((y - 1) / y)
    return e_t


def exit_velocity(y, r, c_t, p_atm, p_c):
    # RPE (3-16), calculates exit velocity, (m/s)
    e_v = sqrt(((y * 2 * r * c_t) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y)))
    return e_v


def exit_mach(e_t, c_t, y):
    # RPE (3-12) modified, calculates exit mach number, (M)
    m = sqrt((2 / (y - 1)) * ((c_t / e_t) - 1))
    return m


def mass_flow(t_a, p_c, y, r, c_t):
    # RPE (3-24), calculates total mass flow of propellants, (kg/s)
    m_dot = t_a * p_c * y * ((sqrt((2 / (y + 1)) ** ((y + 1) / (y - 1)))) / (sqrt(y * r * c_t)))
    return m_dot


def fuel_mass_flow(m_dot, mr):
    # RPE (6-4), calculates mass flow of fuel, (kg/s)
    m_dot_f = m_dot / (mr + 1)
    return m_dot_f


def oxidizer_mass_flow(m_dot, mr):
    # RPE (6-3), calculates mass flow of oxidizer, (kg/s)
    m_dot_o = mr * m_dot / (mr + 1)
    return m_dot_o
