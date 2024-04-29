# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:06:58 2024

@author: ingvieb
"""

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from scipy.ndimage import zoom

d1_path = r"C:\Users\ingvieb\dopamap\D1_volumes_averaged.nii"
d1_vol = nib.load(d1_path)
d1_vol_data = d1_vol.get_fdata()
d1_vol_data[d1_vol_data<0] = 0


d2_path = r"C:\Users\ingvieb\dopamap\D2_volumes_averaged.nii"
d2_vol = nib.load(d2_path)
d2_vol_data = d2_vol.get_fdata()
d2_vol_data[d2_vol_data<0] = 0


pc99 = np.percentile((d1_vol_data, d2_vol_data), 99.9)

d1_vol_data[d1_vol_data>pc99] = pc99

d1_range = np.nanmax(d1_vol_data) - np.nanmin(d1_vol_data)
d1_normalized = ((d1_vol_data - np.nanmin(d1_vol_data)) / d1_range)

d2_vol_data[d2_vol_data>pc99] = pc99

d2_range = np.nanmax(d2_vol_data) - np.nanmin(d2_vol_data)
d2_normalized = ((d2_vol_data - np.nanmin(d2_vol_data)) / d2_range)



max_val = np.nanmax((d1_normalized,d2_normalized))

ratio_vol = 1 - (((d1_normalized - d2_normalized)/max_val))



ratio_vol[~(ratio_vol % 7).astype(bool)] = np.nan

cmap = mpl.colormaps.get_cmap('bwr')
cmap.set_bad(color='grey')


plt.imshow((ratio_vol[:,300,:]),cmap=cmap)
plt.colorbar()
plt.show()


vol_for_header = nib.load(r"C:\Users\ingvieb\dopamap\annotation_boundary_10.nii.gz")

micron_size = 0.001 * 25 # i changed this to 10 from 25 for the zoom method below. 
header = vol_for_header.header 
header.set_xyzt_units(xyz=2, t=0)
header['pixdim'][1:4] = np.array([micron_size, micron_size, micron_size])
header['dim'] = d1_vol.header['dim']
header['srow_x'] = np.array([0.025,0,0, -5.695])
header['srow_y'] = np.array([0,0.025,0, 5.35])
header['srow_z'] = np.array([0,0,-0.025, -5.22])
vol_for_header.affine[:,:3] *= 2.5
vol_for_header.affine[:3,:3] = np.array([[0.025,0,0],
                                                       [0.0,0.025,0],
                                                       [0.0,0,0.025]])
print(header)
out_img = nib.Nifti1Image(ratio_vol, vol_for_header.affine, header)
nib.save(out_img, r"C:\Users\ingvieb\dopamap\ratio_vol.nii.gz")



print(d1_vol.header)

















