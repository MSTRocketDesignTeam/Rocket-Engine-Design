import math


# Modern Design, pg. 76-83
# http://www.aspirespace.org.uk/downloads/Thrust%20optimised%20parabolic%20nozzle.pdf
def engine_contour(t_d, a, exp_rat):
    theta_n = 22.7 * math.pi/180
    theta_e = 13.7 * math.pi/180
    t_r = throat_radius(t_d)
    r = arc_throat_radius(t_r)
    l_n = convergent_cone_length(t_r, r, a, exp_rat)
    n_t = n_sub_t(t_r, theta_n)
    n_a = n_sub_a(t_r, theta_n)
    e_t = l_n
    e_a = e_sub_a(t_r, exp_rat)

    n = [n_t, n_a]
    e = [e_t, e_a]

    g1, g2 = m_gradients(theta_n,theta_e)
    c1 = c_intercepts(n, g1)
    c2 = c_intercepts(e, g2)

    q_t = q_sub_t(g1, g2, c1, c2)
    q_a = q_sub_a(g1, g2, c1, c2)
    q = [q_t, q_a]

    print(n)
    print(q)
    print(e)
    print(t_r, r)
    print(.382*t_r)


def throat_radius(t_d):
    t_r = t_d / 2
    return t_r


def arc_throat_radius(t_r):
    r = t_r * 1.5
    return r


def convergent_cone_length(t_r, r, a, exp_rat):  # (4-7)
    l_n = 0.80 * (t_r * (math.sqrt(exp_rat) - 1) + r * ((1 / math.cos(a)) - 1)) / (math.tan(a))
    return l_n


def n_sub_t(t_r, theta_n):
    n_t = 0.382 * t_r * math.sin(theta_n)
    return n_t


def n_sub_a(t_r, theta_n):
    n_a = t_r + 0.382 * t_r * (1 - math.cos(theta_n))
    return n_a


def e_sub_a(t_r, exp_rat):
    e_a = math.sqrt(((math.pi*t_r**2)*exp_rat)/math.pi)

    return e_a


def m_gradients(theta_n, theta_e):
    g1 = math.tan(theta_n)
    g2 = math.tan(theta_e)
    return g1, g2


def c_intercepts(point, gradient):
    c = point[1] - gradient * point[0]
    #print(point, gradient, c)
    return c


def q_sub_t(g1, g2, c1, c2):
    q_t = (c2 - c1) / (g1 - g2)
    return q_t


def q_sub_a(g1, g2, c1, c2):
    q_a = g1 * (c2 - c1) / (g1 - g2) + c1
    return q_a
