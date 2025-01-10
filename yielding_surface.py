import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D

def plot_von_mises_yield_2d(sigma_yield=100, num_points=400, sigma_range=None):
    """
    绘制二维冯·米塞斯屈服曲线（σ₁ vs σ₂），假设σ₃ = 0。

    参数：
    - sigma_yield: 屈服应力（例如，300 MPa）。
    - num_points: 每个轴上的点数，用于生成网格。
    - sigma_range: 元组，定义应力范围，如(-sigma_max, sigma_max)。如果为None，则自动设置为1.5倍的sigma_yield。
    """
    if sigma_range is None:
        sigma_max = 1.5 * sigma_yield
    else:
        sigma_max = max(abs(sigma_range[0]), abs(sigma_range[1]))
    sigma1 = np.linspace(-sigma_max, sigma_max, num_points)
    sigma2 = np.linspace(-sigma_max, sigma_max, num_points)
    S1, S2 = np.meshgrid(sigma1, sigma2)

    # 计算冯·米塞斯等效应力
    sigma_eq = np.sqrt(S1**2 - S1*S2 + S2**2)

    # 创建图形
    plt.figure(figsize=(10, 8))

    # 绘制等效应力为sigma_yield的等高线
    contour = plt.contour(S1, S2, sigma_eq, levels=[sigma_yield], colors='blue', linewidths=2)
    plt.clabel(contour, fmt='σ_eq = σ_yield', inline=True, fontsize=12)

    # 填充屈服区域（等效应力 <= sigma_yield）
    plt.contourf(S1, S2, sigma_eq, levels=[0, sigma_yield], colors=['lightblue'], alpha=0.5)

    # 绘制坐标轴
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    # 设置标签和标题
    plt.xlabel('σ₁ (MPa)', fontsize=12)
    plt.ylabel('σ₂ (MPa)', fontsize=12)
    plt.title('二维冯·米塞斯屈服曲线 (σ₃ = 0)', fontsize=15)

    # 设置轴的范围
    plt.xlim(-sigma_max, sigma_max)
    plt.ylim(-sigma_max, sigma_max)

    # 添加网格
    plt.grid(True, linestyle='--', alpha=0.5)

    # 显示图形
    plt.show()




def plot_von_mises_yield_surface(sigma_max=100, num_points=100):
    def calculate_sigma3(sigma1, sigma2, sigma_Y):
        # Coefficients for the quadratic equation
        A = 2
        B = -2 * (sigma1 + sigma2)
        C = sigma1**2 + sigma2**2 - 2 * sigma_Y**2
        
        # Solve the quadratic equation: A*sigma3^2 + B*sigma3 + C = 0
        discriminant = B**2 - 4 * A * C
        if discriminant < 0:
            return None, None  # No real solutions
        else:
            # Calculate the two possible solutions for sigma3
            sigma3_pos = (-B + np.sqrt(discriminant)) / (2 * A)
            sigma3_neg = (-B - np.sqrt(discriminant)) / (2 * A)
            
            # Return the positive solution
            return sigma3_pos, sigma3_neg

    # Define the yield stress value
    sigma_Y = sigma_max  # Example yield stress value (in MPa or any other unit)

    # Create a meshgrid for sigma1 and sigma2
    sigma_range = np.linspace(-sigma_Y, sigma_Y, num_points)  # Range for the stresses
    sigma1, sigma2 = np.meshgrid(-sigma_range, sigma_range)

    # Calculate sigma3 for each combination of sigma1 and sigma2
    sigma3_pos = np.zeros_like(sigma1)
    sigma3_neg = np.zeros_like(sigma1)

    # Loop over each pair of sigma1 and sigma2 to calculate sigma3
    for i in range(len(sigma_range)):
        for j in range(len(sigma_range)):
            sigma3_pos[i, j] = calculate_sigma3(sigma1[i, j], sigma2[i, j], sigma_Y)[0]
            sigma3_neg[i, j] = calculate_sigma3(sigma1[i, j], sigma2[i, j], sigma_Y)[1]


    # Create a figure with two subplots
    fig = plt.figure(figsize=(15, 6))

    # 3D surface plot
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(sigma1, sigma2, sigma3_pos, cmap='coolwarm', alpha=0.8)
    surf2 = ax1.plot_surface(sigma1, sigma2, sigma3_neg, cmap='coolwarm', alpha=0.8)
    ax1.set_xlabel('σ₁ (MPa)')
    ax1.set_ylabel('σ₂ (MPa)')
    ax1.set_zlabel('σ₃ (MPa)')
    ax1.set_title('3D Von Mises Yield Surface')

    # Set equal scale for all axes
    x_lim = ax1.get_xlim3d()
    y_lim = ax1.get_ylim3d()
    z_lim = ax1.get_zlim3d()
    
    # Get the largest range to make all axes equal
    max_range = max(abs(high - low) for low, high in [x_lim, y_lim, z_lim])
    mid_x = np.mean(x_lim)
    mid_y = np.mean(y_lim)
    mid_z = np.mean(z_lim)
    
    # Set limits for equal scale
    ax1.set_xlim3d(mid_x - max_range/2, mid_x + max_range/2)
    ax1.set_ylim3d(mid_y - max_range/2, mid_y + max_range/2)
    ax1.set_zlim3d(mid_z - max_range/2, mid_z + max_range/2)
    
    # Set equal aspect ratio
    ax1.set_box_aspect([1, 1, 1])

    # Add hydrostatic stress line (σ₁=σ₂=σ₃)
    hydro_range = np.linspace(-sigma_Y, sigma_Y, 100)
    ax1.plot3D(hydro_range, hydro_range, hydro_range, 'r-', linewidth=2, 
            label='Hydrostatic stress line\n(σ₁=σ₂=σ₃)')
    ax1.legend()

    # Add colorbar
    plt.colorbar(surf, ax=ax1, label='σ₃ (MPa)')

    # 2D projection plot
    ax2 = fig.add_subplot(122)

    # Create contour plot for the projection
    contour = ax2.contour(sigma1, sigma2, sigma3_pos, levels=20, cmap='viridis')
    # contour2 = ax2.contour(sigma1, sigma2, sigma3_neg, levels=20, cmap='coolwarm')   
    ax2.clabel(contour, inline=True, fontsize=8)
    # ax2.clabel(contour2, inline=True, fontsize=8)

    # Add labels and title for 2D plot
    ax2.set_xlabel('σ₁ (MPa)')
    ax2.set_ylabel('σ₂ (MPa)')
    ax2.set_title('Von Mises Yield Surface\nProjection on σ₁-σ₂ Plane')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.axis('equal')

    # Add colorbar for the contour plot
    # plt.colorbar(contour2, ax=ax2, label='σ₃ (MPa)')

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the plots
    plt.show()



if __name__ == "__main__":
    plot_von_mises_yield_2d()
