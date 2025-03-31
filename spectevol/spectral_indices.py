import numpy as np
import pandas as pd

class SpectralIndices:
    """Class for computing vegetation indices from spectral reflectance data."""

    def __init__(self, sensor, method="centerband"):
        """
        Initialize the SpectralIndices class with the specified sensor.

        :param sensor: str, name of the sensor ('general', 'oli', 'sentinel-2')
        :param method: str, method for NDVI calculation ('centerband' or 'average')

        The data about the sensors was obtained from official sources:
        - Landsat-7 ETM+: https://www.usgs.gov/faqs/what-are-band-designations-landsat-satellites
        - Landsat 8 OLI: https://www.usgs.gov/media/files/landsat-8-data-users-handbook
        - Landsat 9 OLI-2: https://www.usgs.gov/media/files/landsat-9-data-users-handbook
        """
        if method not in ["centerband", "average"]:
            raise ValueError("Method must be either 'centerband' or 'average'.")

        if (sensor == 'sentinel-2' and method == 'average'):
            raise ValueError("Sentinel-2 only works with centerband method")

        self.sensor = sensor
        self.method = method
        self.bands = self.get_sensor_bands()
        self.centerbands = self.get_centerband()

    def get_sensor_bands(self):
        """Assign band wavelength ranges based on the sensor."""
        sensors = {
            "general": {'blue': (450, 520), 'green': (521, 600), 'red': (601, 690), 'nir': (700, 800)},
            "landsat-8": {'aerosol': (435, 451), 'blue': (452, 512), 'green': (533, 590), 'red': (636, 673),
                    'nir': (851, 879), 'swir1': (1566, 1651), 'swir2': (2107, 2294), 'cirrus': (1363, 1384)},
            "landsat-9": {'aerosol': (435, 451), 'blue': (452, 512), 'green': (533, 590), 'red': (636, 673),
                    'nir': (851, 879), 'swir1': (1566, 1651), 'swir2': (2107, 2294), 'cirrus': (1363, 1384)},
            "landsat-7": {'blue': (450, 515), 'green': (525, 605), 'red': (630, 690),
                    'nir': (775, 900), 'swir1': (1550, 1750), 'swir2': (2090, 2350), 'pan': (520, 900)},
            "sentinel-2": {'aerosol': (443), 'blue': (490), 'green': (560), 'red': (665), 'red-edge': (705),
                           'nir': (842), 'nira': (865), 'nir1': (740), 'nir2': (783), 'water_vapour': (945),
                           'cirrus': (1375), 'swir1': (1610), 'swir2': (2190)},
            "planet": {'coastal': (431, 452), 'blue': (465, 515), 'green1': (513, 549), 'green': (547, 583),
                       'yellow': (600, 620), 'red': (650, 680), 'red-edge': (697, 713), 'nir': (845, 885)}
        }

        return sensors.get(self.sensor, None)

    def list_available_bands(self):
        """Human readable list of sensor bands"""
        print(f"Sensor: {self.sensor}")
        for n, (band, wavelength) in enumerate(self.bands.items(), start=1):
            print(f"Band {n}:{band}:  {wavelength}nm")
    
    def get_centerband(self):
        """Calculate the mean (center) wavelength for each band."""
        if not self.bands:
            raise ValueError(f"Sensor '{self.sensor}' not found in database.")

        if self.sensor == 'sentinel-2':
            return {band: wavelength for band, wavelength in self.bands.items()}
        else:
            return {band: int((wavelength[0] + wavelength[1]) / 2) for band, wavelength in self.bands.items()}

    def _get_band_values(self, df, band_name):
        """Retrieve band values based on the selected method ('centerband' or 'average')."""
        if self.method == "centerband":
            return df[self.centerbands[band_name]]
        elif self.method == "average":
            band_range = self.bands[band_name]
            return df.loc[:, (df.columns >= band_range[0]) & (df.columns <= band_range[1])].mean(axis=1)

    def ndvi(self, df, nir='nir'):
        """Compute NDVI (Normalized Difference Vegetation Index)."""
        nir = self._get_band_values(df, nir)
        red = self._get_band_values(df, "red")
        return (nir - red) / (nir + red + 1e-10)

    def evi(self, df, L=1, C1=6, C2=7.5, G=2.5):
        """Compute EVI (Enhanced Vegetation Index)."""
        nir = self._get_band_values(df, "nir")
        red = self._get_band_values(df, "red")
        blue = self._get_band_values(df, "blue")
        return G * ((nir - red) / (nir + C1 * red - C2 * blue + L + 1e-10))

    def savi(self, df, L=0.5):
        """Compute SAVI (Soil-Adjusted Vegetation Index)."""
        nir = self._get_band_values(df, "nir")
        red = self._get_band_values(df, "red")
        return ((nir - red) / (nir + red + L + 1e-10)) * (1 + L)

    def msavi(self, df):
        """Compute MSAVI (Modified Soil-Adjusted Vegetation Index)."""
        nir = self._get_band_values(df, "nir")
        red = self._get_band_values(df, "red")
        return (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2

    def gci(self, df):
        """Compute GCI (Green Chlorophyll Index)."""
        nir = self._get_band_values(df, "nir")
        green = self._get_band_values(df, "green")
        return (nir / green) - 1

    def list_available_indices(self):
        """Print a list of all available vegetation indices."""
        indices = {
            "NDVI": "Normalized Difference Vegetation Index",
            "EVI": "Enhanced Vegetation Index",
            "SAVI": "Soil-Adjusted Vegetation Index",
            "MSAVI": "Modified Soil-Adjusted Vegetation Index",
            "GCI": "Green Chlorophyll Index"
        }

        print("\n📌 Available Spectral Indices:")
        for key, description in indices.items():
            print(f"✅ {key}: {description}")
