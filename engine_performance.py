import math


class Structure:  # structure to make variables easier to categorize
    def __int__(self):
        pass


def engine_performance(p_atm, esp_con, p_c, y, r, c_t, s_f, s_v, f_o, l_star):
    c_f = thrust_coefficient(p_atm, p_c, y)
    c_f_vac = thrust_coefficient_vac(esp_con, p_atm, p_c, c_f)
    c_star = characteristic_velocity(y, r, c_t)
    exp_rat = expansion_ratio(y, p_atm, p_c)
    isp_sl = specific_impulse_sl(c_star, c_f, s_v)
    isp_vac = specific_impulse_vac(c_star, c_f_vac, s_v)
    a_t = throat_area(f_o, c_f, p_c, s_f)
    d_t = diameter(a_t)
    a_c = chamber_area(esp_con, a_t)
    d_c = diameter(a_c)
    c_v = chamber_vol(l_star, a_t)
    p_t = throat_pressure(p_c, y)
    t_t = throat_temperature(c_t, y)
    a_e = exit_area(exp_rat, a_t)
    d_e = diameter(a_e)
    e_t = exit_temperature(c_t, p_atm, p_c, y)
    return c_f, c_f_vac, c_star, exp_rat, isp_sl, isp_vac, a_t, d_t, a_c, d_c, c_v, p_t, t_t, a_e, d_e, e_t


def thrust_coefficient(p_atm, p_c, y):
    # RPE (3-30), calculates thrust coefficient
    c_f = math.sqrt(
        (2 * (y ** 2) / (y - 1)) * (2 / (y + 1)) ** ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y)))
    return c_f


def thrust_coefficient_vac(esp_con, p_atm, p_c, c_f):
    # RPE (3-30), modified, calculates thrust coefficient in a vacuum
    c_f_vac = c_f + esp_con * (p_atm / p_c)
    return c_f_vac


def characteristic_velocity(y, r, c_t):
    c_star = math.sqrt(y * r * c_t) / (y * math.sqrt((2 / (y + 1)) ** ((y + 1) / (y - 1))))
    return c_star


def expansion_ratio(y, p_atm, p_c):
    exp_rat = 1 / ((((y + 1) / 2) ** (1 / (y - 1))) * ((p_atm / p_c) ** (1 / y)) * math.sqrt(
        ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y))))
    return exp_rat


def specific_impulse_sl(c_star, c_f, s_v):
    isp_sl = c_star * s_v * c_f / 9.81
    return isp_sl


def specific_impulse_vac(c_star, c_f_vac, s_v):
    isp_vac = c_star * s_v * c_f_vac / 9.81
    return isp_vac


def throat_area(f_o, c_f, p_c, s_f):
    a_t = f_o / (c_f * p_c * s_f)
    return a_t


def diameter(a):
    d = math.sqrt((4 * a) / math.pi)
    return d


def chamber_area(esp_con, a_t):
    a_c = esp_con * a_t
    return a_c


def chamber_vol(l_star, a_t):
    c_v = l_star * a_t
    return c_v


def throat_pressure(p_c, y):
    p_t = p_c * (2 / (y + 1)) ** (y / (y - 1))
    return p_t


def throat_temperature(c_t, y):
    t_t = (2 * c_t) / (y + 1)
    return t_t


def exit_area(exp_rat, a_t):
    a_e = exp_rat * a_t
    return a_e


def exit_temperature(c_t, p_atm, p_c, y):
    e_t = c_t * (p_atm / p_c) ** ((y - 1) / y)
    return e_t
