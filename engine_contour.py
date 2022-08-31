import math


# Modern Design, pg. 76-83
def engine_contour(t_d, a, exp_rat):
    t_r = throat_radius(t_d)
    r = arc_throat_radius(t_r)
    l_n = convergent_cone_length(t_r, r, a, exp_rat)
    print(t_r, r, l_n)


def throat_radius(t_d):
    t_r = t_d / 2
    return t_r


def arc_throat_radius(t_r):
    r = t_r * 1.5
    return r


def convergent_cone_length(t_r, r, a, exp_rat):  # (4-7)
    l_n = 0.85 * (t_r * (math.sqrt(exp_rat) - 1) + r * ((1 / math.cos(a)) - 1) )/ (math.tan(a))
    return l_n

def n_sub_b(t_r):
    pass