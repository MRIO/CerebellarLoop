from E_Synapses_NoPlasticity import *

# load the structure/ data file
dat = h5py.File(NameFile,'r+')
# Create frequency group
name = str(int(frequencyInput1))+'and'+str(int(frequencyInput2))+'Hz'
if globname.find('initial') != -1:
    freq_group = dat.create_group(name)
    print(freq_group.name)
    # Create subgroup of type of run
    sim_group = freq_group.create_group(typeOfRun)
    print(sim_group.name)
elif globname.find('adapt') != -1:
    freq_group = dat[name]
    sim_group = freq_group.create_group(typeOfRun)
else:
    raise Error('wrong name')

# type definition for variable shaped data
dt_type = h5py.vlen_dtype(np.dtype('float64'))

# Create subgroups for the different data stored
volt_cell = sim_group.create_group('Voltage_Cells')
print(volt_cell.name)
spikes = sim_group.create_group('Spikes')
popul = sim_group.create_group('Population_rate')
inputs = sim_group.create_group('Input')

# Create dataset for the cells
vIO=volt_cell.create_dataset('IOsoma_coupled',data=IO_Statemon_Coupled_noSTDP.Vs)
vIOu=volt_cell.create_dataset('IOsoma_uncoupled',data=IO_Statemon_Uncoupled_noSTDP.Vs)
vDCN = volt_cell.create_dataset('DCN_coupled', data=DCN_Statemon_Coupled_noSTDP.v)
vDCNu = volt_cell.create_dataset('DCN_uncoupled', data=DCN_Statemon_Uncoupled_noSTDP.v)
vPC = volt_cell.create_dataset('PC_coupled',data=PC_Statemon_Coupled_noSTDP.v)
vPCu = volt_cell.create_dataset('PC_uncoupled',data=PC_Statemon_Uncoupled_noSTDP.v)

# input parameters
I = inputs.create_dataset('I',data=Noise_extended_statemon.I)
weight = inputs.create_dataset('weight',data=S_statemon.noise_weight)
I_PC = inputs.create_dataset('I_InputPC_coupled', data=PC_Statemon_Coupled_noSTDP.I_Noise)
I_PCu = inputs.create_dataset('I_InputPC_uncoupled', data=PC_Statemon_Uncoupled_noSTDP.I_Noise)

# Spike Times
S_PC = spikes.create_dataset('PC_coupled',data=list(PC_Spikemon_Coupled_noSTDP.spike_trains().values()),dtype=dt_type)
S_PCu = spikes.create_dataset('PC_uncoupled',data=list(PC_Spikemon_Uncoupled_noSTDP.spike_trains().values()),dtype=dt_type)
S_IO = spikes.create_dataset('IO_coupled',data=list(IO_Spikemon_Coupled_noSTDP.spike_trains().values()),dtype=dt_type)
S_IOu = spikes.create_dataset('IO_uncoupled',data=list(IO_Spikemon_Uncoupled_noSTDP.spike_trains().values()),dtype=dt_type) 
S_DCN = spikes.create_dataset('DCN_coupled',data=list(DCN_Spikemon_Coupled_noSTDP.spike_trains().values()),dtype=dt_type)
S_DCNu = spikes.create_dataset('DCN_uncoupled',data=list(DCN_Spikemon_Uncoupled_noSTDP.spike_trains().values()),dtype=dt_type)

# Population Rates
pPC = popul.create_dataset('PC_coupled',data=PC_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pPCu = popul.create_dataset('PC_uncoupled',data=PC_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pDCN=popul.create_dataset('DCN_coupled',data=DCN_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pDCNu=popul.create_dataset('DCN_uncoupled',data=DCN_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pIO= popul.create_dataset('IO_coupled',data=IO_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)
pIOu=popul.create_dataset('IO_uncoupled',data=IO_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz)

# Fill the assigned data with the according ones
for ii in range(0,N_Cells_IO):
    vIO[ii] = IO_Statemon_Coupled_noSTDP.Vs[ii]
    vIOu[ii] = IO_Statemon_Uncoupled_noSTDP.Vs[ii]
    
    S_IO[ii] = list(IO_Spikemon_Coupled_noSTDP.spike_trains().values())[ii]
    S_IOu[ii] = list(IO_Spikemon_Uncoupled_noSTDP.spike_trains().values())[ii]
    
for jj in range(0,N_Cells_DCN):
    vDCN[jj]=DCN_Statemon_Coupled_noSTDP.v[jj]
    vDCNu[jj]=DCN_Statemon_Uncoupled_noSTDP.v[jj]
    
    S_DCN[jj] = list(DCN_Spikemon_Coupled_noSTDP.spike_trains().values())[jj]
    S_DCNu[jj]= list(DCN_Spikemon_Uncoupled_noSTDP.spike_trains().values())[jj]

for kk in range(0,N_Cells_PC):
    vPC[kk] = PC_Statemon_Coupled_noSTDP.v[kk]
    vPCu[kk] = PC_Statemon_Uncoupled_noSTDP.v[kk]
    
    I_PC[kk] = PC_Statemon_Coupled_noSTDP.I_Noise[kk]
    I_PCu[kk] =PC_Statemon_Uncoupled_noSTDP.I_Noise[kk]
    S_PC[kk] = list(PC_Spikemon_Coupled_noSTDP.spike_trains().values())[kk]
    S_PCu[kk] = list(PC_Spikemon_Uncoupled_noSTDP.spike_trains().values())[kk]
for pp in range(n_Noise):
    I[pp] = Noise_extended_statemon.I[pp]
    
for qq in range(n_Noise*N_Cells_PC):
    weight[qq] = S_statemon.noise_weight[qq]
   

 
pIO = IO_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pIOu = IO_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pPC = PC_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pPCu = PC_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pDCN = DCN_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz
pDCNu = DCN_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz

#Population_NoPlasticity = {'PC_uncoupled':PC_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian', width=1*ms)/Hz, 'DCN_uncoupled':DCN_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz, #'IO_uncoupled':IO_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'PC_coupled':PC_rate_Coupled_#noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz, 'DCN_coupled': #DCN_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'IO_coupled':IO_rate_Coupled_noSTDP.smooth_rate(window='gaussian',width=1*ms)/Hz,'t':PC_rate_Uncoupled_noSTDP.t/ms}

#with open(rates, 'wb') as ka:
#    pickle.dump(Population_NoPlasticity, ka, pickle.HIGHEST_PROTOCOL)
#    print('Population rates saved')

#sim_group.create_dataset('PC_uncoupled',data=PC_rate_Uncoupled_noSTDP.smooth_rate(window='gaussian', width=1*ms)/Hz)
