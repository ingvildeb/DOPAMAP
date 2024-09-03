# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 18:34:27 2024

@author: ingvieb
"""



import pandas as pd
import nibabel as nib
import numpy as np
from tqdm import tqdm
from skimage import feature

def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

customregs = pd.read_csv(r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\customregions.csv", sep=";")
id_to_custom = pd.read_excel(r"Y:\Dopamine_receptors\Analysis\resources\ID_to_custom.xlsx")

list_of_ids = id_to_custom["region ID"].tolist()
list_of_regs = id_to_custom["custom region"].tolist()


dict_minor_to_custom = {}

for key in list_of_ids:
    for value in list_of_regs:
        dict_minor_to_custom[key] = value
        list_of_regs.remove(value)
        break


customregnames = customregs["Region name"].tolist()
majorregs = customregs["Hierarchy"].tolist()

unique_mregs = unique_list(majorregs)
mreg_ids = list(range(1, len(unique_mregs)+1))

major_ids_dict = {}

for key in unique_mregs:
    for value in mreg_ids:
        major_ids_dict[key] = value
        mreg_ids.remove(value)
        break

mapping = (pd.Series(majorregs)).map(major_ids_dict) #convert the list to a pandas series temporarily before mapping
majorregs_id_list = list(mapping) # we transform the mapped values (a series object) back to a list


dict_custom_to_major = {}

for key in customregnames:
    for value in majorregs_id_list:
        dict_custom_to_major[key] = value
        majorregs_id_list.remove(value)
        break

#for id in list of ids, what is the custom region. then get the major region from the dictionary via the customregion

dict_minor_to_major = {}

for key in dict_minor_to_custom:
    creg = dict_minor_to_custom[key]
    major = dict_custom_to_major.get(creg)
    dict_minor_to_major[key] = major
    
    
atlas_path = r"C:\Users\ingvieb\dopamap\annotation_25.nii"
atlas_vol = nib.load(atlas_path)
atlas_vol_data = atlas_vol.get_fdata()

ids = np.unique(atlas_vol_data)

major_regions_volume = np.zeros(atlas_vol_data.shape).astype(int)



for i, mid in dict_minor_to_major.items():
    #print(i,mid)
    major_regions_volume[atlas_vol_data == i] = int(mid)
    
out_img = nib.Nifti1Image(major_regions_volume, atlas_vol.affine, atlas_vol.header)
out_img.set_data_dtype(np.uint32)
out_filename = r"C:\Users\ingvieb\dopamap/majorregs_annotation.nii.gz"
nib.save(out_img, out_filename)




with np.nditer(atlas_vol_data[:229,:,:], op_flags=['readwrite']) as it:

   for x in it:
       x[...] = 0

    
    
split_volume = atlas_vol_data + (major_regions_volume)
    
out_img = nib.Nifti1Image(split_volume, atlas_vol.affine, atlas_vol.header)
out_img.set_data_dtype(np.uint32)
out_filename = r"C:\Users\ingvieb\dopamap/split_annotations.nii.gz"
nib.save(out_img, out_filename)    
    
    

def create_outline(path, save_path):
    img = nib.load(path)
    # Get the data from the image
    data = img.get_fdata()
    # Assuming 'data' is your 3D numpy array
    edges = np.empty_like(data)
    pbar = tqdm(total=data.shape[0] + data.shape[1] + data.shape[2])
    for i in range(data.shape[0]):
        edges[i] = feature.canny(data[i])
        pbar.update(1)

    for i in range(data.shape[1]):
        edges[:, i] += feature.canny(data[:, i])
        pbar.update(1)

    for i in range(data.shape[2]):
        edges[:, :, i] += feature.canny(data[:, :, i])
        pbar.update(1)
    edges[edges > 0] = 1
    pbar.close()
    nib.save(nib.Nifti1Image(edges, img.affine, img.header), save_path)




split_vol = r"C:\Users\ingvieb\dopamap\split_annotations.nii.gz"
# atlas_vol = nib.load(atlas_path)
# atlas_vol_data = atlas_vol.get_fdata()

create_outline(split_vol, r"C:\Users\ingvieb\dopamap\split_annotation_outline.nii.gz")
    
    
    
    
    