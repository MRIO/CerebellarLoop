from E_New_Plasticity import *

# rewrite name of voltage and plasticity variables to specificly save it with the right name
#convert str to list 

# load data file and append new 
dat = h5py.File(NameFile,'a')


name = str(int(frequencyInput1))+'and'+str(int(frequencyInput2))+'Hz'
if name in dat:
    sim_group = dat[name].create_group(typeOfRun)
else :
    freq_group = dat.create_group(name)
    sim_group = freq_group.create_group(typeOfRun)


# type definition for variable shaped data
dt_type = h5py.vlen_dtype(np.dtype('float64'))

# Create subgroups for the different data stored
volt_cell = sim_group.create_group('Voltage_Cells')
spikes = sim_group.create_group('Spikes')
popul = sim_group.create_group('Population_rate')
inputs = sim_group.create_group('Input')
Params = sim_group.create_group('PV')

# Create dataset for the cells
vIO=volt_cell.create_dataset('IOsoma_coupled',data=IO_Statemon_Coupled_STDP.Vs)
vIOu=volt_cell.create_dataset('IOsoma_uncoupled',data=IO_Statemon_Uncoupled_STDP.Vs)
vDCN = volt_cell.create_dataset('DCN_coupled', data=DCN_Statemon_Coupled_STDP.v)
vDCNu = volt_cell.create_dataset('DCN_uncoupled', data=DCN_Statemon_Uncoupled_STDP.v)
vPC = volt_cell.create_dataset('PC_coupled',data=PC_Statemon_Coupled_STDP.v)
vPCu = volt_cell.create_dataset('PC_uncoupled',data=PC_Statemon_Uncoupled_STDP.v)

# input parameters
I = inputs.create_dataset('I',data=Noise_extended_statemon.I)
weight = inputs.create_dataset('weight',data=mon_N_PC_Coupled.new_weight)
I_PC = inputs.create_dataset('I_InputPC_coupled', data=PC_Statemon_Coupled_STDP.I_Noise)
I_PCu = inputs.create_dataset('I_InputPC_uncoupled', data=PC_Statemon_Uncoupled_STDP.I_Noise)

# Spike Times
S_PC = spikes.create_dataset('PC_coupled',data=list(PC_Spikemon_Coupled_STDP.spike_trains().values()),dtype=dt_type)
S_PCu = spikes.create_dataset('PC_uncoupled',data=list(PC_Spikemon_Uncoupled_STDP.spike_trains().values()),dtype=dt_type)
S_IO = spikes.create_dataset('IO_coupled',data=list(IO_Spikemon_Coupled_STDP.spike_trains().values()),dtype=dt_type)
S_IOu = spikes.create_dataset('IO_uncoupled',data=list(IO_Spikemon_Uncoupled_STDP.spike_trains().values()),dtype=dt_type) 
S_DCN = spikes.create_dataset('DCN_coupled',data=list(DCN_Spikemon_Coupled_STDP.spike_trains().values()),dtype=dt_type)
S_DCNu = spikes.create_dataset('DCN_uncoupled',data=list(DCN_Spikemon_Uncoupled_STDP.spike_trains().values()),dtype=dt_type)

