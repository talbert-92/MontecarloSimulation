import numpy as np
import matplotlib.pyplot as plt
import time as t
import colorcet as cc
import matplotlib.colors as colors
from fast_histogram import histogram2d
%matplotlib inline 

fact_rad_deg = 180/np.pi
fact_deg_rad = np.pi/180


tic = t.time()

n = 10000                 #n point simulation
n_lot = 5

groove_width = 2.5
shaft_diam = 2

tol_groove_height_maj = 0
tol_groove_height_min = 0.1
range_tol_height_groove = tol_groove_height_maj - tol_groove_height_min

tol_groove_width_maj = 0
tol_groove_widtht_min = 0.1
range_tol_width_groove = (-tol_groove_width_maj + tol_groove_widtht_min)/2
groove_width = groove_width - range_tol_width_groove

tol_shaft_maj = 0.008
tol_shaft_min = 0.002

tol_shaft_range = (tol_shaft_maj - tol_shaft_min)/2
shaft_diam = shaft_diam + tol_shaft_range + tol_shaft_min
shaft_radius = shaft_diam/2

min_shaft_diam = shaft_diam - tol_shaft_range
max_shaft_diam = shaft_diam + tol_shaft_range

min_shaft_radius = min_shaft_diam/2
max_shaft_radius = max_shaft_diam/2


Eh = 14
Ep = 5.5
R1 = 7.2

range_tol_Eh = 0.1
range_tol_Ep = 0.1
range_tol_R1 = 0.1

sigmaCap = 6

SD_Eh_sigma = (range_tol_Eh)/sigmaCap
SD_Ep_sigma = (range_tol_Ep)/sigmaCap
SD_R1_sigma = (range_tol_R1)/sigmaCap
SD_pin_sigma = (tol_shaft_range)/sigmaCap
SD_groove_sigma = (range_tol_width_groove)/sigmaCap

Eh_norm = np.random.normal(Eh,SD_Eh_sigma,n) 
Ep_norm = np.random.normal(Ep,SD_Ep_sigma,n) 
R1_norm = np.random.normal(R1,SD_R1_sigma,n)
shaft_radius_norm = np.random.normal(shaft_radius,SD_pin_sigma,n)
groove_width_norm = np.random.normal(groove_width,SD_groove_sigma,n)

position_pin_X = Eh_norm - Ep_norm 

gap_dx_pin = Ep_norm + shaft_radius_norm
gap_sx_pin = Ep_norm - shaft_radius_norm

gap_dx_groove = Eh_norm - R1_norm
gap_sx_groove = Eh_norm - R1_norm - groove_width_norm


gap = np.zeros(n)
n_offDesign = 0

for ii in range(n):
    if gap_dx_pin[ii] > gap_dx_groove[ii] or gap_sx_pin[ii] < gap_sx_groove[ii]:
        minGap = min(gap_dx_groove[ii] - gap_dx_pin[ii], gap_sx_pin[ii] - gap_sx_groove[ii] )
        gap[ii] = minGap
        n_offDesign+=1
    else:
        minGap = min(gap_dx_groove[ii] - gap_dx_pin[ii], gap_sx_pin[ii] - gap_sx_groove[ii] )
        gap[ii] = minGap
        
            
complGap = groove_width_norm - minGap - shaft_radius_norm*2



fig2,ax = plt.subplots(1,ncols=2,figsize = (14, 8))
ax = ax.ravel()
ax[0].hist(groove_width_norm, bins=30,color='gray',ec='white')
ax[0].set_title('Distribution of \n Groove diameter')
ax[0].set_xlabel('mm')
ax[0].set_axisbelow(True)
ax[0].xaxis.grid(color='gray', linestyle='dashed')
ax[0].yaxis.grid(color='gray', linestyle='dashed')

ax[1].hist(shaft_radius_norm*2, bins=30,color='purple',ec='white')
ax[1].set_title('Distribution of \n Pin diameter')
ax[1].set_xlabel('mm')
ax[1].set_axisbelow(True)
ax[1].xaxis.grid(color='gray', linestyle='dashed')
ax[1].yaxis.grid(color='gray', linestyle='dashed')




plt.tight_layout()


fig3,ax = plt.subplots(1,ncols=2,figsize = (14, 8))
ax = ax.ravel()
ax[0].hist(gap, bins=40,color='black',ec='white')
ax[0].set_title('Distribution of \n Minimum gap')
ax[0].set_xlabel('mm')
ax[0].set_axisbelow(True)
ax[0].xaxis.grid(color='gray', linestyle='dashed')
ax[0].yaxis.grid(color='gray', linestyle='dashed')

ax = ax.ravel()
ax[1].hist(complGap, bins=40,color='green',ec='white')
ax[1].set_title('Distribution of \n Complementary gap')
ax[1].set_xlabel('mm')
ax[1].set_axisbelow(True)
ax[1].xaxis.grid(color='gray', linestyle='dashed')
ax[1].yaxis.grid(color='gray', linestyle='dashed')


plt.tight_layout()

print('# Off components:',n_offDesign)
print('% Off components:',n_offDesign/n*100)

toc = t.time()

print('elapsed time: \n',round(toc-tic,3),'s')
