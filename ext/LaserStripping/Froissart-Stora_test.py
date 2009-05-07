#-----------------------------------------------------
#Track bunch with r and p through the external field 
# The field is 1 T and has direction (0,1,0)
#-----------------------------------------------------

import sys,math,os

from bunch import *
from trackerrk4 import *
from laserstripping import *
from ext.las_str.plot_mod import *






method = 1

#----------------------Beginning of the tracker and laser parameters----------------------#
orbit_path = os.environ["ORBIT_ROOT"]
addr = orbit_path+"/ext/laserstripping/working_dir/"
trans = orbit_path+"/ext/laserstripping/transitions/"

n_step = 10000
par=10

Ex=4.0e1
n_states = 3


data_name = "data_ampl_"
pic_name = "imageFS.png"

ta = 2.418884326505e-17                             # atomic unit of time
Rabi = 1e+12*ta                                      # Rabi frequency
Gamma = -math.pi*Rabi*Rabi/2/math.log(1-0.87)         # frequency sweep 
Omega = 4./9.
#Omega = 3./8.                                         # basis frequency
dip_trans = math.sqrt(729./8192.)                     # dipole transition between two levels
#dip_trans = math.sqrt(32768./59049.)                     # dipole transition between two levels
Elas=Rabi/dip_trans                                     # Amplitude of laser field

#----------------------End of the tracker and laser parameters----------------------#



levels = n_states*(1+n_states)*(1+2*n_states)/6


LFS = FroissartStoraLF(Omega,Gamma,Elas) 
LFS.setLaserFieldPolarization(1.,1.,1.)
fS = ConstEMfield(Ex,0.,0.,0.,0.,0.)

if(method == 2 or method == 3):     Stark = HydrogenStarkParam(trans, n_states)

if (method == 1):   am, pop, eff = 2*2+1,             2+1,      TwoLevelAtom(LFS,4./9.,math.sqrt(729./8192.))
if (method == 2):   am, pop, eff = 2*levels+1,        levels+1, SchrodingerEquation(LFS,Stark,1000.) 
if (method == 3):   am, pop, eff = 2*levels*levels+1, levels+1, DensityMatrix(LFS,Stark,1000.)  

b = Bunch()
b.charge(0)
b.mass(0.938256 + 0.000511)
b.addParticle(0.,0.,0.,0.,0.,0.)

b.addPartAttr("Populations",{"size":pop})
b.addPartAttr("Amplitudes",{"size":am})
b.partAttrValue("Amplitudes",0,1,1.0)


pr = PrintExtEffects(max(2*n_step*par/10000,1),addr+data_name)

cont_eff = ExtEffectsContainer()
cont_eff.AddEffect(eff)
cont_eff.AddEffect(pr)


tracker = RungeKuttaTracker(0.000000001)

time_step=(2*math.pi*ta/Rabi)/n_step
print "Start tracking."
tracker.track(b,-par*time_step*n_step,2*par*time_step*n_step, time_step,fS,cont_eff)
print "Stop tracking.","t= ",par*time_step*n_step

pop1 = b.partAttrValue("Populations",0,1)
sum = b.partAttrValue("Populations",0,0)

pop2 = sum - pop1

if (method == 1):                  ratio = [3,1]
if (method == 2 or method == 3):   ratio = [5,3]

graph = PlotPopl(ratio,["%1.4f"%pop2],0.15,addr+data_name+"0.dat",addr+pic_name)
os.system('eog '+addr+pic_name)
os.remove(addr+data_name+"0.dat")
print "AttrValue=","sum=", pop2, sum


