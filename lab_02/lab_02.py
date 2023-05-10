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

def u_theor(ul, ur, vel, centre, Ngrid, tau):
    u_theor = np.zeros(Ngrid)
    for n in range(Ngrid):
        if n*h - vel * tau < centre:
            u_theor[n] = ul
        else:
            u_theor[n] = ur
    return u_theor



sigma = 0.25
X = 2
N = 201
h = 0.01
c = 2
tau = sigma * h / c
T = 100

rho = 0.25
UPb = np.zeros((2, 2))
UPb[0, 0] = 1
UPb[0, 1] = 0
UPb[1, 0] = 5
UPb[1, 1] = 2
YZb = np.zeros((2, 2))
YZb[0, 0] = UPb[0, 0] + UPb[1, 0] / (rho * c)
YZb[0, 1] = UPb[0, 1] + UPb[1, 1] / (rho * c)
YZb[1, 0] = UPb[0, 0] - UPb[1, 0] / (rho * c)
YZb[1, 1] = UPb[0, 1] - UPb[1, 1] / (rho * c)


YZprev, YZnext = np.zeros((2, N)), np.zeros((2, N)) # Z inverted
# Z_prev, Z_next = np.zeros(N), np.zeros(N)   # inverted
# for n in range(N):
#     if n*h > 0.4 and n*h < 0.6:
#         u_prev[n] = 1
# for i in range(2):
YZprev[0] = u_theor(YZb[0][0], YZb[0][1], c, 0.5, N, 0)
YZprev[1] = u_theor(YZb[1][1], YZb[1][0], c, 0.5, N, 0) # inverted
# Z_prev = u_theor(Zr, Zl, c, 0.5, N, 0)

YZthis = YZprev.copy()
YZ = np.zeros((2, T + 1, N))
for i in range(2):
    YZ[i, 0] = YZprev[i].copy()
    YZ[1, 1] = YZthis[i].copy()

# Z_this = Z_prev.copy()
# Z = np.zeros((T + 1, N))
# Z[0] = Z_prev.copy()
# Z[1] = Z_this.copy()

hybrid = True
dot = "B1"
# a_1_1 a00 a01 a1_1
alpha = np.zeros(4)

if not hybrid:
    alpha = get_alpha(dot)
    for t in range(2, T + 1):
        YZnext[0, 0], YZnext[0, -1] = YZb[0, 0], YZb[0, 1]
        YZnext[1, 0], YZnext[1, -1] = YZb[1, 1], YZb[1, 0]
        for i in range(2):
            for n in range(1, N - 1):
                YZnext[i, n] = alpha[0] * YZprev[i, n - 1] + alpha[1] * YZthis[i, n] + alpha[2] * YZthis[i, n + 1] + alpha[3] * YZnext[i, n - 1]
            YZ[i, t] = YZnext[i].copy()
            YZprev[i] = YZthis[i].copy()
            YZthis[i] = YZnext[i].copy()
else:
    alpha1 = get_alpha("C")
    alpha2 = get_alpha("B2")
    alpha3 = get_alpha("B4")
    for t in range(2, T + 1):
        YZnext[0, 0], YZnext[0, -1] = YZb[0, 0], YZb[0, 1]
        YZnext[1, 0], YZnext[1, -1] = YZb[1, 1], YZb[1, 0]
        for i in range(2):
            # YZnext[i, 0], YZnext[i, -1] = YZb[i, 0], YZb[i, 1]
            for n in range(1, N - 1):
                YZnext1 = alpha1[0] * YZprev[i, n - 1] + alpha1[1] * YZthis[i, n] + alpha1[2] * YZthis[i, n + 1] + alpha1[3] * YZnext[i, n - 1]
                YZnext2 = alpha2[0] * YZprev[i, n - 1] + alpha2[1] * YZthis[i, n] + alpha2[2] * YZthis[i, n + 1] + alpha2[3] * YZnext[i, n - 1]
                YZnext3 = alpha3[0] * YZprev[i, n - 1] + alpha3[1] * YZthis[i, n] + alpha3[2] * YZthis[i, n + 1] + alpha3[3] * YZnext[i, n - 1]
                # u_next2 = alpha2[0] * u_prev[n - 1] + alpha2[1] * u_this[n] + alpha2[2] * u_this[n + 1] + alpha2[3] * u_next[n - 1]
                # u_next3 = alpha3[0] * u_prev[n - 1] + alpha3[1] * u_this[n] + alpha3[2] * u_this[n + 1] + alpha3[3] * u_next[n - 1]
                if min([YZprev[i, n - 1], YZthis[i, n]]) <= YZnext1 and YZnext1 <= max([YZprev[i, n - 1], YZthis[i, n]]):
                    YZnext[i, n] = YZnext1
                elif min([YZprev[i, n - 1], YZthis[i, n]]) <= YZnext2 and YZnext2 <= max([YZprev[i, n - 1], YZthis[i, n]]):
                    YZnext[i, n] = YZnext2
                elif min([YZprev[i, n - 1], YZthis[i, n]]) <= YZnext3 and YZnext3 <= max([YZprev[i, n - 1], YZthis[i, n]]):
                    YZnext[i, n] = YZnext3
                else:
                    YZnext[i, n] = YZnext1
            YZ[i, t] = YZnext[i].copy()
            YZprev[i] = YZthis[i].copy()
            YZthis[i] = YZnext[i].copy()

