import math


class Structure:  # structure to make variables easier to categorize
    def __int__(self):
        pass


def engine_performance(p_atm, esp_con, p_c, y, r, c_t):
    c_f = thrust_coefficient(p_atm, p_c, y)
    c_f_vac = thrust_coefficient_vac(c_f, esp_con, p_atm, p_c)
    c_star = characteristic_velocity(y, r, c_t)
    exp_rat = expansion_ratio(y, p_atm, p_c)
    return c_f, c_f_vac, c_star, exp_rat


def thrust_coefficient(p_atm, p_c, y):
    # RPE (3-30), calculates thrust coefficient
    c_f = math.sqrt(
        (2 * (y ** 2) / (y - 1)) * (2 / (y + 1)) ** ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y)))
    return c_f


def thrust_coefficient_vac(c_f, esp_con, p_atm, p_c):
    # RPE (3-30), modified, calculates thrust coefficient in a vacuum
    c_f_vac = c_f + esp_con * (p_atm / p_c)
    return c_f_vac


def characteristic_velocity(y, r, c_t):
    c_star = math.sqrt(y * r * c_t) / (y * math.sqrt((2 / (y + 1)) ** ((y + 1) / (y - 1))))
    return c_star


def expansion_ratio(y, p_atm, p_c):
    exp_rat = (((y + 1) / 2) ** (1 / (y - 1))) * ((p_atm / p_c) ** (1 / y)) * math.sqrt(
        ((y + 1) / (y - 1)) * (1 - (p_atm / p_c) ** ((y - 1) / y)))
    return exp_rat
