import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from astropy.stats import LombScargle
from scipy.optimize import curve_fit,fsolve
import csv

jd = []
rv = []
er = []


def keplerian_fit(t,K,P,e,w,tau,vr0):
  e_anomaly = solve_kepler((t-tau)*2*np.pi/P,e)
  theta = 2*np.arctan2(np.sqrt(1.+e)*np.sin(0.5*e_anomaly),
                       np.sqrt(1.-e)*np.cos(0.5*e_anomaly))
  return K*(np.cos(theta+w)+e*np.cos(w))+vr0

def solve_kepler(M,e):
  eanom = np.zeros(M.shape)
  for i,mi in enumerate(M):
    # do iterative root solve with e=0 giving E=M as guess
    tmp,=fsolve(lambda E: E-e*np.sin(E)-mi,mi)
    eanom[i] = tmp
  return eanom

ms       = 1.12
ms_error = 0.06

fname = 'RV_51Pegasi_Data.txt' #'HAT-P-11b.txt' #'HATS-1b.txt'
data = np.genfromtxt(fname,skip_header=21,autostrip=True)
jd = data[:,0]
rv = data[:,1]
er = data[:,2]

# make plot of the RV data
fig1=plt.figure(figsize=(4,3))
axes = fig1.add_axes([0.14,0.14,0.85,0.78])
axes.plot(jd,rv,'.k')
plt.title('Scatter plot of radial velocity for 51 Peg b')
plt.xlabel('Time period in Julian days')
plt.ylabel('Radial velocity (m/s)')
plt.show()

frequency,power = LombScargle(jd,rv,er).autopower()#maximum_frequency=1,minimum_frequency=0.001)

fig2=plt.figure(figsize=(4,3))
axes = fig2.add_axes([0.14,0.14,0.85,0.78])
axes.semilogx(1./frequency,power,'k')
plt.title('Lomb-Scargle periodogram for 51 Peg b')
plt.xlabel('time period (julian days)')
plt.ylabel('power')
plt.show()


period = 1/frequency[np.argmax(power)]
print("The fit period is %10.5f days" % period)

tfit = np.linspace(0,period,1000)
rvfit = LombScargle(jd,rv,er).model(tfit,1/period)
semi_amplitude = 0.5*(np.max(rvfit)-np.min(rvfit))
print("The fit semi-amplitude is %10.5f m/s" % semi_amplitude)
phase = (jd % period)

voffset = np.mean(rvfit)
print("The velocity offset is %10.5f m/s" % voffset)


fig3=plt.figure(figsize=(4,3))
axes = fig3.add_axes([0.14,0.14,0.85,0.78])
axes.errorbar(phase,rv,er,fmt='.k')
axes.plot(tfit,rvfit,'-k')
plt.title('RV curve for 51 Peg b')
plt.xlabel('time (days)')
plt.ylabel('radial velocity (m/s)')
plt.yticks([-75,-50,-25,0,25,50,75])
plt.show()

K = semi_amplitude
P = period
e = 0.
w = 0.
tau = jd[np.argmax(rv)]
vr0 = voffset
guess = (K,P,e,w,tau,vr0)

rvfit = keplerian_fit(jd,K,P,e,w,tau,vr0)
chisq = np.sum(((rv-rvfit)/er)**2)
print("Chi-squared of initial guess is %10.5f" % chisq)

popt,pcov = curve_fit(keplerian_fit,jd,rv,
                      sigma=er,absolute_sigma=True,
                      p0=guess)

(K,P,e,w,tau,vr0) = popt
print(popt)
rvfit = keplerian_fit(jd,K,P,e,w,tau,vr0)
chisq = np.sum(((rv-rvfit)/er)**2)
print("Chi-squared of least-squares fit is %10.5f" % chisq)

tfit = np.linspace(0,P,1000)
rvfit = keplerian_fit(tfit,K,P,e,w,tau,vr0)
phase = (jd % P)

fig4=plt.figure(figsize=(4,3))
axes = fig4.add_axes([0.14,0.14,0.85,0.78])
axes.errorbar(phase,rv,er,fmt='.k')
axes.plot(tfit,rvfit,'-k')
plt.title('phased RV data for 51 Peg b')
plt.xlabel('time (days)')
plt.ylabel('radial velocity (m/s)')
plt.show()

if e<0:
  w -= np.pi
  e *= -1

if K<0:
  K *= -1
  w += np.pi


P_yr   = P/365.2422                    # period in years
a_au   = (ms*P_yr**2)**(1./3)          # semi-major axis in au
K_auyr = K*2.1096256684e-4             # K in au/yr

mp      = (2*np.pi)**(-1)*K_auyr*np.sqrt(1-e**2)*(ms**2*P_yr)**(1/3)
mp_mjup = mp*1047.59421               # convert to Jupiter mass

w_deg = w*180/np.pi

K_error   = np.sqrt(pcov[0,0])
P_error   = np.sqrt(pcov[1,1])
e_error   = np.sqrt(pcov[2,2])
w_error   = np.sqrt(pcov[3,3])
tau_error = np.sqrt(pcov[4,4])
a_error   = a_au * np.sqrt( (2*P_error/(3*P))**2 + (ms_error/(3*ms))**2 )
mp_error  = mp_mjup * np.sqrt( (2*ms_error/(3*ms))**2 + (K_error/K)**2
                             + (P_error/(3*P))**2 + (e*e_error/np.sqrt(1-e*e))**2 )

print(K_error,P_error,e_error,w_error,tau_error,a_error,mp_error)
