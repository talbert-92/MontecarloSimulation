def monteCarloSim(param_sim,param_tol,param_dim):

    nn = param_sim 
    tol_groove_height_maj,tol_groove_widtht_min,tol_shaft_maj,tol_shaft_min,range_tol_Eh,range_tol_Ep,range_tol_R1,sigmaCap = param_tol 
    groove_width,shaft_diam,Eh,Ep,R1 = param_dim
    
    range_tol_height_groove = tol_groove_height_maj - tol_groove_height_min


    range_tol_width_groove = (-tol_groove_width_maj + tol_groove_widtht_min)/2
    groove_width = groove_width - range_tol_width_groove



    tol_shaft_range = (tol_shaft_maj - tol_shaft_min)/2
    shaft_diam = shaft_diam + tol_shaft_range + tol_shaft_min
    shaft_radius = shaft_diam/2

    min_shaft_diam = shaft_diam - tol_shaft_range
    max_shaft_diam = shaft_diam + tol_shaft_range

    min_shaft_radius = min_shaft_diam/2
    max_shaft_radius = max_shaft_diam/2




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


    gap = np.zeros(nn)
    n_offDesign = 0

    for ii in range(n):
        if gap_dx_pin[ii] > gap_dx_groove[ii] or gap_sx_pin[ii] < gap_sx_groove[ii]:
            minGap = min(gap_dx_groove[ii] - gap_dx_pin[ii], gap_sx_pin[ii] - gap_sx_groove[ii] )
            gap[ii] = minGap
            n_offDesign+=1
        else:
            minGap = min(gap_dx_groove[ii] - gap_dx_pin[ii], gap_sx_pin[ii] - gap_sx_groove[ii] )
            gap[ii] = minGap
            
    return n_offDesign


n = 10000 #n point simulation
n_lot = 10

groove_width = 2.5
shaft_diam = 2

tol_groove_height_maj = 0
tol_groove_height_min = 0.1

tol_groove_width_maj = 0
tol_groove_widtht_min = 0.1

tol_shaft_maj = 0.008
tol_shaft_min = 0.002

Eh = 14
Ep = 5.5
R1 = 7.2

range_tol_Eh = 0.1
range_tol_Ep = 0.1
range_tol_R1 = 0.1

sigmaCap = 3

measure_offPoints = np.zeros(n_lot)  
param_sim = [n]
param_tol = [tol_groove_height_maj,tol_groove_widtht_min,tol_shaft_maj,tol_shaft_min,range_tol_Eh,
             range_tol_Ep,range_tol_R1,sigmaCap]
param_dim = [groove_width,shaft_diam,Eh,Ep,R1]

tic = t.time()
for i in range(n_lot):
    measure_offPoints[i] = monteCarloSim(param_sim,param_tol,param_dim)
    

meanOffComponents = np.sum(measure_offPoints)/n_lot
toc = t.time()

print('off components each lot',measure_offPoints)
print("average components rejected:", meanOffComponents*100/n,'%')
print('')
print('elapsed time: \n',round(toc-tic,3),'s')