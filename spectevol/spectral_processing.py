import os
import random
import textwrap

import numpy as np
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt


class SpectralProcessing:

    """Class for spectral data processing from SED files."""

    def __init__(self, path='.'):
        """Initialize the class and set the path where .sed files are stored.

        :param path: str, the directory where the .sed files are
        located (default: current directory)

        """
        self.path = path  # Store the file path
        self.files = []
        self.data = None
        self.data_filtered = None

    def main(self):
        """Display the spectral processing menu."""
        text = textwrap.dedent(f"""\
        *****************************
        **** SPECTRAL PROCESSING ****
        **** UTM - INIAP - ESPAM ****

        Data Path: {self.path}

        1. Read the SED files.
           f = process.get_sedfiles()

        2. Inspect the content of a SED file.
           process.view(f[0], 30)

        3. Read all SED files and create a data array (2D).
           data = process.get_data(f)

        4. Plot some random curves.
           process.plot_random(data, 5)

        5. Smooth the data.
           data_filtered = process.smooth_data(data, window_length=11, polyorder=2)

        6. Compare raw and smoothed data.
           process.plot_diff(data, data_filtered, 6)

        7. To save the data, use:
           \n\033[1m np.savetxt('data.csv', data, delimiter=',', fmt='%.4f')\033[0m
        """)
        print(text)

    def get_sedfiles(self):
        """Retrieve the list of .sed files from the specified directory."""
        if not os.path.exists(self.path):
            print(f"Error: The path '{self.path}' does not exist.")
            return []

        self.files = sorted([file for file in os.listdir(self.path) if file.endswith('.sed')])

        if not self.files:
            print(f"No .sed files found in '{self.path}'.")
        else:
            print('\nFiles were successfully read!')
            print(f'{len(self.files)} .sed files were found.')

        return self.files

    def view(self, file, n=None):
        """Display the content of a SED file."""
        file_path = os.path.join(self.path, file)

        try:
            with open(file_path) as f:
                contents = f.readlines()
                for nline, textline in enumerate(contents):
                    if n is None:
                        print(nline, textline.strip())
                    elif nline <= n:
                        print(nline, textline.rstrip())
        except FileNotFoundError:
            print(f"\nError: The file '{file_path}' does not exist.")

    def get_data(self, files, n=27):
        """Load and process spectral data from SED files."""
        try:
            n = int(n)
        except ValueError:
            print('Error: The second argument must be a number')
            return None

        data = []
        for file in files:
            file_path = os.path.join(self.path, file)
            try:
                with open(file_path) as f:
                    contents = f.readlines()
                    for nline, textline in enumerate(contents):
                        if n is None:
                            data.append(textline.strip())
                        elif nline >= n:
                            data.append(float(textline.rstrip().split("\t")[1]))
            except FileNotFoundError:
                print(f"\nError: The file '{file_path}' does not exist.")

        if not data:
            print("No valid data found.")
            return None

        self.data = np.reshape(data, (int(len(data) / 2151), 2151))
        print('\nFiles were successfully loaded!')
        print(f'The dataset has {self.data.shape[0]} rows and {self.data.shape[1]} columns.')
        return self.data.round(3)

    def smooth_data(self, data, window_length=11, polyorder=2):
        """Apply Savitzky-Golay filter for data smoothing."""
        self.data_filtered = savgol_filter(data, window_length, polyorder, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0)
        print("Data successfully smoothed!")
        return self.data_filtered

    def plot_random(self, array, k=5):
        """Plot random spectral curves."""
    
        samples = random.sample(range(len(array)), k)
            
        fig, ax = plt.subplots(figsize=(9, 5))
        for i in samples:
            ax.plot(array[i], linewidth=1.5)
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Reflectance (%)')
        ax.set_xticks(range(0, array.shape[1] + 49, 150))
        ax.set_xticklabels(range(350, 2561, 150))
        ax.legend(samples, fontsize=7)
        plt.show()

    def plot_diff(self, array, array_filtered, n):
        """Plot a raw vs. filtered spectral curve."""
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(array[n], linewidth=1.5, label='Raw')
        ax.plot(array_filtered[n], linewidth=1.5, label='Filtered')
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Reflectance (%)')
        ax.set_xticks(range(0, array.shape[1] + 1, 200))
        ax.set_xticklabels(range(350, 2501, 200))
        ax.legend(fontsize=7)
        plt.title(f'Raw and filtered sample: {n}', loc='left', fontsize=7)
        plt.show()


# # Run the program
# if __name__ == '__main__':
#     # Change the path if needed (default is current directory)
#     process = SpectralProcessing(path='data')  # Example: Change to where .sed files are stored
#     process.main()
