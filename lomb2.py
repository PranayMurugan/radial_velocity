import matplotlib.pyplot as plt
from astropy.timeseries import LombScargle
import astropy.units as u
from scipy.signal import find_peaks
import numpy as np
import csv

t = []
r = []
dr = []
new_t = []

with open('/home/safesoccer/Projects/Planetary/RV_51Pegasi_Data.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=' ')
    for row in plots:
        t.append(float(row[0]))
        r.append(float(row[1]))
        dr.append(float(row[2]))

plt.scatter(t,r, label='Radial velocity')
plt.xlabel('Time period (in Julian days)')
plt.ylabel('Radial Velocity')
plt.title('Scatter plot')
plt.legend()
plt.show()

frequency, power = LombScargle(t, r, dr).autopower()
plt.plot(frequency, power)
plt.show()

peaks, height = find_peaks(power, height = 0.9)
y = 1/(frequency[peaks])
print(np.round(y,2))

i = 0

for x in t:
    new_t.append(x % y)

plt.errorbar(new_t, r, yerr = dr, fmt="o")
plt.xlabel('Time period')
plt.ylabel('Radial velocity')
plt.title('R_V curve')
plt.show()

