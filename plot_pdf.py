from starter1 import *
import yt
import astropy.io.fits as pyfits
import matplotlib.colors as colors
plt.close('all')

def dump_array_to_fits(array,filename):
    hdu = pyfits.PrimaryHDU(array)
    hdulist = pyfits.HDUList([hdu])
    hdulist.writeto(filename,overwrite=True)


plotdir="/home/dccollins/PigPen"
basedir="/data/cb1/Projects/P49_EE_BB"
simlist=nar(["half_half","half_1","half_2","1_half","1_1","1_2","2_half","2_1","2_2","3_half","3_1","3_2"])
frame_list=[range(11,31),range(11,31),range(11,31),range(11,31),range(11,31),range(11,31),range(65,85),range(11,31),range(11,31),range(72,91),range(56,75),range(20,40)]
frame_dict = dict( zip( simlist, frame_list) )

simulations = ['half_half','half_1','half_2','3_half','3_1','3_2']

frb_base = "/data/cb1/Projects/P64_onepoint/frb_temp"

#
# Make PDFs
# Save them in HDF5 files.
#

for sim in simulations:
    for frame in frame_dict[sim][0:1]:
        print(sim,frame)
        data_fname = "%s/%s/DD%04d/data%04d"%(basedir,sim,frame,frame)
        ds = yt.load(data_fname)
        if not os.path.exists(frb_dir):
            os.mkdir(frb_dir)

        pdf_name = "%s/pdf_%s_n%04d_%s_%s.h5"%(frb_dir, sim, frame, field,axis)

        if os.path.exists(pdf_name):
            print("Skipping ", pdf_name)
            continue

        ad = ds.region([0.5]*3,[0.4]*3,[0.6]*3)
        profile  = yt.create_profile(ad,['density'],'cell_volume',weight_field=None)
        fptr = h5py.File(pdf_name,'w')
        fptr.create_dataset("density_bins",data=profile.x_bins)
        fptr.create_dataset("cell_volume",data=profile['cell_volume'])
        fptr.close()

#
# Read and plot
#


fig, ax = plt.subplots(3,2,figsize=(8,12))
axlist = ax.flatten()
for nsim,sim in enumerate(simulations):
    for frame in frame_dict[sim][0:1]:


        pdf_name = "%s/pdf_%s_n%04d_%s_%s.h5"%(frb_dir, sim, frame, field,axis)

        fptr = h5py.File(pdf_name,'r')

        x_bins = fptr['density_bins'][()] #this syntax is odd but its what h5py wants
        cell_volume = fptr['cell_volume'][()]

        bin_cen = 0.5*(x_bins[1:]+x_bins[:-1])

        axlist[nsim].plot(bin_cen,cell_volume)
        axlist[nsim].set_xlabel(r'$\rho$')
        axlist[nsim].set_xscale('log')
        axlist[nsim].set_yscale('log')
for n in range(3):
    ax[n][1].yaxis.tick_right()
    ax[n][0].set_ylabel(r'$V(\rho)$')
fig.savefig("%s/pdf_%s_%s_%04d.png"%(plotdir,field,axis,frame))




