# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 16:06:58 2024

@author: ingvieb
"""

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib as mpl
from skimage import feature
from tqdm import tqdm

d1_path = r"C:\Users\ingvieb\dopamap\D1_volumes_averaged.nii"
d1_vol = nib.load(d1_path)
d1_vol_data = d1_vol.get_fdata()
d1_vol_data[d1_vol_data<0] = 0


d2_path = r"C:\Users\ingvieb\dopamap\D2_volumes_averaged.nii"
d2_vol = nib.load(d2_path)
d2_vol_data = d2_vol.get_fdata()
d2_vol_data[d2_vol_data<0] = 0


pc99 = np.percentile((d1_vol_data, d2_vol_data), 99)

d1_vol_data[d1_vol_data>pc99] = pc99

d1_range = np.nanmax(d1_vol_data) - np.nanmin(d1_vol_data)
d1_normalized = ((d1_vol_data - np.nanmin(d1_vol_data)) / d1_range)

d2_vol_data[d2_vol_data>pc99] = pc99

d2_range = np.nanmax(d2_vol_data) - np.nanmin(d2_vol_data)
d2_normalized = ((d2_vol_data - np.nanmin(d2_vol_data)) / d2_range)



max_val = np.nanmax((d1_normalized,d2_normalized))

#ratio_vol = 1 - (((d1_normalized - d2_normalized)/max_val))


ratio_vol = (d1_vol_data - d2_vol_data) / (d1_vol_data + d2_vol_data)
#ratio_vol = (d1_normalized - d2_normalized) / (d1_normalized + d2_normalized)

ratio_vol[~(ratio_vol % 7).astype(bool)] = np.nan

cmap = mpl.colormaps.get_cmap('bwr')
cmap.set_bad(color='grey')


plt.imshow((ratio_vol[:,300,:]),cmap=cmap)
plt.colorbar()
plt.show()


out_img = nib.Nifti1Image(ratio_vol, d1_vol.affine)
nib.save(out_img, r"C:\Users\ingvieb\dopamap\ratio_vol.nii.gz")















