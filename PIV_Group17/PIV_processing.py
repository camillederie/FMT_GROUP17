import os
import numpy as np
from matplotlib import pyplot as plt
import mplcursors

def plot_velocity_field(alpha, dt, mp_sp, resolution, overlap, time_mean=False):
    """
    !!! Make sure that you are in the FMT_Group17 directory !!!

    Parameters:
    - alpha: str, angle in degrees (e.g., '0deg', '5deg', '15deg')
    - dt: str, time step (e.g., '75microseconds', '6microseconds')
    - Multi or Single: str, 'MP' or 'SP'
    - resolution: str, resolution (e.g., '32x32', '16x16', '64x64')
    - overlap: str, overlap percentage (e.g., '50ov', '0ov')
    - time_mean: bool, whether to use TimeMeanQF data
    """
    # Construct the folder name
    time_mean_str = '_TimeMeanQF_Vector' if time_mean else ''
    folder_name = f"{alpha}_{dt}_PIV_{mp_sp}({resolution}_{overlap})_PostProc{time_mean_str}"
    
    # Specify the path to the PIV data
    path = os.path.join(os.getcwd(), 'PIV_data')
    path_folder = os.path.join(path, folder_name)
    path_file = os.path.join(path_folder, 'B00001.dat')
    
    # Read the data from the file
    data = np.loadtxt(path_file, skiprows=3)
    
    # Extract the columns for x, y, Vx, Vy
    x, y, Vx, Vy = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    
    # Calculate the magnitude of the velocity vectors
    velocity_magnitude = np.sqrt(Vx**2 + Vy**2)
    print(Vx.shape)
    # Filter out anomalies
    # for i in range(len(Vx)):
    #     if velocity_magnitude[i] > 15:
    #         Vx[i] = 0
    #         Vy[i] = 0
    #         velocity_magnitude[i] = 0

    # Create the velocity field plot
    # plt.figure(figsize=(10, 8))
    plt.figure()
    quiver = plt.quiver(x, y, Vx, Vy, velocity_magnitude, angles='xy', scale_units='xy', scale=1, cmap='turbo',
                        clim=(0, 15))
    plt.colorbar(quiver, label='Velocity Magnitude [m/s]')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().invert_yaxis()

    # Add interactive tooltips
    cursor = mplcursors.cursor(quiver, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        index = sel.index
        # Calculate the 2D index from the flattened index
        i, j = np.divmod(index, x.size)
        sel.annotation.set_text(f'({x[j]}, {y[i]})\nVelocity: {velocity_magnitude[index]:.2f} m/s')

    plt.show()
    
    # Save the plot
    figures_path = os.path.join(os.getcwd(), 'Figures')
    plt.savefig(os.path.join(figures_path, f'velocity_field_{alpha}_{dt}_{mp_sp}_{resolution}_{overlap}_time_mean_{time_mean}.png'))
    plt.close()

def plot_mean_x_component_vs_y(alpha_values, dt, mp_sp, resolution, overlap, x_target=100):
    """
    New parameters:
    - x_target: float, the x value near which to plot the mean Vx component
    """
    # Initialize the plot
    plt.figure(figsize=(10, 8))
    # plt.figure()
    
    for alpha in alpha_values:
        # Construct the folder name
        folder_name = f"{alpha}_{dt}_PIV_{mp_sp}({resolution}_{overlap})_PostProc_TimeMeanQF_Scalar"
        
        # Specify the path to the PIV data
        path = os.path.join(os.getcwd(), 'PIV_Group17/PIV_data')
        path_folder = os.path.join(path, folder_name)
        path_file = os.path.join(path_folder, 'B00001.dat')
        
        # Read the data from the file
        data = np.loadtxt(path_file, skiprows=3)
        
        # Extract the columns for x, y, Vx
        x, y, Vx = data[:, 0], data[:, 1], data[:, 2]
        
        # Find the indices where x is close to x_target
        indices = np.where(np.isclose(x, x_target, atol=1))
        
        # Extract the corresponding y and Vx values
        y_values = y[indices]
        Vx_values = Vx[indices]
        
        # Plot the mean x component (Vx) vs y distance as scatter with dashed line
        plt.plot(Vx_values, y_values, 'o--', label=f'{alpha}')
    
    # Customize the plot
    # plt.title(f'Mean X Component of Flow vs Y Distance near X={x_target}')
    plt.ylabel('Y Distance')
    plt.xlabel('Mean X Component of Flow (Vx) [m/s]')
    plt.gca().invert_yaxis()
    plt.legend()
    plt.grid(True)
    
    # Save the plot
    figures_path = os.path.join(os.getcwd(), 'PIV_Group17/Figures')
    plt.savefig(os.path.join(figures_path, f'mean_x_component_vs_y_{dt}_{mp_sp}_{resolution}_{overlap}_x_target_{x_target}.png'))
    plt.close()


# plot_velocity_field('0deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
# plot_velocity_field('0deg', '75microseconds', 'SP', '32x32', '50ov', time_mean=False)
# plot_velocity_field('5deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
plot_velocity_field('15deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)

# plot_velocity_field('15deg', '6microseconds', 'MP', '32x32', '50ov', time_mean=True)

# plot_velocity_field('0deg', '75microseconds', 'SP', '16x16', '0ov', time_mean=False)
# plot_velocity_field('0deg', '75microseconds', 'SP', '32x32', '0ov', time_mean=False)
# plot_velocity_field('0deg', '75microseconds', 'SP', '64x64', '0ov', time_mean=False)

# plot_mean_x_component_vs_y(['0deg', '5deg', '15deg'], '75microseconds', 'MP', '32x32', '50ov', x_target=25)
# plot_mean_x_component_vs_y(['0deg', '5deg', '15deg'], '75microseconds', 'MP', '32x32', '50ov', x_target=100)

# plot_velocity_field('0deg', '75microseconds', 'SP', '32x32', '50ov', time_mean=False)
