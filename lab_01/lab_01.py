import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def get_alpha(dot):
    # a_1_1 a00 a01 a1_1
    alpha = np.zeros(4)

    if dot == "A0":
        alpha[0] = 0
        alpha[2] = 0
    elif dot == "A1":
        alpha[0] = sigma / (1 - sigma)
        alpha[2] = 0
    elif dot == "A2":
        alpha[0] = (1 + sigma) / (2 - sigma)
        alpha[2] = (1 - 2 * sigma) / (2 - sigma)
    elif dot == "A3":
        alpha[0] = 0
        alpha[2] = 1 / (2 + sigma)
    elif dot == "B1":
        a = ((2 + sigma) / (sigma * (1 - sigma))) ** 2 / 2
        alpha[0] = (1 + a *sigma) / ((1 - sigma) * (a + 2))
        alpha[2] = sigma / (2 + sigma) * (2 * (1 - sigma) * alpha[0] - 1)
    elif dot == "B2":
        alpha[0] = sigma * (sigma + 1) / ((2 - sigma) * (1 - sigma))
        alpha[2] = sigma * (2 * sigma - 1) / (2 - sigma)
    elif dot == "B3":
        alpha[0] = (1 + sigma) / (2 * sigma * (2 - sigma))
        alpha[2] = (1 - 2 * sigma) / (4 - sigma ** 2)
    elif dot == "B4":
        alpha[0] = 1 / (2 * (1 - sigma))
        alpha[2] = 0
    elif dot == "C":
        alpha[0] = (1 + sigma) / (2 * (1 - sigma) * (2 - sigma))
        alpha[2] = sigma * (2 * sigma - 1) / (4 - sigma ** 2)

    alpha[1] = (1 - alpha[2] * (2 + sigma) - 2 * sigma * alpha[0]) / (1 + sigma)
    alpha[3] = 1 - alpha[0] - alpha[2] - alpha[1]

    return alpha

def u_theor(tau):
    u_theor = np.zeros(N)
    for n in range(N):
        if (n*h - lamb * tau) > 0.4 and (n*h - lamb * tau) < 0.6:
            u_theor[n] = 1
    return u_theor



sigma = 0.25
X = 2
N = 201
h = 0.01
lamb = 1
tau = sigma * h / lamb
T = 100

u_prev, u_next = np.zeros(N), np.zeros(N)
# for n in range(N):
#     if n*h > 0.4 and n*h < 0.6:
#         u_prev[n] = 1
u_prev = u_theor(0)
u_this = u_prev.copy()
U = np.zeros((T + 1, N))
U[0] = u_prev.copy()
U[1] = u_this.copy()

hybrid = True
dot = "C"
# a_1_1 a00 a01 a1_1
alpha = np.zeros(4)

if not hybrid:
    alpha = get_alpha(dot)
    for t in range(2, T + 1):
        u_next[0], u_next[-1] = 0, 0
        for n in range(1, N - 1):
            # u_next[n] = (1 - sigma) * u_this[n] + sigma * u_this[n - 1]
            u_next[n] = alpha[0] * u_prev[n - 1] + alpha[1] * u_this[n] + alpha[2] * u_this[n + 1] + alpha[3] * u_next[n - 1]
        U[t] = u_next.copy()
        u_prev = u_this.copy()
        u_this = u_next.copy()
else:
    alpha1 = get_alpha("C")
    alpha2 = get_alpha("B2")
    alpha3 = get_alpha("B4")
    for t in range(2, T + 1):
        u_next[0], u_next[-1] = 0, 0
        for n in range(1, N - 1):
            u_next1 = alpha1[0] * u_prev[n - 1] + alpha1[1] * u_this[n] + alpha1[2] * u_this[n + 1] + alpha1[3] * u_next[n - 1]
            u_next2 = alpha2[0] * u_prev[n - 1] + alpha2[1] * u_this[n] + alpha2[2] * u_this[n + 1] + alpha2[3] * u_next[n - 1]
            u_next3 = alpha3[0] * u_prev[n - 1] + alpha3[1] * u_this[n] + alpha3[2] * u_this[n + 1] + alpha3[3] * u_next[n - 1]
            if min([u_prev[n - 1], u_this[n]]) <= u_next1 and u_next1 <= max([u_prev[n - 1], u_this[n]]):
                u_next[n] = u_next1
            elif min([u_prev[n - 1], u_this[n]]) <= u_next2 and u_next2 <= max([u_prev[n - 1], u_this[n]]):
                u_next[n] = u_next2
            elif min([u_prev[n - 1], u_this[n]]) <= u_next3 and u_next3 <= max([u_prev[n - 1], u_this[n]]):
                u_next[n] = u_next3
            else:
                u_next[n] = u_next1
        U[t] = u_next.copy()
        u_prev = u_this.copy()
        u_this = u_next.copy()

fig = plt.figure()
ax = plt.subplot()
# ax.set_ylim(0, 1.05)
ax.set_xlim(0, 1.5)

x_grid = np.linspace(0, X, N)

ax.plot(x_grid, U[T], "k")
ax.plot(x_grid, u_theor(T * tau), "b")
if not hybrid:
    ax.set_title(dot)
else:
    ax.set_title("hybrid: C + B2 + B4")

# def animate(i):
#     ax.clear()
#     ax.set_ylim(0, 1.05)
#     ax.plot(x_grid, U[i], "k")
#     ax.plot(x_grid, u_theor(i * tau), "b")
#     return ax

# interval_animation = 10
# repeat_animation = True
# corner_animation = FuncAnimation(fig, 
#                                 animate, 
#                                 np.arange(T + 1),
#                                 interval = interval_animation,
#                                 repeat = repeat_animation)

plt.show()