# Population Rates
pPC = popul.create_dataset('PC_coupled',data=PC_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pPCu = popul.create_dataset('PC_uncoupled',data=PC_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pDCN=popul.create_dataset('DCN_coupled',data=DCN_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pDCNu=popul.create_dataset('DCN_uncoupled',data=DCN_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pIO= popul.create_dataset('IO_coupled',data=IO_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pIOu=popul.create_dataset('IO_uncoupled',data=IO_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz)

# Plasticity Variables
wPC = Params.create_dataset('weight_PC_coupled',data=mon_N_PC_Coupled.weight_PC)
wPCu = Params.create_dataset('weight_PC_uncoupled',data=mon_N_PC_Uncoupled.weight_PC)
deltawPC=Params.create_dataset('delta_weight_coupled',data=mon_N_PC_Coupled.delta_weight)
deltawPCu= Params.create_dataset('delta_weight_uncoupled',data=mon_N_PC_Uncoupled.delta_weight)
newPC = Params.create_dataset('new_weight_coupled', data=mon_N_PC_Coupled.new_weight)
newPCu = Params.create_dataset('new_weight_uncoupled',data=mon_N_PC_Uncoupled.new_weight)
PC_long = Params.create_dataset('Long_term_f_coupled', data= mon_N_PC_Coupled.f_lt_PC_coupled)
PC_longu=Params.create_dataset('Long_term_f_uncoupled', data= mon_N_PC_Uncoupled.f_lt_PC_uncoupled)
PC_short = Params.create_dataset('Short_term_f_coupled',data=mon_N_PC_Coupled.f_st_PC_coupled)
PC_shortu = Params.create_dataset('Short_term_f_uncoupled',data=mon_N_PC_Uncoupled.f_st_PC_uncoupled)
tau = Params.create_dataset('tau_coupled',data=mon_N_PC_Coupled.tau)
tau_u = Params.create_dataset('tau_uncoupled',data=mon_N_PC_Uncoupled.tau)

# Fill the assigned data with the according ones
for ii in range(0,N_Cells_IO):
    vIO[ii] = IO_Statemon_Coupled_STDP.Vs[ii]
    vIOu[ii] = IO_Statemon_Uncoupled_STDP.Vs[ii]
    
    S_IO[ii] = list(IO_Spikemon_Coupled_STDP.spike_trains().values())[ii]
    S_IOu[ii] = list(IO_Spikemon_Uncoupled_STDP.spike_trains().values())[ii]
    
   
for jj in range(0,N_Cells_DCN):
    vDCN[jj]=DCN_Statemon_Coupled_STDP.v[jj]
    vDCNu[jj]=DCN_Statemon_Uncoupled_STDP.v[jj]

    S_DCN[jj] = list(DCN_Spikemon_Coupled_STDP.spike_trains().values())[jj]
    S_DCNu[jj]= list(DCN_Spikemon_Uncoupled_STDP.spike_trains().values())[jj]

for kk in range(0,N_Cells_PC):
    vPC[kk] = PC_Statemon_Coupled_STDP.v[kk]
    vPCu[kk] = PC_Statemon_Uncoupled_STDP.v[kk]
    
    I_PC[kk] = PC_Statemon_Coupled_STDP.I_Noise[kk]
    I_PCu[kk] = PC_Statemon_Uncoupled_STDP.I_Noise[kk]
    S_PC[kk] = list(PC_Spikemon_Coupled_STDP.spike_trains().values())[kk]
    S_PCu[kk] = list(PC_Spikemon_Uncoupled_STDP.spike_trains().values())[kk]
    
for pp in range(n_Noise):
    I[pp] = Noise_extended_statemon.I[pp]
    
for qq in range(n_Noise*N_Cells_PC):
    wPC[qq] = mon_N_PC_Coupled.weight_PC[qq]
    wPCu[qq] =mon_N_PC_Uncoupled.weight_PC[qq]
    deltawPC[qq] = mon_N_PC_Coupled.delta_weight[qq]
    deltawPCu[qq] = mon_N_PC_Uncoupled.delta_weight[qq]
    newPC[qq] = mon_N_PC_Coupled.new_weight[qq]
    newPCu[qq] = mon_N_PC_Uncoupled.new_weight[qq]
    PC_long[qq] = mon_N_PC_Coupled.f_lt_PC_coupled[qq]
    PC_longu[qq] = mon_N_PC_Uncoupled.f_lt_PC_uncoupled[qq]
    PC_short[qq]=mon_N_PC_Coupled.f_st_PC_coupled[qq]
    PC_shortu[qq]=mon_N_PC_Uncoupled.f_st_PC_uncoupled[qq]
    tau[qq]=mon_N_PC_Coupled.tau[qq]
    tau_u[qq]= mon_N_PC_Uncoupled.tau[qq]

pIO = IO_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pIOu = IO_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pPC = PC_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pPCu = PC_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pDCN = DCN_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pDCNu = DCN_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz

FinalWeights = [mon_N_PC_Coupled.new_weight[k][-1] for k in range(0,n_Noise*n_PC)]
FinalWeightsu = [mon_N_PC_Uncoupled.new_weight[k][-1] for k in range(0,n_Noise*n_PC)]

fw = Params.create_dataset('final_weights_coupled', data=FinalWeights)
fwu = Params.create_dataset('final_weights_uncoupled', data=FinalWeightsu)
fw = FinalWeights
fwu=FinalWeightsu


### Noise input

#Input={'I':Noise_extended_statemon.I, 'nweight':mon_N_PC_Coupled.new_weight, 'I_InputPC':PC_Statemon_Coupled_STDP.I_Noise}
#with open(nois, 'wb') as inp:
#    pickle.dump(Input, inp, pickle.HIGHEST_PROTOCOL)
#    print('Inputs are saved')

### Voltage of Cell
#VoltCell = {'IOsoma_coupled':IO_Statemon_Coupled_STDP.Vs, 'IOdend':IO_Statemon_Coupled_STDP.Vd, 
#            'IOsoma_uncoupled':IO_Statemon_Uncoupled_STDP.Vs,'PC_coupled':PC_Statemon_Coupled_STDP.v, 'DCN_coupled':DCN_Statemon_Coupled_STDP.v,'PC_uncoupled':PC_Statemon_Uncoupled_STDP.v, 'DCN_uncoupled':DCN_Statemon_Uncoupled_STDP.v}
#with open(volt, 'wb') as vc:
#    pickle.dump(VoltCell, vc, pickle.HIGHEST_PROTOCOL)
#    print('Voltage Cells are saved')

### Spike times

#SpikeTimes = {'PC_coupled':list(PC_Spikemon_Coupled_STDP.spike_trains().values()),
#              'DCN_coupled':list(DCN_Spikemon_Coupled_STDP.spike_trains().values()),
#              'PC_uncoupled':list(PC_Spikemon_Uncoupled_STDP.spike_trains().values()),
#              'DCN_uncoupled':list(DCN_Spikemon_Uncoupled_STDP.spike_trains().values()),
#              'IO_coupled':list(IO_Spikemon_Coupled_STDP.spike_trains().values()),
#             'IO_uncoupled':list(IO_Spikemon_Uncoupled_STDP.spike_trains().values())}
#with open(spikes, 'wb') as st:
#    pickle.dump(SpikeTimes, st, pickle.HIGHEST_PROTOCOL)
#    print('Spike Times are saved')
#Population = {'PC_uncoupled':PC_rate_Uncoupled_STDP.smooth_rate(window='gaussian', width=1*ms)/Hz, 'DCN_uncoupled':DCN_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz, 'IO_uncoupled':IO_rate_Uncoupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'PC_coupled':PC_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz, 'DCN_coupled': DCN_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'IO_coupled':IO_rate_Coupled_STDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'t':PC_rate_Uncoupled_STDP.t/ms}

#with open(poprate, 'wb') as ka:
#    pickle.dump(Population, ka, pickle.HIGHEST_PROTOCOL)
#    print('population rates saved')
    
    
