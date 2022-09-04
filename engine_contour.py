import math
import numpy as np
from matplotlib import pyplot as plt


# Modern Design, pg. 76-83
# http://www.aspirespace.org.uk/downloads/Thrust%20optimised%20parabolic%20nozzle.pdf

def engine_contour(t_d, c_d, a, exp_rat, l_star):
    theta_n = 22.7 * math.pi / 180
    theta_e = 13.7 * math.pi / 180
    t_r = throat_radius(t_d)
    r = arc_throat_radius(t_r)
    l_n = convergent_cone_length(t_r, r, a, exp_rat)
    n_t = n_sub_t(t_r, theta_n)
    n_a = n_sub_a(t_r, theta_n)
    e_t = l_n
    e_a = e_sub_a(t_r, exp_rat)

    n = [n_t, n_a]
    e = [e_t, e_a]
    norm_x = l_n / 1000

    g1, g2 = m_gradients(theta_n, theta_e)
    c1 = c_intercepts(n, g1)
    c2 = c_intercepts(e, g2)

    q_t = x_point(g1, g2, c1, c2)
    q_a = y_point(g1, g2, c1, c2)
    q = [q_t, q_a]

    bell_px, bell_py = bell_exit(n, e, q, norm_x)
    bell_npx, bell_npy = bell_nozzle(theta_n, t_r, norm_x)
    bell_conx, bell_cony = bell_con(theta_n, t_r, norm_x)

    g3, g4 = 0, -2 / math.sqrt(2)
    c3 = c_intercepts([-l_star, c_d / 2], g3)
    c4 = c_intercepts([bell_conx[0], bell_cony[0]], g4)
    h_t = x_point(g3, g4, c3, c4)
    h_a = y_point(g3, g4, c3, c4)
    h = [h_t, h_a]

    pointx = np.empty(0, float)
    pointy = np.empty(0, float)
    pointx = np.append(pointx, np.array([bell_npx]))
    pointx = np.append(pointx, np.array([bell_px]))
    pointy = np.append(pointy, np.array([bell_npy]))
    pointy = np.append(pointy, np.array([bell_py]))
    pointx = np.append(pointx, np.array([bell_conx]))
    pointy = np.append(pointy, np.array([bell_cony]))

    plt.title("Chamber")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.scatter(pointx, pointy)
    plt.show()


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
    e_a = math.sqrt(((math.pi * t_r ** 2) * exp_rat) / math.pi)

    return e_a


def m_gradients(theta_n, theta_e):
    g1 = math.tan(theta_n)
    g2 = math.tan(theta_e)
    return g1, g2


def c_intercepts(point, gradient):
    c = point[1] - gradient * point[0]
    # print(point, gradient, c)
    return c


def x_point(g1, g2, c1, c2):
    q_t = (c2 - c1) / (g1 - g2)
    return q_t


def y_point(g1, g2, c1, c2):
    q_a = g1 * (c2 - c1) / (g1 - g2) + c1
    return q_a


def bell_exit(n, q, e, norm_x):
    norm_v = abs(int((n[0] - e[0]) / norm_x))
    print(norm_v)
    t = np.linspace(0, 1, norm_v)
    xarr = np.empty(0, float)
    yarr = np.empty(0, float)
    for i in t:
        x = n[0] * ((1 - i) ** 2) + 2 * i * e[0] * (1 - i) + q[0] * (i ** 2)
        y = n[1] * ((1 - i) ** 2) + 2 * i * e[1] * (1 - i) + q[1] * (i ** 2)
        xarr = np.append(xarr, np.array([x]), axis=0)
        yarr = np.append(yarr, np.array([y]), axis=0)
    return xarr, yarr


def bell_nozzle(theta_n, t_r, norm_x):
    norm_v = abs(int(0.382 * t_r * math.cos(theta_n - (math.pi / 2)) / norm_x))
    t = np.linspace((-math.pi / 2), theta_n - (math.pi / 2), norm_v)
    print(norm_v)
    xarr = np.empty(0, float)
    yarr = np.empty(0, float)
    for i in t:
        x = 0.382 * t_r * math.cos(i)
        y = 0.382 * t_r * math.sin(i) + .382 * t_r + t_r
        xarr = np.append(xarr, np.array([x]), axis=0)
        yarr = np.append(yarr, np.array([y]), axis=0)
    return xarr, yarr


def bell_con(theta_n, t_r, norm_x):
    norm_v = int(abs(1.5 * t_r * math.cos(-math.pi * 3 / 4)) / norm_x)
    print(norm_v)
    xarr = np.empty(0, float)
    yarr = np.empty(0, float)
    t = np.linspace(-math.pi * 3 / 4, -math.pi / 2, norm_v)
    for i in t:
        x = 1.5 * t_r * math.cos(i)
        y = 1.5 * t_r * math.sin(i) + 1.5 * t_r + t_r
        xarr = np.append(xarr, np.array([x]), axis=0)
        yarr = np.append(yarr, np.array([y]), axis=0)
    return xarr, yarr
