import math


def engine_performance(p_atm, esp_con, p_c, y):
    c_f = math.sqrt((2 * (y ** 2) / (y - 1)) * (2 / (y+1)) ** ((y+1)/(y-1)) * (1-(p_atm/p_c)**((y-1)/y)))
    return c_f
