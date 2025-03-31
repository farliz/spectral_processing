import pandas as pd
from spectevol import SpectralProcessing, SpectralIndices
import matplotlib.pyplot as plt
import ipywidgets as widgets

# Create instances
process = SpectralProcessing('data')

process.main()
f = process.get_sedfiles()
process.view(f[0], 30)
data = process.get_data(f)

df = pd.DataFrame(data)
df.columns = range(350, 2501)


######## WIDGETS

@widgets.interact_manual(
curve = df.index)

def lineplot(curve):
    fig, ax = plt.subplots()
    ax.plot(range(len(df)), df[curve], label=str(curve))
    ax.legend()
    plt.show()


    
    plt.plot(xdata,line,'-k',xdata, ydata,'ok');
#plt.ticklabel_format(fontsize=16)
#plt.title("C Predicted vs C");
    plt.xlabel(var_x, fontsize=16);
    plt.ylabel(var_y, fontsize=16);
    # plt.title('$y=%3.7sx+%3.7s$'%(slope, intercept))
#plt.savefig('lregression.svg')



# Create instances

# planet
spectra = SpectralIndices("planet")
spectra.list_available_bands()

spectra.ndvi(df)
spectra.evi(df)
spectra.savi(df)
spectra.gci(df)

# sentinel-2 
spectra = SpectralIndices("sentinel-2")

print(spectra.sensor)
for n, (band, wavelength) in enumerate(spectra.bands.items(), start=1):
    print(f"Band {n}:{band}:  {wavelength}nm")
    
print(spectra.bands)
print(spectra.centerbands)

spectra.ndvi(df)
spectra.ndvi(df, nir='nira')
spectra.evi(df)
spectra.savi(df)
spectra.gci(df)


# oli
spectra = SpectralIndices("landsat-9")

print(spectra.sensor)
print(spectra.bands)
print(spectra.centerbands)

spectra.ndvi(df)
spectra.evi(df)
spectra.savi(df)
spectra.gci(df)

# landsat-7
spectra = SpectralIndices("landsat-7")

print(spectra.sensor)
print(spectra.bands)
print(spectra.centerbands)

spectra.ndvi(df)
spectra.evi(df)
spectra.savi(df)
spectra.gci(df)



fig, ax = plt.subplots()

for key, value in idf.items():
    ax.plot(value, label=key)
ax.legend()
plt.show()


########################


spectra1 = SpectralIndices("oli", method='average')

idf1 = {index_name: spectra1.compute_index(df, index_name) for index_name in indices}


fig, ax = plt.subplots()

for key, value in idf1.items():
    ax.plot(value, label=key)
ax.legend()
plt.show()



fig, ax = plt.subplots()
ax.plot(range(len(df)), idf['ndvi'], label='centerband')
ax.plot(range(len(df)), idf1['ndvi'], label='average')
ax.legend()
plt.show()
