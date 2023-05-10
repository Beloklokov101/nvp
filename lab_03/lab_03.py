import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

gamma = 1.4
rho_bor = np.array([1, 1])
u_bor = np.array([0, 0])
p_bor = np.array([1000, 0.01])
W_bor = np.array([rho_bor, u_bor, p_bor])
U_bor, F_bor = np.zeros((3, 2)), np.zeros((3, 2))
U_bor[0] = W_bor[0]
U_bor[1] = W_bor[0] * W_bor[1]
U_bor[2] = W_bor[2] / (gamma - 1) + W_bor[0] * W_bor[1]**2 / 2
F_bor[0] = U_bor[1]
F_bor[1] = W_bor[2] + U_bor[1]**2 / U_bor[0]
F_bor[2] = (W_bor[2] + U_bor[2]) * U_bor[1] / U_bor[0]

N = 1000
h = 1 / N
TIME = 5e-3
CFL = 0.25

W = np.zeros((3, N + 1))
U = np.zeros((3, N + 1))
F = np.zeros((3, N + 1))

for n in range(N + 1):
    flag = int(h * n > 0.5)
    W[:, n] = W_bor[:, flag]
    U[:, n] = U_bor[:, flag]
    F[:, n] = F_bor[:, flag]

U_next = np.zeros((3, N + 1))
T = 0
while(T < TIME):
    c = np.max(np.sqrt(gamma * W[2] / W[0]))
    tau = CFL * h / np.max(c + np.abs(W[1]))

    for i in range(2):
        U_next[:, -i] = U_bor[:, i]
    
    F_LF = np.zeros((3, N))
    for n in range(N):
        F_LF[:, n] = (F[:, n] + F[:, n + 1]) / 2 + (U[:, n] - U[:, n + 1]) * h / tau / 2
    for n in range(1, N):
        U_next[:, n] = U[:, n] + (F_LF[:, n - 1] - F_LF[:, n]) * tau / h
    
    U = U_next.copy()
    W[0] = U[0]
    W[1] = U[1] / U[0]
    W[2] = (gamma - 1) * (U[2] - U[1]**2 / (2 * U[0]))
    F[0] = U[1]
    F[1] = W[2] + U[1]**2 / U[0]
    F[2] = (W[2] + U[2]) * U[1] / U[0]

    T += tau
    U_next = np.zeros((3, N + 1))
    print(T)

x_grid = np.linspace(0, 1, N + 1)

fig, axs = plt.subplots(3, 1, sharex=True)
# axs[0].set_xlim(0, 1)
axs[0].plot(x_grid, W[0], "b")
axs[1].plot(x_grid, W[1], "b")
axs[2].plot(x_grid, W[2], "b")
# print(W)
# for i in range(3):
#     axs[i].legend()

with open("C://My_Progs//nvp//Accurate_solution//Accurate_solution//Exact_solution//Exact_solution//exact_solution.dat", "r") as file:
    filelines = file.read().split("\n")
len_file = len(filelines) - 1
x_grid_acc, rho_acc, u_acc, p_acc = np.zeros(len_file), np.zeros(len_file), np.zeros(len_file), np.zeros(len_file)
for i in range(len_file):
    x_grid_acc[i] = float(filelines[i].split(" ")[0])
    rho_acc[i] = float(filelines[i].split(" ")[1])
    u_acc[i] = float(filelines[i].split(" ")[2])
    p_acc[i] = float(filelines[i].split(" ")[3])

axs[0].plot(x_grid_acc, rho_acc, "g")
axs[1].plot(x_grid_acc, u_acc, "g")
axs[2].plot(x_grid_acc, p_acc, "g")

axs[0].set_title(r"$\rho$")
axs[1].set_title("u")
axs[2].set_title("p")
plt.tight_layout()
plt.show()