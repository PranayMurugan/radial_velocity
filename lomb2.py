""" This program takes the data in the form of radial velocity and the time (in Julian days) at which the data was recorded,
and applies Lomb-Scargle Periodogram, and finding the orbital time period,
after finding the time period the radial velocity is folded to get the radial_velocity curve
"""
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

# Read the data file as a csv

with open('/home/safesoccer/Projects/Planetary/RV_51Pegasi_Data.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=' ')
    for row in plots:
        t.append(float(row[0]))
        r.append(float(row[1]))
        dr.append(float(row[2]))

# simple scatter plot of the raw data

plt.scatter(t,r, label='Radial velocity')
plt.xlabel('Time period (in Julian days)')
plt.ylabel('Radial Velocity')
plt.title('Scatter plot')
plt.legend()
plt.show()

# Apply LombScargle Periodogram to find orbital time period

frequency, power = LombScargle(t, r, dr).autopower()
plt.plot(frequency, power)
plt.show()

# Find the peak in the LombScargle probablity distribution

peaks, height = find_peaks(power, height = 0.9)  # height = 0.9 refers the 90% probablity
y = 1/(frequency[peaks])
print(np.round(y,2))

i = 0

for x in t:
    new_t.append(x % y)

# Radial-velocity curve plotted

plt.errorbar(new_t, r, yerr = dr, fmt="o")
plt.xlabel('Time period')
plt.ylabel('Radial velocity')
plt.title('R_V curve')
plt.show()

