# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 17:27:47 2022

@author: ingvieb
"""


import os
import pandas as pd
import glob
import re
import numpy as np
import xlwt
from xlwt.Workbook import *
from pandas import ExcelWriter
import xlsxwriter
from scipy.interpolate import interp1d
import math


os.chdir(r'Y:\Dopamine_receptors\Analysis\resources\\')
import nut_postprocessing_functions as nutpp


# ENTER PARAMETERS:

genotype = 'D1R'
age = 'P17'
sex = 'M'
subject = 'C137'


# SET UP DIRECTORIES AND FILES NEEDED:

## Define directories:

nutilpath = 'Y:/Dopamine_receptors/Analysis/QUINT_analysis/' + genotype + '/' + age + '/' + genotype + '_' + age + '_' + sex + '_' + subject + '/07_nutil//'
countspath = 'Y:/Dopamine_receptors/Analysis/QUINT_analysis/' + genotype + '/' + age + '/' + genotype + '_' + age + '_' + sex + '_' + subject + '/07_nutil/01_output_cells/Reports/CustomRegions//'
objectspath = 'Y:/Dopamine_receptors/Analysis/QUINT_analysis/' + genotype + '/' + age + '/' + genotype + '_' + age + '_' + sex + '_' + subject + '/07_nutil/01_output_cells/Reports/Objects//'
maskpath = 'Y:/Dopamine_receptors/Analysis/QUINT_analysis/' + genotype + '/' + age + '/' + genotype + '_' + age + '_' + sex + '_' + subject + '/07_nutil/02_output_masks/Reports/CustomRegions//'
registrationpath = 'Y:/Dopamine_receptors/Analysis/QUINT_analysis/' + genotype + '/' + age + '/' + genotype + '_' + age + '_' + sex + '_' + subject + '/00_nonlin_registration_files//'

all_files_list = glob.glob(os.path.join(countspath, "CustomRegions__s*.csv"))
all_mask_files = glob.glob(os.path.join(maskpath, "CustomRegions__s*.csv"))


## Get custom region names from excel file:

customregsfile = 'Y:/Dopamine_receptors/Analysis/resources//customregions.csv'


# PARAMETERS USED IN CALCULATIONS

my_section_thickness = 40
my_pixel_size = 1.21


## GENERATE DATAFRAMES

list_of_regionnames = nutpp.set_region_names(customregsfile)    
list_of_sections = nutpp.create_section_list(all_files_list)
complete_section_list = nutpp.create_full_section_list(list_of_sections)
list_of_missing_sections = nutpp.identify_missing_sections(complete_section_list, list_of_sections)
missing_sections_df = nutpp.create_missing_sections_df(list_of_missing_sections, list_of_regionnames)


compiled_obj_counts = nutpp.compile_nut_customregions_reports(all_files_list, "Object count")
obj_counts = nutpp.format_dataframe(compiled_obj_counts, list_of_sections, list_of_regionnames, missing_sections_df)

compiled_reg_areas = nutpp.compile_nut_customregions_reports(all_files_list, "Region area")
reg_areas = nutpp.format_dataframe(compiled_reg_areas, list_of_sections, list_of_regionnames, missing_sections_df)

compiled_mask_load = nutpp.compile_nut_customregions_reports(all_mask_files, "Load")
mask_load = nutpp.format_dataframe(compiled_mask_load, list_of_sections, list_of_regionnames, missing_sections_df).fillna(0)

object_mean_pixels = nutpp.describe_object_sizes(objects_all_file = (objectspath + 'Objects_all.csv'))    
object_mean_pixels = nutpp.complete_and_sort_object_counts(object_mean_pixels, list_of_regionnames)    

object_mean_diameters = nutpp.calculate_object_diameters(object_mean_pixels, list_of_regionnames, my_pixel_size)    

compiled_hidden_mask_load = nutpp.get_hidden_mask_load((registrationpath + subject + "_hidden_mask_loads.xlsx"), list_of_sections)
hidden_mask_load = nutpp.format_dataframe(compiled_hidden_mask_load, list_of_sections, list_of_regionnames, missing_sections_df).fillna(0).astype(float)


## PERFORM CALCULATIONS

maskcorrected_object_counts, maskcorrected_region_area = nutpp.mask_correction(obj_counts, reg_areas, mask_load, hidden_mask_load, pixel_size = my_pixel_size, complete_section_list = complete_section_list)    
    
abcorrected_object_counts = nutpp.abercrombie_correction(object_mean_diameters, maskcorrected_object_counts, complete_section_list, my_section_thickness)
    
densities_2D, densities_3D = nutpp.calculate_densities(abcorrected_object_counts, maskcorrected_region_area, my_section_thickness)

densities_3D_interpolated = nutpp.interpolate_data(densities_3D, complete_section_list)

densities_2D_interpolated = nutpp.interpolate_data(densities_2D, complete_section_list)

regions_interpolated = nutpp.interpolate_data(maskcorrected_region_area, complete_section_list)

object_counts_interpolated = densities_2D_interpolated * regions_interpolated


## EXPORT TO EXCEL

writer = pd.ExcelWriter(nutilpath + 'output_compiled_' + subject + '.xlsx', engine='xlsxwriter')

maskcorrected_object_counts.to_excel(writer, sheet_name='maskcorrected_object_counts', index=True, na_rep = "NaN")
abcorrected_object_counts.to_excel(writer, sheet_name='abcorrected_object_counts', index=True, na_rep = "NaN")
densities_3D_interpolated.to_excel(writer, sheet_name='densities_3D_interpolated', index=True, na_rep = "NaN")
regions_interpolated.to_excel(writer, sheet_name='regions_interpolated', index=True, na_rep = "NaN")
object_counts_interpolated.to_excel(writer, sheet_name='object_counts_interpolated', index=True, na_rep = "NaN")
object_mean_diameters.to_excel(writer, sheet_name='object_mean_diameters', index=True, na_rep = "NaN")
object_mean_pixels.to_excel(writer, sheet_name='object_mean_pixels', index=True, na_rep = "NaN")
mask_load.to_excel(writer, sheet_name='mask_load', index=True, na_rep = "NaN")
hidden_mask_load.to_excel(writer, sheet_name='hidden_mask_load', index=True, na_rep = "NaN")

writer.save()





