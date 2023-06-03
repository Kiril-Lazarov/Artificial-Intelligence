import numpy as np
import matplotlib.pyplot as plt

def intersection_problem_plot():
    bodyA_pos = np.array([-4, -4])
    bodyB_pos_0 = np.array([3, -2])
    bodyB_pos_1 = np.array([2, 2])

    signal_0_pos = np.array([2.3, -2.2])
    signal_1_pos = np.array([3.2, 3.2])

    lineA_to_frame_0_x = [bodyA_pos[0], bodyB_pos_0[0]]
    lineA_to_frame_0_y = [bodyA_pos[1], bodyB_pos_0[1]]
    linaA_to_frame_1_x = [bodyA_pos[0], signal_1_pos[0]]
    linaA_to_frame_1_y = [bodyA_pos[1], signal_1_pos[1]]

    plt.scatter(bodyA_pos[0], bodyA_pos[1], s=200, color='blue')
    plt.scatter(bodyB_pos_0[0], bodyB_pos_0[1], s=100, color='orange')
    plt.scatter(bodyB_pos_1[0], bodyB_pos_1[1], s=100, color='orange')
    plt.scatter(signal_0_pos[0], signal_0_pos[1], color='gray')
    plt.scatter(signal_1_pos[0], signal_1_pos[1], color='gray')

    plt.text(bodyA_pos[0] - 0.5, bodyA_pos[1] - 0.5, 'A', fontsize=12, fontweight='bold')
    plt.text(bodyB_pos_0[0] - 0.3, bodyB_pos_0[1] - 0.8, 'B', fontsize=12, fontweight='bold')
    plt.text(bodyB_pos_1[0] - 0.3, bodyB_pos_1[1] - 0.8, 'B', fontsize=12, fontweight='bold')
    plt.text(bodyB_pos_0[0] + 0.4, bodyB_pos_0[1], 'Frame 0', fontsize=8)
    plt.text(bodyB_pos_1[0] + 0.4, bodyB_pos_1[1], 'Frame 1', fontsize=8)
    plt.text(signal_0_pos[0] - 2.5, signal_0_pos[1] + 0.5, 'Gravitational signal', fontsize=8)
    plt.text(signal_1_pos[0] - 2.5, signal_1_pos[1] + 0.5, 'Gravitational signal', fontsize=8)
    plt.text(2.4, 0, '?', fontsize=20)
    plt.text(1.5, -0.5, 'Point of intersection', fontsize=8)    
    
    plt.title('The point-of-intersection problem')

    plt.xlim(-5, 5)
    plt.ylim(-5, 5)

    plt.xlabel('X')
    plt.ylabel('Y')

    plt.plot(lineA_to_frame_0_x, lineA_to_frame_0_y, color='gray')
    plt.plot(linaA_to_frame_1_x, linaA_to_frame_1_y, color='gray')

    plt.show()