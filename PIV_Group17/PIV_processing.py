import os
import numpy as np
from matplotlib import pyplot as plt

def plot_velocity_field(alpha, dt, mp_sp, resolution, overlap, time_mean=False):
    """
    Plot the velocity field for the specified parameters.

    Parameters:
    - alpha: str, angle in degrees (e.g., '0deg', '5deg', '15deg')
    - dt: str, time step (e.g., '75microseconds', '6microseconds')
    - mp_sp: str, 'MP' or 'SP'
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
    
    # Create a quiver plot with a color scale for the magnitude of the velocity
    plt.figure(figsize=(10, 8))
    quiver = plt.quiver(x, y, Vx, Vy, velocity_magnitude, angles='xy', scale_units='xy', scale=1, cmap='turbo', clim=(0, 15))
    plt.colorbar(quiver, label='Velocity Magnitude')
    plt.title(f'Velocity Field: {folder_name}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    plt.show()

plot_velocity_field('0deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
plot_velocity_field('5deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)
plot_velocity_field('15deg', '75microseconds', 'MP', '32x32', '50ov', time_mean=True)