import os
import numpy as np
from matplotlib import pyplot as plt

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
    path = os.path.join(os.getcwd(), 'PIV_Group17/PIV_data')
    path_folder = os.path.join(path, folder_name)
    path_file = os.path.join(path_folder, 'B00001.dat')
    
    # Read the data from the file
    data = np.loadtxt(path_file, skiprows=3)
    
    # Extract the columns for x, y, Vx, Vy
    x, y, Vx, Vy = data[:, 0], data[:, 1], data[:, 2], data[:, 3]
    
    # Calculate the magnitude of the velocity vectors
    velocity_magnitude = np.sqrt(Vx**2 + Vy**2)
    
    # Create the velocity field plot
    plt.figure(figsize=(10, 8))
    quiver = plt.quiver(x, y, Vx, Vy, velocity_magnitude, angles='xy', scale_units='xy', scale=1, cmap='turbo', clim=(0, 15))
    plt.colorbar(quiver, label='Velocity Magnitude')
    plt.title(f'Velocity Field: {alpha}, {dt}, {mp_sp}, {resolution}, {overlap}, Time Mean: {time_mean}')
    plt.xlabel('X')
    plt.ylabel('Y')

def plot_mean_x_component_vs_y(alpha_values, dt, mp_sp, resolution, overlap, x_target=100):
    """
    New parameters:
    - x_target: float, the x value near which to plot the mean Vx component
    """
    # Initialize the plot
    plt.figure(figsize=(10, 8))
    
    for alpha in alpha_values:
        # Construct the folder name
        folder_name = f"{alpha}_{dt}_PIV_{mp_sp}({resolution}_{overlap})_PostProc_TimeMeanQF_Scalar"
        
        # Specify the path to the PIV data
        path = os.path.join(os.getcwd(), 'PIV_Group17/PIV_data')
        path_folder = os.path.join(path, folder_name)
        path_file = os.path.join(path_folder, 'B00001.dat')
        
        # Read the data from the file
        data = np.loadtxt(path_file, skiprows=3)
        
        # Extract the columns for x, y, Vx, Vy
        x, y, Vx = data[:, 0], data[:, 1], data[:, 2]
        
        # Find the indices where x is close to x_target
        indices = np.where(np.isclose(x, x_target, atol=1))
        
        # Extract the corresponding y and Vx values
        y_values = y[indices]
        Vx_values = Vx[indices]
        
        # Plot the mean x component (Vx) vs y distance
        plt.plot(Vx_values, y_values, 'o--', label=f'{alpha}')
    
    # Customize the plot
    plt.title(f'Mean X Component of Flow vs Y Distance near X={x_target}')
    plt.ylabel('Y Distance')
    plt.xlabel('Mean X Component of Flow (Vx)')
    plt.legend()
    plt.grid(True)

plot_velocity_field('0deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
plot_velocity_field('5deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
plot_velocity_field('15deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
# plot_velocity_field('15deg', '6microseconds', 'MP', '32x32', '50ov', time_mean=True)

plot_mean_x_component_vs_y(['0deg', '5deg', '15deg'], '75microseconds', 'MP', '32x32', '50ov', x_target=100)

plt.show()