import numpy as np
import matplotlib.pyplot as plt

# sigma = 0.25
# x, y = np.linspace(0, 1, 100), np.linspace(0, 1, 100)
# X, Y = [], []

# for x_ in x:
#     for y_ in y:
#         alpha1_1 = (sigma + 1 - x_ * (2 - sigma) - y_) / (2 + sigma)
#         if alpha1_1 >= 0:
#             alpha01 = 1 - x_ - y_ - alpha1_1
#             if alpha01 >= 0:
#                 X.append(x_)
#                 Y.append(y_)

# plt.subplot()
# plt.xlim(-1, 3)
# plt.ylim(-1, 3)
# plt.plot(X, Y, "r*")
# plt.show()


with open("C://My_Progs//nvp//Accurate_solution//Accurate_solution//Exact_solution//Exact_solution//exact_solution.dat", "r") as file:
    filelines = file.read().split("\n")
len_file = len(filelines) - 1
x_grid_acc, rho_acc, u_acc, p_acc = np.zeros(len_file), np.zeros(len_file), np.zeros(len_file), np.zeros(len_file)
for i in range(len_file):
    print(filelines[i].split(" ")[0])
    x_grid_acc[i] = float(filelines[i].split(" ")[0])
    rho_acc[i] = float(filelines[i].split(" ")[1])
    u_acc[i] = float(filelines[i].split(" ")[2])
    p_acc[i] = float(filelines[i].split(" ")[3])