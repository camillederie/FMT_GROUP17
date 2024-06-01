import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

angles = [0, 5, 15]
# vertical positions are a list of value form -40 to 40 in steps of 4
vertical_positions = [-40, -36, -32, -28, -24, -20, -16, -12, -8, -4, 0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40]
# read data files and process data
def read_data(file_path):
    # skip 23 rows, column 1 is the x-value and 2 is the value

    data = pd.read_csv(file_path, skiprows=23, sep='\t', header=None, names=['x', 'y'])
    return data
data_all = {}
for i in vertical_positions:

    filepath = f'HWA_Group17\Data\Measurement_{i}_+05.txt'
    data = read_data(filepath)
    data_all[f'Measurement_{i}_5'] = data

    filepath = f'HWA_Group17\Data\Measurement_{i}_+15.txt'
    data = read_data(filepath)
    data_all[f'Measurement_{i}_15'] = data

    filepath = f'HWA_Group17\Data\Measurement_{i}_+00.txt'
    data = read_data(filepath)
    data_all[f'Measurement_{i}_0'] = data

print(data_all.keys())
print(data_all['Measurement_-40_5'])
mean_voltage = {}
for k in angles:
    mean_voltage[f'{k}'] = []
    for i in vertical_positions:
        mean_voltage[f'{k}'].append(np.mean(data_all[f'Measurement_{i}_{k}']['y']))
        #print(f'{i} has mean voltage of {np.mean(data_all[i]["y"])}')
# plot the data

    plt.plot(mean_voltage[f'{k}'], vertical_positions, label=f'{k} degrees')
plt.ylabel('Vertical Position')
plt.xlabel('Mean Voltage')
plt.title('Mean Voltage vs Vertical Position')
plt.legend()
plt.show()