Nnew = int((N - 1) * 3/2) + 1
Nnew_3 = int((N - 1) / 2)
UP = np.zeros((2, T + 1, Nnew))
# P = np.zeros((T + 1, Nnew))
for n in range(Nnew):
    if n < Nnew_3:
        UP[0, :, n] = (YZb[0, 0] + YZ[1, :, -(n + 1)]) / 2
        UP[1, :, n] = (YZb[0, 0] - YZ[1, :, -(n + 1)]) * rho * c / 2
    elif n <= 2 * Nnew_3:
        UP[0, :, n] = (YZ[0, :, n - Nnew_3] + YZ[1, :, -(n + 1)]) / 2
        UP[1, :, n] = (YZ[0, :, n - Nnew_3] - YZ[1, :, -(n + 1)]) * rho * c / 2
    else:
        UP[0, :, n] = (YZ[0, :, n - Nnew_3] + YZb[1, 1]) / 2
        UP[1, :, n] = (YZ[0, :, n - Nnew_3] - YZb[1, 1]) * rho * c / 2


# fig = plt.figure()
fig, axs = plt.subplots(2, 1, sharex=True)
# ax.set_ylim(0, 1.05)
axs[0].set_xlim(0, 3 * X / 2)

# x_grid = np.linspace(0, X, N)
x_grid = np.linspace(0, X * 3 / 2, Nnew)

UPth = np.zeros((2, 2, Nnew))
for i in range(2):
    axs[i].set_xlim(0, 3 * X / 2)
    axs[i].plot(x_grid, UP[i, T], "k")
    UPth[i, 0] = u_theor(UPb[i, 0], UPb[i, 1], c, 1.5, Nnew, T * tau)
    UPth[i, 1] = u_theor(UPb[i, 0], UPb[i, 1], c, 1.5, Nnew, - T * tau)
axs[0].set_title("U")
axs[1].set_title("P")
axs[0].set_ylim(np.min(UPb[0]) - 1, (UPb[0, 0] + UPb[0, 1])/2 + (UPb[1, 0] - UPb[1, 1])/(2*rho*c) + 1)
axs[1].set_ylim(np.min(UPb[1]) - 1, np.max(UPb[i]) + 1)

Uth = (UPth[0, 0] + UPth[0, 1]) / 2 + (UPth[1, 0] - UPth[1, 1]) / (2 * rho * c)
Pth = (UPth[0, 0] - UPth[0, 1]) * rho * c / 2 + (UPth[1, 0] + UPth[1, 1]) / 2
axs[0].plot(x_grid, Uth, "b")
axs[1].plot(x_grid, Pth, "b")

# if not hybrid:
#     ax.set_title(dot)
# else:
#     ax.set_title("hybrid: C + B2 + B4")

# def animate(k):
#     for i in range(2):
#         axs[i].clear()
#         axs[i].set_ylim(np.min(YZb[i]) - 1, np.max(YZb[i]) + 1)
#         axs[i].plot(x_grid, YZ[i, k], "k")
#     axs[0].plot(x_grid, u_theor(YZb[0, 0], YZb[0, 1], c, 0.5, N, k * tau), "b")
#     axs[1].plot(x_grid, u_theor(YZb[1, 1], YZb[1, 0], c, 0.5, N, k * tau), "b")
#     return axs

if not hybrid:
    fig.suptitle(dot)
else:
    fig.suptitle("hybrid: C + B2 + B4")

# def animate(k):
#     UPth = np.zeros((2, 2, Nnew))
#     for i in range(2):
#         axs[i].clear()
#         axs[i].set_xlim(0, 3 * X / 2)
#         # axs[i].set_ylim(np.min(UPb[i]) - 1, np.max(UPb[i]) + 1)
#         axs[i].plot(x_grid, UP[i, k], "k")
#         UPth[i, 0] = u_theor(UPb[i, 0], UPb[i, 1], c, 1.5, Nnew, k * tau)
#         UPth[i, 1] = u_theor(UPb[i, 0], UPb[i, 1], c, 1.5, Nnew, - k * tau)

#     axs[0].set_title("U")
#     axs[1].set_title("P")
#     axs[0].set_ylim(np.min(UPb[0]) - 1, (UPb[0, 0] + UPb[0, 1])/2 + (UPb[1, 0] - UPb[1, 1])/(2*rho*c) + 1)
#     axs[1].set_ylim(np.min(UPb[1]) - 1, np.max(UPb[i]) + 1)
    
#     Uth = (UPth[0, 0] + UPth[0, 1]) / 2 + (UPth[1, 0] - UPth[1, 1]) / (2 * rho * c)
#     Pth = (UPth[0, 0] - UPth[0, 1]) * rho * c / 2 + (UPth[1, 0] + UPth[1, 1]) / 2
#     axs[0].plot(x_grid, Uth, "b")
#     axs[1].plot(x_grid, Pth, "b")

#     return axs

# interval_animation = 10
# repeat_animation = True
# corner_animation = FuncAnimation(fig, 
#                                 animate, 
#                                 np.arange(T + 1),
#                                 interval = interval_animation,
#                                 repeat = repeat_animation)

plt.show()