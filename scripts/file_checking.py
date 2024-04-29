# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:44:34 2023

@author: ingvieb
"""




from glob import glob
import json
import pandas as pd
import os
from tqdm import tqdm



## Check the integrity of all 3D_combined JSON files

nut_coord_files = glob(r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D*R\P*\D*R_P*_*_*\07_nutil\01_output_cells\Coordinates\3D_combined.json")
all_subject_folders = glob(r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D*R\P*\D*R_P*_*_*//")


for nutil_file in tqdm(nut_coord_files):
    try:
        cloud = json.load(open(nutil_file))
    except Exception as e:
        print(e)
        print(nutil_file + ' bad file')



## Generate an excel sheet of all the included subjects

ID_list = []   
sex_list = []   
age_list = []   
receptor_list = []        
        
for folder in all_subject_folders:
    groups = (folder.split("\\")[-2]).split("_")
    ID = groups[-1]
    sex = groups[-2]
    age = groups[-3]
    receptor = groups[-4]
    
    ID_list.append(ID)
    sex_list.append(sex)
    age_list.append(age)
    receptor_list.append(receptor)
    


subject_dict = {"ID":ID_list, "age":age_list, "sex":sex_list, "receptor":receptor_list}
subject_df = pd.DataFrame(subject_dict)
group_ns = subject_df.groupby(["receptor","age","sex"]).count()
group_ns = group_ns.sort_values(['receptor','age','sex'], ascending=[True,False,False])

group_ns.to_excel("group_subject_numbers.xlsx")
subject_df.to_excel("subjects_overview.xlsx",index=False)


## Check that all subjects have equal number of nut slice coordinate files and nut masked segmentation

for ID, sex, age, receptor in zip(ID_list, sex_list, age_list, receptor_list):
    
    nut_section_coord_files = glob(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{age}\{receptor}_{age}_{sex}_{ID}\07_nutil\01_output_cells\Coordinates\3D_slice*.json")
    number_of_nut_sections = len(nut_section_coord_files)
    masked_segmentation_files = glob(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{age}\{receptor}_{age}_{sex}_{ID}\05_masked_segmentations\*.png")
    number_of_masked_segmentation_files = len(masked_segmentation_files)
    nut_report_files = glob(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{age}\{receptor}_{age}_{sex}_{ID}\07_nutil\01_output_cells\Reports\CustomRegions\CustomRegions__*")
    number_of_nut_report_files = len(nut_report_files)    
    
    if number_of_nut_sections == number_of_masked_segmentation_files:
        print("All good!")
    
    else:
        print(receptor + " " + age + " " + sex + " " + ID + " has mismatched numbers")
        print("number_of_masked_segmentation_files: " + str(number_of_masked_segmentation_files))
        print("number_of_nut_sections: " + str(number_of_nut_sections))
        print("number_of_nut_report_files: " + str(number_of_nut_report_files))





##
files_to_be_removed = []


for ID, sex, age, receptor in zip(ID_list, sex_list, age_list, receptor_list):

    # check that there are no extra files in parent folder of the subject
    subject_path = rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{age}\{receptor}_{age}_{sex}_{ID}\\"
    content = glob(subject_path + "*")
    
    if len(content) == 8:
        print("All good!")
    else:
        print("Check folder of subject " + ID)
        
    nonlin_path = subject_path + "00_nonlin_registration_files\\"
    all_files = glob(nonlin_path + "*")
    
    pngs = glob(nonlin_path + "*.png")
    hidden_mask_load = nonlin_path + ID + "_hidden_mask_loads.xlsx"
    summary_stats = nonlin_path + ID + "_nonlinear_summary_statistics.xlsx" 
    nonlin_file = nonlin_path + ID + "_nonlinear.json"
    
    list_of_relevant_files = [*pngs, hidden_mask_load, summary_stats, nonlin_file]
    for file in all_files:
        if file in list_of_relevant_files:
            continue
        else:
            files_to_be_removed.append(file)
            #os.remove(file)
    
    nutil_path = subject_path + "07_nutil\\"
    output_cells = nutil_path + "01_output_cells"
    output_masks = nutil_path + "02_output_masks"
    compiled_file = nutil_path + "output_compiled_" + ID + ".xlsx"
    nutil_path_relevant_files = [output_cells, output_masks, compiled_file]
    nutil_path_content = glob(nutil_path + "*")
    
    for file in nutil_path_content:
        if file in nutil_path_relevant_files:
            continue
        else:
            files_to_be_removed.append(file)
            #os.remove(file)
        


mask_coords_to_be_removed = []

for ID, sex, age, receptor in zip(ID_list, sex_list, age_list, receptor_list):
    
    subject_path = rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{age}\{receptor}_{age}_{sex}_{ID}\\"
    mask_coords_path = subject_path + "07_nutil\\02_output_masks\\Coordinates\\"
    mask_coords_path_content = glob(mask_coords_path + "*")
    mask_coords_to_be_removed.append(mask_coords_path_content)

mask_coords_to_be_removed = [item for sublist in mask_coords_to_be_removed for item in sublist]

df = pd.DataFrame(mask_coords_to_be_removed)
df.to_excel("to_delete.xlsx",index=False)


for maskfile in mask_coords_to_be_removed:

    os.remove(maskfile)
    
    
    
    
    
    
    
    
    
    
    


