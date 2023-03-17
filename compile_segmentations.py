# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 09:23:42 2022

@author: ingvieb
"""

import numpy as np
import cv2
import pandas as pd
import glob as glob
import os
import struct
from tqdm import tqdm
#import matplotlib.pyplot as plt



#EDIT VARIABLES BEFORE RUNNING SCRIPT:

genotype = 'D2R'
age = 'P17'
sex = 'M'
subject = 'E19'




#######################################################################################

subjectpath = 'Y:\Dopamine_receptors\Analysis\QUINT_analysis/' + '/' + genotype + '/' + age + '/' + '/' + genotype + '_' + age + '_' + sex + '_' + subject 
atlaspath = subjectpath + '/06_atlas_maps//'
segpath_gen = subjectpath + '/02_ilastik_output/Output_general/glasbey//'
segpath_fib = subjectpath + '/02_ilastik_output/Output_fibrous/glasbey//'
segpath_heavy = subjectpath + '/02_ilastik_output/Output_heavily/glasbey//'
damagemaskpath = subjectpath + '/04_damage_masks//'

outpath_gen = subjectpath + '/03_combined_segmentations/01_General_masked//'
outpath_fib = subjectpath + '/03_combined_segmentations/02_Fibrous_masked//'
outpath_heavy = subjectpath + '/03_combined_segmentations/03_Heavily_masked//'
outpath_combined = subjectpath + '/03_combined_segmentations/04_Masked_files_combined//'
outpath_recolored = subjectpath + '/03_combined_segmentations/05_Combined_segmentations_recolored//'
outpath_recolored_masked = subjectpath + '/05_masked_segmentations//'

# Definition of function to read .flat files obtained by use of QuickNII or VisuAlign. Written by Gergely Csucs. NB: Has only been tested with .flat files from Allen CCFv3 2017 and DeMBA v1-beta.

def read_flat_file(flat_file_path):
    with open(flat_file_path, 'rb') as flat:
        b,w,h=struct.unpack('>bii',flat.read(9))
        mx=0
        empty_file = np.zeros((h,w))
        for row in range(h):
            for col in range(w):
                i,=struct.unpack('>H',flat.read(2))
                empty_file[row, col] = i
        return empty_file, h, w
    

# Definition of the initial files to be used:

my_images = glob.glob(os.path.join(atlaspath, "*_nl.png")) #find all .png atlas maps. Requires .png files from VisuAlign with last part of name being _nl.png
my_files = glob.glob(os.path.join(atlaspath, "*_nl.flat")) #find all .flat atlas maps. Requires .flat files from VisuAlign with last part of name being _nl.flat
my_segmentations_gen = glob.glob(os.path.join(segpath_gen, "*.png")) #find all segmentation .png images from the first classifier (here called _gen for general)
my_segmentations_fib = glob.glob(os.path.join(segpath_fib, "*.png")) #find all segmentation .png images from the second classifier (here called _fib for fibrous)
my_segmentations_heavy = glob.glob(os.path.join(segpath_heavy, "*.png")) #find all segmentation .png images from the third classifier (here called _heavy for heavily)

file_numbers = []    
    
for file in my_files:
    #filepath = atlaspath + file
    filenumber = os.path.basename(file).split('_s')[1].split('_')[0]
    file_numbers.append(filenumber)

seg_numbers = []    
    
for segmentation in my_segmentations_gen:
    segnumber = os.path.basename(segmentation).split('_s')[1].split('_')[0]
    seg_numbers.append(segnumber)        

# Specify the file that gives the labels (region names) of the atlas used to generate the FLAT files. 
# NOTE: The flat file uses an ID for each region that is based on the order in which the regions appear in the .label file used in QuickNII / VisuAlign.

allen2nutdir = 'Y:/Dopamine_receptors/Analysis/resources//'


if age == 'P35' or age == 'P25' or age == 'P17':
    allen2nutfile = 'newmaster2nut.csv'
    
if age == 'P70' or age == 'P49':
    allen2nutfile = 'allen2nut.csv'
    

D1R_ids = pd.read_csv(allen2nutfile, sep=';', usecols =['nutil_id', 'D1R_classifier'])
D1R_general_IDs = D1R_ids.loc[D1R_ids['D1R_classifier'] == 'general']
D1R_fibrous_IDs = D1R_ids.loc[D1R_ids['D1R_classifier'] == 'fibrous']
D1R_heavily_IDs = D1R_ids.loc[D1R_ids['D1R_classifier'] == 'heavily']

D2R_ids = pd.read_csv(allen2nutfile, sep=';', usecols =['nutil_id', 'D2R_classifier'])
D2R_general_IDs = D2R_ids.loc[D2R_ids['D2R_classifier'] == 'general']
D2R_fibrous_IDs = D2R_ids.loc[D2R_ids['D2R_classifier'] == 'fibrous']
D2R_heavily_IDs = D2R_ids.loc[D2R_ids['D2R_classifier'] == 'heavily']


if genotype == 'D1R':
    included_regions_gen = D1R_general_IDs['nutil_id'].values
    included_regions_fib = D1R_fibrous_IDs['nutil_id'].values
    included_regions_heavy = D1R_heavily_IDs['nutil_id'].values

if genotype == 'D2R':
    included_regions_gen = D2R_general_IDs['nutil_id'].values
    included_regions_fib = D2R_fibrous_IDs['nutil_id'].values
    included_regions_heavy = D2R_heavily_IDs['nutil_id'].values


my_masks_gen = []

for file in my_files:
    file, height, width = read_flat_file(file)
    empty_file = np.zeros((height, width))
    ##mask all regions
    for region in included_regions_gen:
        mask = (file==region)
        empty_file[mask] = True 
    # plt.imshow(empty_file, cmap='gray')
    # plt.show()
    my_masks_gen.append(empty_file) 
    
my_masks_fib = []

for file in my_files:
    file, height, width = read_flat_file(file)
    empty_file = np.zeros((height, width))
    ##mask all regions
    for region in included_regions_fib:
        mask = (file==region)
        empty_file[mask] = True 
    # plt.imshow(empty_file, cmap='gray')
    # plt.show()
    my_masks_fib.append(empty_file)   
    
my_masks_heavy = []

for file in my_files:
    file, height, width = read_flat_file(file)
    empty_file = np.zeros((height, width))
    ##mask all regions
    for region in included_regions_heavy:
        mask = (file==region)
        empty_file[mask] = True 
    # plt.imshow(empty_file, cmap='gray')
    # plt.show()
    my_masks_heavy.append(empty_file)   



my_matched_segmentations_gen = []
    
for file, segmentation in zip(my_files, my_segmentations_gen):        
    if segnumber in file_numbers:    
        my_matched_segmentations_gen.append(segmentation)


my_matched_segmentations_fib = []
    
for file, segmentation in zip(my_files, my_segmentations_fib):        
    if segnumber in file_numbers:    
        my_matched_segmentations_fib.append(segmentation)


my_matched_segmentations_heavy = []
    
for file, segmentation in zip(my_files, my_segmentations_heavy):        
    if segnumber in file_numbers:    
        my_matched_segmentations_heavy.append(segmentation)


print("Combining segmentations...")

for seg_gen, seg_fib, seg_heavy, mask_gen, mask_fib, mask_heavy, segnum in tqdm(zip(my_matched_segmentations_gen, my_matched_segmentations_fib, my_matched_segmentations_heavy, my_masks_gen, my_masks_fib, my_masks_heavy, seg_numbers), total = len(seg_numbers)):
    print(f'{outpath_gen}{genotype}_{age}_{sex}_{subject}_SS_general_masked_s{segnum}.png', f'{outpath_fib}{genotype}_{age}_{sex}_{subject}_SS_fibrous_masked_s{segnum}.png', f'{outpath_heavy}{genotype}_{age}_{sex}_{subject}_SS_heavily_masked_s{segnum}.png')
    segimg_gen = cv2.imread(seg_gen)
    segimg_fib = cv2.imread(seg_fib)
    segimg_heavy = cv2.imread(seg_heavy)
    size = segimg_gen.shape
    maskimg_gen = mask_gen
    maskimg_fib = mask_fib
    maskimg_heavy = mask_heavy
    resized_maskimg_gen = cv2.resize(maskimg_gen, size[:2][::-1], interpolation = cv2.INTER_NEAREST)
    resized_maskimg_gen = np.expand_dims(resized_maskimg_gen,2)
    resized_maskimg_fib = cv2.resize(maskimg_fib, size[:2][::-1], interpolation = cv2.INTER_NEAREST)
    resized_maskimg_fib = np.expand_dims(resized_maskimg_fib,2)
    resized_maskimg_heavy = cv2.resize(maskimg_heavy, size[:2][::-1], interpolation = cv2.INTER_NEAREST)
    resized_maskimg_heavy = np.expand_dims(resized_maskimg_heavy,2)
    masked_segmentation_gen = resized_maskimg_gen * segimg_gen
    masked_segmentation_fib = resized_maskimg_fib * segimg_fib
    masked_segmentation_heavy = resized_maskimg_heavy * segimg_heavy
    cv2.imwrite(f'{outpath_gen}{genotype}_{age}_{sex}_{subject}_SS_general_masked_s{segnum}.png', masked_segmentation_gen)
    cv2.imwrite(f'{outpath_fib}{genotype}_{age}_{sex}_{subject}_SS_fibrous_masked_s{segnum}.png', masked_segmentation_fib)
    cv2.imwrite(f'{outpath_heavy}{genotype}_{age}_{sex}_{subject}_SS_heavily_masked_s{segnum}.png', masked_segmentation_heavy)
    my_combined_segmentation = cv2.imwrite(f'{outpath_combined}{genotype}_{age}_{sex}_{subject}_SS_combined_s{segnum}.png', masked_segmentation_gen + masked_segmentation_fib + masked_segmentation_heavy)    

    
    
my_combined_segmentations = glob.glob(os.path.join(outpath_combined, "*.png"))       
print("Recolouring segmentations...")

for segmentation, segnum in tqdm(zip(my_combined_segmentations, seg_numbers), total = len(seg_numbers)):

    combined_segmentation = cv2.imread(segmentation)
    recolored_combined_segmentation = combined_segmentation[np.all(combined_segmentation == (255, 0, 0), axis=-1)] = (255,0,255)
    recolored_combined_segmentation = combined_segmentation[np.all(combined_segmentation == (0, 255, 0), axis=-1)] = (255,0,255)
    recolored_combined_segmentation = combined_segmentation[np.all(combined_segmentation == (0, 0, 255), axis=-1)] = (255,0,255)  
    cv2.imwrite(f'{outpath_recolored}{genotype}_{age}_{sex}_{subject}_SS_combined_recolored_s{segnum}.png', combined_segmentation)
    
print("Applying Masks...")


for segnum in tqdm(seg_numbers):
    my_recolored_segmentations = glob.glob(os.path.join(outpath_recolored, f'*{segnum}*.png'))
    my_damage_masks = glob.glob(os.path.join(damagemaskpath, f'*{segnum}*.png'))
    if len(my_recolored_segmentations)==1 and len(my_damage_masks)==1:
        damage_mask = my_damage_masks[0]
        my_recolored_segmentation = my_recolored_segmentations[0]
        my_recolored_segmentation = np.array(cv2.imread(my_recolored_segmentation))
        size = my_recolored_segmentation.shape
        damage_mask = np.array(cv2.imread(damage_mask))
        damage_mask = cv2.resize(damage_mask, size[:2][::-1], interpolation = cv2.INTER_NEAREST)
        damage_mask = damage_mask / 255
        dst = my_recolored_segmentation * damage_mask
        dst = dst[:,:,::-1]
        cv2.imwrite(f'{outpath_recolored_masked}{genotype}_{age}_{sex}_{subject}_SS_s{segnum}.png', dst)
    else:
        my_recolored_segmentation = my_recolored_segmentations[0]
        my_recolored_segmentation = np.array(cv2.imread(my_recolored_segmentation))
        cv2.imwrite(f'{outpath_recolored_masked}{genotype}_{age}_{sex}_{subject}_SS_s{segnum}.png', my_recolored_segmentation)
        
print('-------------------------------------------')
print('All done! :D')


#to print masks as .png images, use the following:    
    
# my_mask_images = []

# for maskimg, filenum in zip(my_masks_gen, file_numbers):  
#     img_out = maskimg * 255 
#     cv2.imwrite(f'{outpath}_segmentation_masked{filenum}.png', img_out)
    



    
    