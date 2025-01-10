import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

def general_failure_criterion_for_polymers(min_lambda=0.2, max_lambda=5, num_points=400):
    """
    计算聚合物的一般失效准则
    """


    lambda1 = np.linspace(min_lambda, max_lambda, num_points)
    lambda2 = np.linspace(min_lambda, max_lambda, num_points)
    L1, L2 = np.meshgrid(lambda1, lambda2)   

    L3 = 1 / (L2 * L1)

    I1 = L1 ** 2 + L2 ** 2 + L3 ** 2
    I2 = L1 ** 2 * L2 ** 2 + L2 ** 2 * L3 ** 2 + L3 ** 2 * L1 ** 2


    def F(gamma1, gamma2):
        return (I1 - 3) + gamma1 * (I1- 3) ** 2 + gamma2 * (I2 - 3)
    
    F_0_0_02 = F(0, 0.02)
    F_0_0_04 = F(0, 0.2)
    F_0_0_06 = F(0, 0.5)
    F_0_0_08 = F(0, 1)
    F_0_0_10 = F(0, 35)   


    # 创建图形
    plt.figure(figsize=(10, 8))

    # 绘制等效应力为sigma_yield的等高线
    # contour = plt.contour(L1, L2, F_0_0_02, levels=[10], colors='blue', linewidths=2)
    
    contour2 = plt.contour(L1, L2, F_0_0_04, levels=[20], colors='red', linewidths=2)
    contour3 = plt.contour(L1, L2, F_0_0_06, levels=[20], colors='green', linewidths=2)
    contour4 = plt.contour(L1, L2, F_0_0_08, levels=[20], colors='yellow', linewidths=2)
    contour5 = plt.contour(L1, L2, F_0_0_10, levels=[45], colors='purple', linewidths=2)
    # plt.clabel(contour, fmt='σ_eq = σ_yield', inline=True, fontsize=12)
    F_1_0_02 = F(1, 0.02)
    F_2_0_02 = F(2, 0.02)
    F_3_0_02 = F(3, 0.02)
    F_4_0_02 = F(4, 0.02)

    contour6 = plt.contour(L1, L2, F_0_0_02, levels=[20], colors='blue', linewidths=2, linestyles='dotted')
    contour7 = plt.contour(L1, L2, F_1_0_02, levels=[20], colors='red', linewidths=2, linestyles='dotted')
    contour8 = plt.contour(L1, L2, F_2_0_02, levels=[20], colors='green', linewidths=2, linestyles='dotted')
    contour9 = plt.contour(L1, L2, F_3_0_02, levels=[20], colors='yellow', linewidths=2, linestyles='dotted')
    contour10 = plt.contour(L1, L2, F_4_0_02, levels=[20], colors='purple', linewidths=2, linestyles='dotted')

   

    # 填充屈服区域（等效应力 <= sigma_yield）   
    # plt.contourf(L1, L2, F, levels=[0, K], colors=['lightblue'], alpha=0.5)

    # 绘制坐标轴
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    # 设置标签和标题
    # plt.xlabel('σ₁ (MPa)', fontsize=12)
    # plt.ylabel('σ₂ (MPa)', fontsize=12)
    # plt.title('二维冯·米塞斯屈服曲线 (σ₃ = 0)', fontsize=15)

    # # 设置轴的范围
    # plt.xlim(-sigma_max, sigma_max)
    # plt.ylim(-sigma_max, sigma_max)

    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.5)

    # Add λ₁=λ₂ line
    lambda_eq = np.linspace(min_lambda, max_lambda, 100)
    plt.plot(lambda_eq, lambda_eq, 'k--', label='λ₁=λ₂', linewidth=1.5)
    
    # Add λ₁λ₂²=1 curve
    lambda1_ps = np.linspace(min_lambda, max_lambda, 100)
    lambda2_ps = np.sqrt(1/lambda1_ps)
    plt.plot(lambda1_ps, lambda2_ps, 'k:', label='λ₁λ₂²=1', linewidth=1.5)
    
    # Add legend
    legend_elements = [
        Line2D([0], [0], color='blue', label='γ₂=0.02', linestyle='-'),
        Line2D([0], [0], color='red', label='γ₂=0.04', linestyle='-'),
        Line2D([0], [0], color='green', label='γ₂=0.06', linestyle='-'),
        Line2D([0], [0], color='yellow', label='γ₂=0.08', linestyle='-'),
        Line2D([0], [0], color='purple', label='γ₂=0.10', linestyle='-'),
        Line2D([0], [0], color='blue', label='γ₁=0, γ₂=0.02', linestyle='dotted'),
        Line2D([0], [0], color='red', label='γ₁=1, γ₂=0.02', linestyle='dotted'),
        Line2D([0], [0], color='green', label='γ₁=2, γ₂=0.02', linestyle='dotted'),
        Line2D([0], [0], color='yellow', label='γ₁=3, γ₂=0.02', linestyle='dotted'),
        Line2D([0], [0], color='purple', label='γ₁=4, γ₂=0.02', linestyle='dotted'),
        Line2D([0], [0], color='black', linestyle='--', label='λ₁=λ₂'),
        Line2D([0], [0], color='black', linestyle=':', label='λ₁λ₂²=1')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Add labels
    plt.xlabel('λ₁', fontsize=12)
    plt.ylabel('λ₂', fontsize=12)
    plt.title('General Failure Criterion for Polymers', fontsize=15)

    # Add specific points
    point1 = (2, 1/np.sqrt(2))
    point2 = (1.34, 1.28)
    
    plt.plot(point1[0], point1[1], 'ko', markersize=8, label='Point 1')  # black circle marker
    plt.plot(point2[0], point2[1], 'k^', markersize=8, label='Point 2')  # black triangle marker
    
    # Add annotations
    plt.annotate(f'({point1[0]:.2f}, {point1[1]:.2f})', 
                xy=point1, 
                xytext=(10, 10), 
                textcoords='offset points',
                fontsize=10)
    
    plt.annotate(f'({point2[0]:.2f}, {point2[1]:.2f})', 
                xy=point2, 
                xytext=(10, 10), 
                textcoords='offset points',
                fontsize=10)
    
    # Update legend_elements to include the new points
    legend_elements.extend([
        Line2D([0], [0], marker='o', color='w', markerfacecolor='black', markersize=8, label='Point 1'),
        Line2D([0], [0], marker='^', color='w', markerfacecolor='black', markersize=8, label='Point 2')
    ])

    # 显示图形
    plt.show()


if __name__ == "__main__":
    general_failure_criterion_for_polymers()
