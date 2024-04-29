# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 14:35:34 2022

@author: ingvieb
"""


import pandas as pd
import nutil_scripts.create_nut_file_functions as nff

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
metadata = resourcedir + "ids_for_nut_files.xlsx"


subjects = pd.read_excel(metadata)    

ID = subjects["ID"]
genotype = subjects["Genotype"]
age = subjects["Age"]
sex = subjects["Sex"]

# Write files to extract cells:
    
for i, g, a, s in zip(ID, genotype, age, sex):
    if a == "P49" or a == "P70":
        nff.write_nut_quant_file(filename = i + "_cells", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/01_output_cells",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_DOPAMAP.xlsx", extraction_color = "255,0,255,255", label_file = "Allen Mouse Brain 2017",
                       object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
    if a == "P35" or a == "P25" or a == "P17":
        nff.write_nut_quant_file(filename = i + "_cells", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/01_output_cells",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_Newmaster.xlsx", extraction_color = "255,0,255,255", label_file = "Custom",
                       custom_label_file = "Y:/Dopamine_receptors/Analysis/resources/atlas_volumes/labels_rev_CCF-colors.txt", object_splitting = "No", object_min_size = "4", custom_region_type = "Custom")
        
        
# Write files to extract masks:
    
for i, g, a, s in zip(ID, genotype, age, sex):
    if a == "P49" or a == "P70":
        nff.write_nut_quant_file(filename = i + "_masks", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/02_output_masks",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_DOPAMAP.xlsx", extraction_color = "0,0,0,255", label_file = "Allen Mouse Brain 2017",
                       object_splitting = "Yes", object_min_size = "4", custom_region_type = "Custom", coordinate_extraction = "None")
    if a == "P35" or a == "P25" or a == "P17":
        nff.write_nut_quant_file(filename = i + "_masks", quantifier_input_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/05_masked_segmentations", 
                       quantifier_atlas_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/06_atlas_maps",
                       xml_anchor_file = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/00_nonlin_registration_files/" + i + "_nonlinear.json",
                       quantifier_output_dir = "Y:/Dopamine_receptors/Analysis/QUINT_analysis/" + g + "/" + a + "/" + g + "_" + a + "_" + s + "_" + i + "/07_nutil/02_output_masks",
                       custom_region_file = "Y:/Dopamine_receptors/Analysis/resources/CustomRegions_Allen2017_Newmaster.xlsx", extraction_color = "0,0,0,255", label_file = "Custom",
                       custom_label_file = "Y:/Dopamine_receptors/Analysis/resources/atlas_volumes/labels_rev_CCF-colors.txt", object_splitting = "Yes", object_min_size = "4", custom_region_type = "Custom",
                       coordinate_extraction = "None")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        