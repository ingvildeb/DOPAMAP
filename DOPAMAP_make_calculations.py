# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 09:58:10 2022

@author: ingvieb
"""

import pandas as pd
import glob
import numpy as np



resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'

regionnames = pd.read_csv(customregsfile, sep=';', usecols =['Region name'])
regionnames = regionnames.values

flat_regionnames = []

for namelist in regionnames:
    for name in namelist:
        flat_regionnames.append(name)
        
regionnames = flat_regionnames

D1R_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\*\*\07_nutil/output_compiled_*.xlsx"
D1R_files = glob.glob(D1R_paths)

D2R_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\*\*\07_nutil/output_compiled_*.xlsx"
D2R_files = glob.glob(D2R_paths)


D1R_P70_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P70\*_M_*\07_nutil/output_compiled_*.xlsx"
D1R_P70_male_files = glob.glob(D1R_P70_male_paths)

D1R_P70_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P70\*_F_*\07_nutil/output_compiled_*.xlsx"
D1R_P70_female_files = glob.glob(D1R_P70_female_paths)

D1R_P49_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P49\*_M_*\07_nutil/output_compiled_*.xlsx"
D1R_P49_male_files = glob.glob(D1R_P49_male_paths)

D1R_P49_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P49\*_F_*\07_nutil/output_compiled_*.xlsx"
D1R_P49_female_files = glob.glob(D1R_P49_female_paths)

D1R_P35_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P35\*_M_*\07_nutil/output_compiled_*.xlsx"
D1R_P35_male_files = glob.glob(D1R_P35_male_paths)

D1R_P35_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P35\*_F_*\07_nutil/output_compiled_*.xlsx"
D1R_P35_female_files = glob.glob(D1R_P35_female_paths)

D1R_P25_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P25\*_M_*\07_nutil/output_compiled_*.xlsx"
D1R_P25_male_files = glob.glob(D1R_P25_male_paths)

D1R_P25_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P25\*_F_*\07_nutil/output_compiled_*.xlsx"
D1R_P25_female_files = glob.glob(D1R_P25_female_paths)

D1R_P17_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P17\*_M_*\07_nutil/output_compiled_*.xlsx"
D1R_P17_male_files = glob.glob(D1R_P17_male_paths)

D1R_P17_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P17\*_F_*\07_nutil/output_compiled_*.xlsx"
D1R_P17_female_files = glob.glob(D1R_P17_female_paths)

D2R_P70_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P70\*_M_*\07_nutil/output_compiled_*.xlsx"
D2R_P70_male_files = glob.glob(D2R_P70_male_paths)

D2R_P70_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P70\*_F_*\07_nutil/output_compiled_*.xlsx"
D2R_P70_female_files = glob.glob(D2R_P70_female_paths)

D2R_P49_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P49\*_M_*\07_nutil/output_compiled_*.xlsx"
D2R_P49_male_files = glob.glob(D2R_P49_male_paths)

D2R_P49_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P49\*_F_*\07_nutil/output_compiled_*.xlsx"
D2R_P49_female_files = glob.glob(D2R_P49_female_paths)

D2R_P35_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P35\*_M_*\07_nutil/output_compiled_*.xlsx"
D2R_P35_male_files = glob.glob(D2R_P35_male_paths)

D2R_P35_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P35\*_F_*\07_nutil/output_compiled_*.xlsx"
D2R_P35_female_files = glob.glob(D2R_P35_female_paths)

D2R_P25_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P25\*_M_*\07_nutil/output_compiled_*.xlsx"
D2R_P25_male_files = glob.glob(D2R_P25_male_paths)

D2R_P25_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P25\*_F_*\07_nutil/output_compiled_*.xlsx"
D2R_P25_female_files = glob.glob(D2R_P25_female_paths)

D2R_P17_male_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P17\*_M_*\07_nutil/output_compiled_*.xlsx"
D2R_P17_male_files = glob.glob(D2R_P17_male_paths)

D2R_P17_female_paths = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\P17\*_F_*\07_nutil/output_compiled_*.xlsx"
D2R_P17_female_files = glob.glob(D2R_P17_female_paths)

list_of_file_lists = [D1R_P70_male_files, D1R_P70_female_files, D1R_P49_male_files, D1R_P49_female_files, D1R_P35_male_files, D1R_P35_female_files, D1R_P25_male_files, D1R_P25_female_files,
                      D1R_P17_male_files, D1R_P17_female_files, D2R_P70_male_files, D2R_P70_female_files, D2R_P49_male_files, D2R_P49_female_files, D2R_P35_male_files, D2R_P35_female_files, 
                      D2R_P25_male_files, D2R_P25_female_files, D2R_P17_male_files, D2R_P17_female_files]


# for each group (receptor * age * sex), get the sheet with the 3D interpolated densities. used to remove values that deviate by 3 SDs from the mean of the region in the group.

for group in list_of_file_lists:

    list_of_density_dfs = []
    
    for file in group:
        grouping = file.split("\\")[6]
        genotype = grouping.split("_")[0]
        name = grouping.split("_")[3]
        sex = grouping.split("_")[2]
        age = grouping.split("_")[1]
        section_densities = pd.read_excel(file, sheet_name = "densities_3D_interpolated")
        section_densities.insert(0, "ID", name, True)
        section_densities.insert(0, "sex", sex, True)
        section_densities.insert(0, "age", age, True)
        list_of_density_dfs.append(section_densities)
        
    
    # compile all the density dfs into one, and remove zero values, which are not needed for the calculation
    all_densities = pd.concat(list_of_density_dfs)    
    zerofilter = (all_densities != 0)  
    all_densities = all_densities[zerofilter]  
    
    
    # generate average and mean value for each region:
    
    avg_densities = all_densities.mean()
    avg_densities = pd.DataFrame(avg_densities[1:])
    avg_densities = avg_densities.transpose()
    
    sd_densities  = all_densities.std()
    sd_densities  = pd.DataFrame(sd_densities[1:])
    sd_densities  = sd_densities.transpose()
    
    list_of_density_sds = []
    
       
    average_and_sd = pd.concat([avg_densities, sd_densities])
    
    
    excluded_values_list = []
    new_densities_list = []
    
    
    densities_df = all_densities.iloc[:,4:]
    
    # exclude the outlier values
    
    for i, j in zip(densities_df.columns, average_and_sd):
        outlier_filter = []
    
        density = densities_df[i].values
        sd = average_and_sd[j].values[1]
        mean = average_and_sd[j].values[0]
        
        for value in density:
            if (value > (mean + (3*sd))) or (value < (mean - (3*sd))) or value > 100000:
                exclude = True
            else:
                exclude = False
            outlier_filter.append(exclude)
            outlier_filter_mask = np.array(outlier_filter)

        new_density = pd.DataFrame(density)
        excluded_density = new_density[outlier_filter_mask].copy()
        new_density[outlier_filter_mask] = np.nan
        excluded_values_list.append(excluded_density)
        new_densities_list.append(new_density)
    
        
    
    animal_info = all_densities[["age", "sex", "ID"]]
    animal_info = animal_info.reset_index(drop=True)
    
    excluded_all_densities = pd.concat(excluded_values_list, axis=1)
    excluded_all_densities = excluded_all_densities.sort_index()
    
    new_all_densities = pd.concat(new_densities_list, axis=1)
    new_all_densities.columns = regionnames
    new_all_densities = pd.concat([animal_info, new_all_densities], axis=1)
    
    
                
    # write excel sheet with only the included densities
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{genotype}\{age}\{genotype}_{age}_{sex}_densities.xlsx", engine='xlsxwriter')
    new_all_densities.to_excel(writer, sheet_name='new_densities', index=True, na_rep = "NaN")
    
    writer.save()
    
    # write excel sheet with only the excluded densities
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{genotype}\{age}\{genotype}_{age}_{sex}_excluded_densities.xlsx", engine='xlsxwriter')
    excluded_all_densities.to_excel(writer, sheet_name='excluded_densities', index=True, na_rep = "NaN")
    
    writer.save()
    
    # write sheet with densities averaged across sections for each animal
    densities_per_animal = new_all_densities.groupby("ID").mean()
    densities_per_animal.insert(0, "sex", sex, True)
    densities_per_animal.insert(0, "age", age, True)
    
    
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{genotype}\{age}\{genotype}_{age}_{sex}_densities_per_animal.xlsx", engine='xlsxwriter')
    densities_per_animal.to_excel(writer, sheet_name='densities_per_animal', index=True, na_rep = "NaN")
    
    writer.save()





# compile all the densities per animal into a common sheet

receptors = ["D1R", "D2R"]
file_lists = [D1R_files, D2R_files]

for receptor in receptors:
    
    densities_per_animal_paths = rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\*/*_densities_per_animal.xlsx"
    densities_per_animal_files = glob.glob(densities_per_animal_paths)
    
    densities_per_animal_files_list = []
    
    for densityfile in densities_per_animal_files:
        density_df = pd.read_excel(densityfile)
        densities_per_animal_files_list.append(density_df)
    
    all_densities_compiled = pd.concat(densities_per_animal_files_list)
    
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{receptor}_densities.xlsx", engine='xlsxwriter')
    all_densities_compiled.to_excel(writer, sheet_name='all_densities', index=False, na_rep = "NaN")
    
    writer.save()   




## CALCULATE TOTAL NUMBERS
## 7: calculate total number IF the whole region is covered (for each column, if first row = 0 and last row = 0, then calculate total number)

section_sampling_frequency = 4
all_totals_list = []   


for receptor, file_list in zip(receptors, file_lists):
    
    for file in file_list:
        grouping = file.split("\\")[6]
        name = grouping.split("_")[3]
        sex = grouping.split("_")[2]
        age = grouping.split("_")[1]
    
        df = pd.read_excel(file, sheet_name = "object_counts_interpolated")
        df.pop("Section")
        
        region_areas = pd.read_excel(file, sheet_name = "regions_interpolated")
        region_areas.pop("Section")
    
        
        coverage_filter = []
    
        for column in region_areas:
            values = region_areas[column].values
            if values.sum() == 0:
                exclude = True
            else:
                exclude = False
            
            coverage_filter.append(exclude)
            
        coverage_filter = pd.DataFrame(coverage_filter)
        coverage_filter = coverage_filter.transpose()
        coverage_filter.columns = regionnames
        
    
        total_numbers = []
        
        
        for column in df:
            raw_number = df[column].values
                    #print(raw_number)
            if (raw_number[0] == 0) and (raw_number[-1] == 0):
                total = raw_number.sum(axis=0)
                total_numbers.append(total)
            else:
                total_numbers.append(np.nan)    
                
                            
        total_numbers_df = pd.DataFrame(total_numbers)
        total_numbers_df = total_numbers_df * section_sampling_frequency
        total_numbers_df = total_numbers_df.transpose()
        total_numbers_df.columns = regionnames
        total_numbers_df = total_numbers_df[~coverage_filter]
        total_numbers_df.insert(0, "Sex", sex, True)
        total_numbers_df.insert(0, "Age", age, True)
        total_numbers_df.insert(0, "ID", name, True)
        all_totals_list.append(total_numbers_df)
    
    
    
    all_totals = pd.concat(all_totals_list)
        
        
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{receptor}_total_numbers.xlsx", engine='xlsxwriter')
    all_totals.to_excel(writer, sheet_name='all_totals', index=False, na_rep = "NaN")
    
    writer.save()    

        

## compile all cell sizes in pixels to a common sheet
all_sizes_list = []   

for receptor, file_list in zip(receptors, file_lists):
    
    for file in file_list:
        grouping = file.split("\\")[6]
        name = grouping.split("_")[3]
        sex = grouping.split("_")[2]
        age = grouping.split("_")[1]
    
        sizes_df = pd.read_excel(file, sheet_name = "object_mean_pixels")
        sizes_df.insert(0, "sex", sex, True)
        sizes_df.insert(0, "age", age, True)
        sizes_df.insert(0, "ID", name, True)
        
        all_sizes_list.append(sizes_df)
        
    
    all_sizes = pd.concat(all_sizes_list)
    
    writer = pd.ExcelWriter(rf"Y:\Dopamine_receptors\Analysis\QUINT_analysis\{receptor}\{receptor}_cell_pixels.xlsx", engine='xlsxwriter')
    all_sizes.to_excel(writer, sheet_name='all_cell_pixels', index=False, na_rep = "NaN")
    
    writer.save()  

    




