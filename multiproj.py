from starter1 import *
import yt
import astropy.io.fits as pyfits
import matplotlib.colors as colors
plt.close('all')



plotdir="/home/dccollins/PigPen"
basedir="/data/cb1/Projects/P49_EE_BB"
simlist=nar(["half_half","half_1","half_2","1_half","1_1","1_2","2_half","2_1","2_2","3_half","3_1","3_2"])
frame_list=[range(11,31),range(11,31),range(11,31),range(11,31),range(11,31),range(11,31),range(65,85),range(11,31),range(11,31),range(72,91),range(56,75),range(20,40)]
frame_dict = dict( zip( simlist, frame_list) )

simulations = ['half_half','half_1','half_2','3_half','3_1','3_2']

pdf_base = "/data/cb1/Projects/P64_onepoint/frb_temp"

#
# Make projections.  
# Save them in FITS files.
#

for field in ['density']:
    for axis in 'x':  
        density_array={}

        for sim in simulations:
            for frame in frame_dict[sim][0:1]:
                print(sim,frame)
                data_fname = "%s/%s/DD%04d/data%04d"%(basedir,sim,frame,frame)
                ds = yt.load(data_fname)
                frb_dir =  "%s/%s"%(frb_base, sim)
                if not os.path.exists(frb_dir):
                    os.mkdir(frb_dir)

                frb_name = "%s/frb_%s_n%04d_%s_%s.fits"%(frb_dir, sim, frame, field,axis)

                if os.path.exists(frb_name):
                    print("Skipping ", frb_name)
                    continue
                res = ds.parameters['TopGridDimensions'][0] 
                proj = ds.proj(field,axis)
                frb = proj.to_frb(1,res)
                dump_array_to_fits(frb[field], frb_name)



#
# Read and Project
#


fig, ax = plt.subplots(3,2,figsize=(4,6))
fig.subplots_adjust(wspace=0, hspace=0)
axlist = ax.flatten()
for nsim,sim in enumerate(simulations):
    for frame in frame_dict[sim][0:1]:

        data_fname = "%s/%s/DD%04d/data%04d"%(basedir,sim,frame,frame)
        frb_dir =  "%s/%s"%(frb_base, sim)
        frb_name = "%s/frb_%s_n%04d_%s_%s.fits"%(frb_dir, sim, frame, field,axis)
        
        data = pyfits.open(frb_name)[0].data

        plot=axlist[nsim].imshow( data, interpolation='nearest',origin='lower')
        #fig.colorbar(plot,ax=axlist[nsim])
        axlist[nsim].text( 10,10,r"$\mathcal{M}_s=4$",color=[1.0]*3)
        axlist[nsim].axis('off')

fig.savefig("%s/proj_%s_%s.png"%(plotdir,field,axis))




