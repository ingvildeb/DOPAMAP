# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:37:07 2022

@author: ingvieb
"""

import cupy as np
import nibabel as nib
from datetime import datetime
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
import numpy as numpy



volume_path = r"Y:\Dopamine_receptors\Analysis\resources\atlas_volumes\P14_label_rev-resampled.nii"

volume_open = nib.load(volume_path)

volume = np.array(volume_open.get_fdata())
columns = ["ox", "oy", "oz", "ux", "uy", "uz", "vx", "vy", "vz"]
numpy.set_printoptions(suppress=True)

def generate_target_slice(alignment, volume, center_alignment = False):
    Ox,Oy,Oz,Ux,Uy,Uz,Vx,Vy,Vz = alignment
    ##just for mouse for now
    bounds = np.array(volume.shape) -1
    
    X_size = np.linalg.norm(np.array((Ux,Uy,Uz))) * 10
    Z_size = np.linalg.norm(np.array((Vx,Vy,Vz))) * 10

    U_vector = np.array((Ux, Uy, Uz)) / X_size
    V_vector = np.array((Vx, Vy, Vz)) / Z_size
    
    X_size =  np.round_(X_size).astype(int)
    Z_size =  np.round_(Z_size).astype(int)

    #arange from 0 to 456 matching CCF U dimension (mediolateral)
    U_increment = np.arange(Ox, Ox+Ux, -1)
    #arange from 0 to 320 matching CCF V dimension (dorsoventral)
    V_increment = np.arange(Oz, Oz+Vz, -1)
    #make this into a grid (0,0) to (320,456)
    Uarange = np.arange(0,1,1/X_size.get())
    Varange = np.arange(0,1,1/Z_size.get())
    Ugrid, Vgrid = np.meshgrid(Uarange, Varange)
    Ugrid_x = Ugrid * Ux
    Ugrid_y = Ugrid * Uy
    Ugrid_z = Ugrid * Uz
    Vgrid_x = Vgrid * Vx
    Vgrid_y = Vgrid * Vy
    Vgrid_z = Vgrid * Vz

    X_Coords = (Ugrid_x + Vgrid_x).flatten() + Ox 
    Y_Coords = (Ugrid_y + Vgrid_y).flatten() + Oy
    Z_Coords = (Ugrid_z + Vgrid_z).flatten() + Oz

    X_Coords = np.round_(X_Coords).astype(int)
    Y_Coords = np.round_(Y_Coords).astype(int)
    Z_Coords = np.round_(Z_Coords).astype(int)


    out_bounds_Coords = (X_Coords>bounds[0]) | (Y_Coords>bounds[1]) | (Z_Coords>bounds[2]) | (X_Coords<0) | (Y_Coords<0) | (Z_Coords<0)
    X_pad = X_Coords.copy()
    Y_pad = Y_Coords.copy()
    Z_pad = Z_Coords.copy()

    X_pad[out_bounds_Coords] = 0
    Y_pad[out_bounds_Coords] = 0
    Z_pad[out_bounds_Coords] = 0
    # print('ob!: ')
    # print(np.sum(X_pad[out_bounds_Coords]))

    regions = volume[X_pad, Y_pad, Z_pad]
    # plt.plot(regions)
    # plt.show()
    # plt.plot(regions[out_bounds_Coords])
    # plt.show()
    ##this is a quick hack to solve rounding errors
    Z_size = abs(np.asnumpy(Z_size))
    X_size = abs(np.asnumpy(X_size)) 
    C = len(regions)
    compare = (C - X_size*Z_size)
    if abs(compare) == X_size:
        if compare>0:
            Z_size+=1
        if compare<0:
            Z_size-=1
    elif abs(compare) == Z_size:
        if compare>0:
            X_size+=1
        if compare<0:
            X_size-=1
    elif abs(compare) == Z_size + X_size + 1:
        
        if compare>0:
            X_size+=1
            Z_size+=1
        if compare<0:
            X_size-=1
            Z_size-=1
    
    regions = np.asnumpy(regions).reshape((Z_size,X_size))

    return regions

def find_plane_equation(plane):
    """
    Finds the plane equation of a plane
    :param plane: the plane to find the equation of
    :type plane: :any:`numpy.ndarray`
    :returns: the normal vector of the plane and the constant k
    :rtype: :any:`numpy.ndarray`, float
    """
    a, b, c = (
        np.array(plane[0:3], dtype=np.float64),
        np.array(plane[3:6], dtype=np.float64),
        np.array(plane[6:9], dtype=np.float64),
    )
    cross = np.cross(b, c)
    cross /= 9
    k = -((a[0] * cross[0]) + (a[1] * cross[1]) + (a[2] * cross[2]))
    return (cross, k)

def calculate_Z(Yarr,Xarr, alignment):
    ABC_plane, D = find_plane_equation(alignment)
    A, B, C = ABC_plane
    Z_grid = -((Xarr* A) + (Yarr* C) + D ) / B
    return Z_grid



def view_atlas_image(image, flip=True):
    if flip:
        image = image[::-1, ::-1]
    regions = np.unique(image)
    regions_replace = np.arange(len(regions))
    viewable_slice = np.zeros(image.shape)
    for region, region_rep in zip(regions, regions_replace):
        mask = image == region
        viewable_slice[mask] = region_rep
    plt.imshow(viewable_slice)
    plt.show()

    
def return_cropped_region_ids(alignment, atlas_shape_YXZ):
    """

    Parameters
    ----------
    alignment : array
        a single quickNii vector consisting of OxyzUxyzVxyz.
    atlas_shape_YX : tuple
        the size of the target atlas.

    Returns
    -------
    overlapping : list
        region ids which are in both the section and cropped areas (so are partially cropped).
    cropped : TYPE
        region ids which are only in the cropped areas (so are fully cropped).

    """
    start = datetime.now()
    
    atlas_y,atlas_x, atlas_z = atlas_shape_YXZ
    top_right_side_atlas_z = calculate_Z(0,atlas_x, alignment)
    top_left_side_atlas_z  = calculate_Z(0,0, alignment)
    bottom_left_side_atlas_z = calculate_Z(atlas_y, 0, alignment)
    
    top_left_side_atlas_point = np.array((0,top_left_side_atlas_z.get(),0))    
    top_right_side_atlas_point = np.array((atlas_x, top_right_side_atlas_z.get(), 0))
    bottom_left_side_atlas_point = np.array((0, bottom_left_side_atlas_z.get(), atlas_y))
    
    
    
    Xdist = np.linalg.norm(top_left_side_atlas_point-top_right_side_atlas_point) * 10
    Ydist = np.linalg.norm(top_left_side_atlas_point-bottom_left_side_atlas_point) * 10
    
    checkpoint1 =  datetime.now() - start
    # print('checkpoint 1: ', checkpoint1)
    # print('Xdist: ', Xdist)
    # print('Ydist: ', Ydist)
    XdistO = atlas_shape_YXZ[1]
    YdistO = atlas_shape_YXZ[0]

    #create a consectuive series of integers from 0 to the atlas_Y_size-1
    Y_indexes = np.arange(0,YdistO, YdistO/Ydist.get())
    #do the same for X
    X_indexes = np.arange(0,XdistO, XdistO/Xdist.get())
    #interlace them both into a grid
    X_grid, Y_grid = np.meshgrid(X_indexes, Y_indexes)

    checkpoint2 = datetime.now() - start 
    # print('checkpoint 2: ', checkpoint2)
    #call a function which calculates the Z position for a given XY along the plane of 'alignment'
    Z_grid = calculate_Z(Y_grid, X_grid, alignment)
    #round Z grid to the nearest whole number and convert to an int
    X_grid = np.round_(X_grid).astype(int)
    Y_grid = np.round_(Y_grid).astype(int)
    Z_grid = np.round_(Z_grid).astype(int)
    
    out_bounds_Coords = (X_grid>atlas_x-1) | (Z_grid>atlas_z-1) | (Y_grid>atlas_y-1)
    X_pad = X_grid.copy()
    Y_pad = Y_grid.copy()
    Z_pad = Z_grid.copy()

    X_pad[out_bounds_Coords] = 0
    Y_pad[out_bounds_Coords] = 0
    Z_pad[out_bounds_Coords] = 0
    #The rounding is necessary as we use the integers to index into the volume and get the corresponding region IDS (indexing requires integers)
    #here we get the whole image without any cropping
    image = volume[X_pad,Z_pad,Y_pad]
   #view_atlas_image(image)
    checkpoint3 = datetime.now() - start
    # print('checkpoint 3: ', checkpoint3)
    #generate the section as it appears in QuickNII, crops and all
    og_im = generate_target_slice(alignment, volume)
    checkpoint4 =  datetime.now() - start
    # print('checkpoint 4: ', checkpoint4)
    #get all the unique regions in the original image, and how many pixels are included in each
    og_unique, og_pix = np.unique(og_im, return_counts=True)
   #view_atlas_image(og_im)
    whole_unique, whole_pix = np.unique(image, return_counts=True)
    is_in = np.isin(whole_unique, og_unique)
    inv_is_in = np.isin(og_unique, whole_unique)
    not_in = ~is_in
    overlapping = whole_unique[is_in]
    cropped = whole_unique[not_in]
    checkpoint5 = datetime.now() - start
    # print('checkpoint 5: ', checkpoint5)
    
    overlapping_whole_pix = whole_pix[is_in] 
    non_overlapping_pix = whole_pix[not_in]
    whole_pix = np.concatenate((overlapping_whole_pix, non_overlapping_pix))
    overlapping_percent =   og_pix[inv_is_in] / overlapping_whole_pix
    return overlapping, cropped , whole_pix , og_pix[inv_is_in], overlapping_percent

from pandas import ExcelWriter

def save_xls(dict_df, path):
    """
    Save a dictionary of dataframes to an excel file, 
    with each dataframe as a separate page
    """

    writer = ExcelWriter(path)
    for key in dict_df.keys():
        dict_df[key].to_excel(writer, sheet_name=key)

    writer.save()
    
##set this to the Y and X values of the atlas you're using :)
atlas_shape_YX = numpy.array(volume.shape)[[2,0,1]] - 1

P49path = r'Y:\Dopamine_receptors\Analysis\QUINT_analysis\D*R\P17\*\00_nonlin_registration_files/*.json'
#P70path = r'Y:\Dopamine_receptors\Analysis\QUINT_analysis\D*R\P25\*\00_nonlin_registration_files/*.json'
P49jsons = glob(P49path)
#P70jsons = glob(P70path)
jsons = [*P49jsons]



for js in jsons:
    temp_df = pd.DataFrame({'Region ID', 'whole section pixels', 'cropped section pixels', 'percent present', 'percent absent'})
    df, atlas_target = read_QUINT_JSON(js)
    percent = []
    absent = []
    region_id = []
    dict_of_dicts = {}
    for index, alignment in df[columns].iterrows():
        filename = (df.iloc[index]['Filenames'])
        filename = '_'.join(filename.split('_')[3:])
        print(filename)
        overlapping, cropped,  whole_pix, og_pix, overlap_pc = return_cropped_region_ids(alignment, atlas_shape_YX)
        overlapping = np.asnumpy(overlapping)
        cropped = np.asnumpy(cropped)
        og_pix = np.asnumpy(og_pix)
        whole_pix = np.asnumpy(whole_pix)

        cropped_pixels = numpy.zeros(len(cropped))
        
        cropped_pixels[:] = numpy.nan

        ##this is just adding zeores sorry for the variable name
        og_pix = numpy.array([*og_pix, *cropped_pixels])
        

        temp_percent = og_pix / whole_pix
        temp_percent = numpy.nan_to_num(temp_percent)
        if (temp_percent[1:] > 1.2).any():
            print('check this file as it has a value over 120%')
        temp_absent = 1 - temp_percent
        temp_region_id = [*overlapping, *cropped]
        temp_dict = {'Region ID': temp_region_id, 'percent present':temp_percent, 'percent absent':temp_absent, 'pix whole section': whole_pix/10, 'pix cropped section': og_pix/10}
        dict_of_dicts[filename] = pd.DataFrame(temp_dict)
   



    fn = js.split('.')[0] + '_summary_statistics.xlsx'
    print(f'saving as {fn}...')
    save_xls(dict_of_dicts, fn)
    
        
    
