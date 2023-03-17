# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:29:51 2023

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
import matplotlib.pyplot as plt


###########################################################################################################################

## Set up paths
D1R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_densities.xlsx"
D1R_totals_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_total_numbers.xlsx"
D1R_cell_sizes_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_cell_pixels.xlsx"


D1R_densities = pd.read_excel(D1R_densities_path)
D1R_densities["Area prostriata"] = np.nan
D1R_totals = pd.read_excel(D1R_totals_path)
D1R_cell_sizes = pd.read_excel(D1R_cell_sizes_path)



D2R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_densities.xlsx"
D2R_totals_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_total_numbers.xlsx"
D2R_cell_sizes_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_cell_pixels.xlsx"


D2R_densities = pd.read_excel(D2R_densities_path)
D2R_densities["Area prostriata"] = np.nan
D2R_totals = pd.read_excel(D2R_totals_path)
D2R_cell_sizes = pd.read_excel(D2R_cell_sizes_path)

## Get custom region names from excel file:

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'
read_customregs = pd.read_csv(customregsfile, sep = ";")


## list regions at various levels of hierarchy
hierarchy_regs = (read_customregs['Hierarchy'].unique()).tolist()
major_regs = (read_customregs['Hierarchy_major'].unique()).tolist()
medium_hier_regs = (read_customregs['Hierarchy_medium'].unique()).tolist()


regions_to_hierarchy_dict = dict(zip(read_customregs['Region name'], read_customregs['Hierarchy']))



#medium_hierarchy_dict = dict(zip(read_customregs['Region name'], read_customregs['Hierarchy_medium']))
#medium_to_major_dict = dict(zip(read_customregs['Hierarchy_medium'], read_customregs['Hierarchy_major']))



###########################################################################################################################

## Summarize densities by hierarchy


def group_data_by_hierarchy(datafile, hreg_list, reg_to_hreg_dict, id_column_list = []):
    
    hierarchy_dict = {}
    df_list = []
    nan_list = []
    num_regions_list = []
    
    for hreg in hreg_list:
        included_regions = [k for k,v in reg_to_hreg_dict.items() if v == hreg]
        hierarchy_dict[hreg] = included_regions    
        
        nan_count = datafile[hierarchy_dict[hreg]].isna().sum(axis=1)
        avg_value = datafile[hierarchy_dict[hreg]].mean(axis=1)
        
        new_column = (pd.DataFrame([avg_value]).transpose())
        new_column.columns = [hreg]
        df_list.append(new_column)   
        
        nan_column = (pd.DataFrame([nan_count]).transpose())
        nan_column.columns = [hreg]
        nan_list.append(nan_column)
        
        num_regions = len(included_regions)
        num_regions_list.append(num_regions)


    df = pd.concat(df_list, axis = 1)
    
#    nan_df = pd.concat(nan_list, axis = 1)
#    num_regions_df = pd.DataFrame(num_regions_list).transpose()
#    num_regions_df.columns = hierarchy_regs
#    num_regions_df = pd.concat([num_regions_df]*len(nan_df), ignore_index=True)

    #nan_filter = ((num_regions_df / 2) >= (nan_df))

    #df_masked = df[nan_filter]
    
    id_cols = datafile[id_column_list]
    full_df = pd.concat([id_cols, df], axis = 1)
    
    return(full_df)





D1R_hierarchical_densities = group_data_by_hierarchy(D1R_densities, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_densities = group_data_by_hierarchy(D2R_densities, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])

D1R_hierarchical_totals = group_data_by_hierarchy(D1R_totals, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_totals = group_data_by_hierarchy(D2R_totals, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])

D1R_hierarchical_cell_sizes = group_data_by_hierarchy(D1R_cell_sizes, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_cell_sizes = group_data_by_hierarchy(D2R_cell_sizes, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])


D1R_hierarchical_densities.to_excel("D1R_hierarchical_densities.xlsx")
D2R_hierarchical_densities.to_excel("D2R_hierarchical_densities.xlsx")

D1R_hierarchical_totals.to_excel("D1R_hierarchical_totals.xlsx")
D2R_hierarchical_totals.to_excel("D2R_hierarchical_totals.xlsx")

D1R_hierarchical_cell_sizes.to_excel("D1R_hierarchical_cell_sizes.xlsx")
D2R_hierarchical_cell_sizes.to_excel("D2R_hierarchical_cell_sizes.xlsx")


## Get and save descriptive statistics

def get_descriptive_statistics(densityfile, totalfile, cellsizefile, filesuffix = ""):

    densities_descriptives_by_age = densityfile.groupby("age").describe()
    totals_descriptives_by_age = totalfile.groupby("age").describe()
    cell_sizes_descriptives_by_age = cellsizefile.groupby("age").describe()
    
    with pd.ExcelWriter(r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\descriptive_statistics_" + filesuffix + ".xlsx") as writer:
        densities_descriptives_by_age.to_excel(writer, sheet_name = "Densities_by_age")
        totals_descriptives_by_age.to_excel(writer, sheet_name = "Totals_by_age")
        cell_sizes_descriptives_by_age.to_excel(writer, sheet_name = "Cellsizes_by_age")
        

get_descriptive_statistics(D1R_densities, D1R_totals, D1R_cell_sizes, filesuffix = "D1R")
get_descriptive_statistics(D2R_densities, D2R_totals, D2R_cell_sizes, filesuffix = "D2R")

get_descriptive_statistics(D1R_hierarchical_densities, D1R_hierarchical_totals, D1R_hierarchical_cell_sizes, filesuffix = "hierarchical_D1R")
get_descriptive_statistics(D2R_hierarchical_densities, D2R_hierarchical_totals, D2R_hierarchical_cell_sizes, filesuffix = "hierarchical_D2R")


## Get counts and mean values per age group

D1R_count = (D1R_densities.groupby("age").count()).iloc[0:,2:]
D2R_count = (D2R_densities.groupby("age").count()).iloc[0:,2:]

D1R_densities_mean = D1R_densities.groupby("age").mean()
D2R_densities_mean = D2R_densities.groupby("age").mean()    

D1R_cell_sizes_mean = D1R_cell_sizes.groupby("age").mean()
D2R_cell_sizes_mean = D2R_cell_sizes.groupby("age").mean()   

D1R_totals_mean = D1R_totals.groupby("age").mean()
D2R_totals_mean = D2R_totals.groupby("age").mean() 

D1R_hierarchical_densities_mean = D1R_hierarchical_densities.groupby("age").mean()
D2R_hierarchical_densities_mean = D2R_hierarchical_densities.groupby("age").mean()

D1R_hierarchical_densities_count = (D1R_hierarchical_densities.groupby("age").count()).iloc[0:,2:]
D2R_hierarchical_densities_count = (D2R_hierarchical_densities.groupby("age").count()).iloc[0:,2:]

### Calculate ratios


def calculate_ratio(df1, df2, countdf1 = '', countdf2 = '', countfilter = "yes", count_lim = 3):
    ratio = (df1 / df2)
    
    if countfilter == "yes":
        filter1 = countdf1 < count_lim
        filter2 = countdf2 < count_lim
        
        ratio[filter1] = np.nan
        ratio[filter2] = np.nan
        return(ratio)
    
    else:
        return(ratio)
    


### calculate D1R/D2R ratios

D1R_D2R_ratio = calculate_ratio(D1R_densities_mean, D2R_densities_mean, D1R_count, D2R_count)
D1R_D2R_ratio = D1R_D2R_ratio.transpose()
D1R_D2R_ratio.to_excel("d1-d2_ratio.xlsx")

D1R_D2R_ratio_hierarchical = calculate_ratio(D1R_hierarchical_densities_mean, D2R_hierarchical_densities_mean, 
                                             D1R_hierarchical_densities_count, D2R_hierarchical_densities_count)
D1R_D2R_ratio_hierarchical = D1R_D2R_ratio_hierarchical.transpose()
D1R_D2R_ratio_hierarchical.to_excel("d1-d2_ratio_hierarchical.xlsx")





### calculate male / female ratio for D1R

ages = ["P17", "P25", "P35", "P49", "P70"]

# fine region ratios: 
D1R_grouped_means = D1R_densities.groupby(["age", "sex"]).mean()
D1R_grouped_counts = D1R_densities.groupby(["age", "sex"]).count()


D1R_m17_mean, D1R_m25_mean, D1R_m35_mean, D1R_m49_mean, D1R_m70_mean = ((D1R_grouped_means.loc[age, "M"]) for age in ages)
D1R_f17_mean, D1R_f25_mean, D1R_f35_mean, D1R_f49_mean, D1R_f70_mean = ((D1R_grouped_means.loc[age, "F"]) for age in ages)

D1R_m17_count, D1R_m25_count, D1R_m35_count, D1R_m49_count, D1R_m70_count = ((D1R_grouped_counts.loc[age, "M"])[1:] for age in ages)
D1R_f17_count, D1R_f25_count, D1R_f35_count, D1R_f49_count, D1R_f70_count = ((D1R_grouped_counts.loc[age, "F"])[1:] for age in ages)

D1R_P17_M_F_ratio = calculate_ratio(D1R_m17_mean, D1R_f17_mean, D1R_m17_count, D1R_f17_count)
D1R_P25_M_F_ratio = calculate_ratio(D1R_m25_mean, D1R_f25_mean, D1R_m25_count, D1R_f25_count)
D1R_P35_M_F_ratio = calculate_ratio(D1R_m35_mean, D1R_f35_mean, D1R_m35_count, D1R_f35_count)
D1R_P49_M_F_ratio = calculate_ratio(D1R_m49_mean, D1R_f49_mean, D1R_m49_count, D1R_f49_count)
D1R_P70_M_F_ratio = calculate_ratio(D1R_m70_mean, D1R_f70_mean, D1R_m70_count, D1R_f70_count)

D1R_male_female_ratios = pd.concat([D1R_P17_M_F_ratio, D1R_P25_M_F_ratio, D1R_P35_M_F_ratio, D1R_P49_M_F_ratio, D1R_P70_M_F_ratio], axis = 1)
D1R_male_female_ratios.columns = [ages]

D1R_mean_values = D1R_grouped_means.transpose()

# broader regions ratios:
    
D1R_hier_grouped_means = D1R_hierarchical_densities.groupby(["age", "sex"]).mean()
D1R_hier_grouped_counts = D1R_hierarchical_densities.groupby(["age", "sex"]).count()


D1R_hier_m17_mean, D1R_hier_m25_mean, D1R_hier_m35_mean, D1R_hier_m49_mean, D1R_hier_m70_mean = ((D1R_hier_grouped_means.loc[age, "M"]) for age in ages)
D1R_hier_f17_mean, D1R_hier_f25_mean, D1R_hier_f35_mean, D1R_hier_f49_mean, D1R_hier_f70_mean = ((D1R_hier_grouped_means.loc[age, "F"]) for age in ages)

D1R_hier_m17_count, D1R_hier_m25_count, D1R_hier_m35_count, D1R_hier_m49_count, D1R_hier_m70_count = ((D1R_hier_grouped_counts.loc[age, "M"])[1:] for age in ages)
D1R_hier_f17_count, D1R_hier_f25_count, D1R_hier_f35_count, D1R_hier_f49_count, D1R_hier_f70_count = ((D1R_hier_grouped_counts.loc[age, "F"])[1:] for age in ages)

D1R_hier_P17_M_F_ratio = calculate_ratio(D1R_hier_m17_mean, D1R_hier_f17_mean, D1R_hier_m17_count, D1R_hier_f17_count)
D1R_hier_P25_M_F_ratio = calculate_ratio(D1R_hier_m25_mean, D1R_hier_f25_mean, D1R_hier_m25_count, D1R_hier_f25_count)
D1R_hier_P35_M_F_ratio = calculate_ratio(D1R_hier_m35_mean, D1R_hier_f35_mean, D1R_hier_m35_count, D1R_hier_f35_count)
D1R_hier_P49_M_F_ratio = calculate_ratio(D1R_hier_m49_mean, D1R_hier_f49_mean, D1R_hier_m49_count, D1R_hier_f49_count)
D1R_hier_P70_M_F_ratio = calculate_ratio(D1R_hier_m70_mean, D1R_hier_f70_mean, D1R_hier_m70_count, D1R_hier_f70_count)

D1R_hier_male_female_ratios = pd.concat([D1R_hier_P17_M_F_ratio, D1R_hier_P25_M_F_ratio, D1R_hier_P35_M_F_ratio, D1R_hier_P49_M_F_ratio, D1R_hier_P70_M_F_ratio], axis = 1)
D1R_hier_male_female_ratios.columns = [ages]

D1R_hier_mean_values = D1R_hier_grouped_means.transpose()



### calculate male / female ratio for D2R

D2R_grouped_means = D2R_densities.groupby(["age", "sex"]).mean()
D2R_grouped_counts = D2R_densities.groupby(["age", "sex"]).count()



D2R_m17_mean, D2R_m25_mean, D2R_m35_mean, D2R_m49_mean, D2R_m70_mean = ((D2R_grouped_means.loc[age, "M"]) for age in ages)
D2R_f17_mean, D2R_f25_mean, D2R_f35_mean, D2R_f49_mean, D2R_f70_mean = ((D2R_grouped_means.loc[age, "F"]) for age in ages)

D2R_m17_count, D2R_m25_count, D2R_m35_count, D2R_m49_count, D2R_m70_count = ((D2R_grouped_counts.loc[age, "M"])[1:] for age in ages)
D2R_f17_count, D2R_f25_count, D2R_f35_count, D2R_f49_count, D2R_f70_count = ((D2R_grouped_counts.loc[age, "F"])[1:] for age in ages)

D2R_P17_M_F_ratio = calculate_ratio(D2R_m17_mean, D2R_f17_mean, D2R_m17_count, D2R_f17_count)
D2R_P25_M_F_ratio = calculate_ratio(D2R_m25_mean, D2R_f25_mean, D2R_m25_count, D2R_f25_count)
D2R_P35_M_F_ratio = calculate_ratio(D2R_m35_mean, D2R_f35_mean, D2R_m35_count, D2R_f35_count)
D2R_P49_M_F_ratio = calculate_ratio(D2R_m49_mean, D2R_f49_mean, D2R_m49_count, D2R_f49_count)
D2R_P70_M_F_ratio = calculate_ratio(D2R_m70_mean, D2R_f70_mean, D2R_m70_count, D2R_f70_count)

D2R_male_female_ratios = pd.concat([D2R_P17_M_F_ratio, D2R_P25_M_F_ratio, D2R_P35_M_F_ratio, D2R_P49_M_F_ratio, D2R_P70_M_F_ratio], axis = 1)
D2R_male_female_ratios.columns = [ages]

D2R_mean_values = D2R_grouped_means.transpose()


# broader regions ratios:
    
D2R_hier_grouped_means = D2R_hierarchical_densities.groupby(["age", "sex"]).mean()
D2R_hier_grouped_counts = D2R_hierarchical_densities.groupby(["age", "sex"]).count()


D2R_hier_m17_mean, D2R_hier_m25_mean, D2R_hier_m35_mean, D2R_hier_m49_mean, D2R_hier_m70_mean = ((D2R_hier_grouped_means.loc[age, "M"]) for age in ages)
D2R_hier_f17_mean, D2R_hier_f25_mean, D2R_hier_f35_mean, D2R_hier_f49_mean, D2R_hier_f70_mean = ((D2R_hier_grouped_means.loc[age, "F"]) for age in ages)

D2R_hier_m17_count, D2R_hier_m25_count, D2R_hier_m35_count, D2R_hier_m49_count, D2R_hier_m70_count = ((D2R_hier_grouped_counts.loc[age, "M"])[1:] for age in ages)
D2R_hier_f17_count, D2R_hier_f25_count, D2R_hier_f35_count, D2R_hier_f49_count, D2R_hier_f70_count = ((D2R_hier_grouped_counts.loc[age, "F"])[1:] for age in ages)

D2R_hier_P17_M_F_ratio = calculate_ratio(D2R_hier_m17_mean, D2R_hier_f17_mean, D2R_hier_m17_count, D2R_hier_f17_count)
D2R_hier_P25_M_F_ratio = calculate_ratio(D2R_hier_m25_mean, D2R_hier_f25_mean, D2R_hier_m25_count, D2R_hier_f25_count)
D2R_hier_P35_M_F_ratio = calculate_ratio(D2R_hier_m35_mean, D2R_hier_f35_mean, D2R_hier_m35_count, D2R_hier_f35_count)
D2R_hier_P49_M_F_ratio = calculate_ratio(D2R_hier_m49_mean, D2R_hier_f49_mean, D2R_hier_m49_count, D2R_hier_f49_count)
D2R_hier_P70_M_F_ratio = calculate_ratio(D2R_hier_m70_mean, D2R_hier_f70_mean, D2R_hier_m70_count, D2R_hier_f70_count)

D2R_hier_male_female_ratios = pd.concat([D2R_hier_P17_M_F_ratio, D2R_hier_P25_M_F_ratio, D2R_hier_P35_M_F_ratio, D2R_hier_P49_M_F_ratio, D2R_hier_P70_M_F_ratio], axis = 1)
D2R_hier_male_female_ratios.columns = [ages]

D2R_hier_mean_values = D2R_hier_grouped_means.transpose()



# sex-specific d1 d2 ratios


#male

male_d1_d2_ratios_P17 = calculate_ratio(D1R_hier_m17_mean, D2R_hier_m17_mean, D1R_hier_m17_count, D2R_hier_m17_count)
male_d1_d2_ratios_P25 = calculate_ratio(D1R_hier_m25_mean, D2R_hier_m25_mean, D1R_hier_m25_count, D2R_hier_m25_count)
male_d1_d2_ratios_P35 = calculate_ratio(D1R_hier_m35_mean, D2R_hier_m35_mean, D1R_hier_m35_count, D2R_hier_m35_count)
male_d1_d2_ratios_P49 = calculate_ratio(D1R_hier_m49_mean, D2R_hier_m49_mean, D1R_hier_m49_count, D2R_hier_m49_count)
male_d1_d2_ratios_P70 = calculate_ratio(D1R_hier_m70_mean, D2R_hier_m70_mean, D1R_hier_m70_count, D2R_hier_m70_count)

male_d1_d2_ratios = pd.concat([male_d1_d2_ratios_P17, male_d1_d2_ratios_P25, male_d1_d2_ratios_P35, male_d1_d2_ratios_P49, male_d1_d2_ratios_P70], axis = 1)
male_d1_d2_ratios.columns = [ages]


#female

female_d1_d2_ratios_P17 = calculate_ratio(D1R_hier_f17_mean, D2R_hier_f17_mean, D1R_hier_f17_count, D2R_hier_f17_count)
female_d1_d2_ratios_P25 = calculate_ratio(D1R_hier_f25_mean, D2R_hier_f25_mean, D1R_hier_f25_count, D2R_hier_f25_count)
female_d1_d2_ratios_P35 = calculate_ratio(D1R_hier_f35_mean, D2R_hier_f35_mean, D1R_hier_f35_count, D2R_hier_f35_count)
female_d1_d2_ratios_P49 = calculate_ratio(D1R_hier_f49_mean, D2R_hier_f49_mean, D1R_hier_f49_count, D2R_hier_f49_count)
female_d1_d2_ratios_P70 = calculate_ratio(D1R_hier_f70_mean, D2R_hier_f70_mean, D1R_hier_f70_count, D2R_hier_f70_count)

female_d1_d2_ratios = pd.concat([female_d1_d2_ratios_P17, female_d1_d2_ratios_P25, female_d1_d2_ratios_P35, female_d1_d2_ratios_P49, female_d1_d2_ratios_P70], axis = 1)
female_d1_d2_ratios.columns = [ages]





with pd.ExcelWriter('male_female_ratios.xlsx') as writer:
    D1R_male_female_ratios.to_excel(writer, sheet_name='D1R_male_female_ratio')
    D1R_mean_values.to_excel(writer, sheet_name='D1R_means')
    D2R_male_female_ratios.to_excel(writer, sheet_name='D2R_male_female_ratio')
    D2R_mean_values.to_excel(writer, sheet_name='D2R_means')


with pd.ExcelWriter('male_female_hierarchical_ratios.xlsx') as writer:
    D1R_hier_male_female_ratios.to_excel(writer, sheet_name='D1R_hier_male_female_ratio')
    D1R_hier_mean_values.to_excel(writer, sheet_name='D1R_hier_means')
    D2R_hier_male_female_ratios.to_excel(writer, sheet_name='D2R_hier_male_female_ratio')
    D1R_hier_mean_values.to_excel(writer, sheet_name='D2R_hier_means')



with pd.ExcelWriter('sex-specific_d1-d2_ratios.xlsx') as writer:
    male_d1_d2_ratios.to_excel(writer, sheet_name='male_d1_d2_ratios')
    female_d1_d2_ratios.to_excel(writer, sheet_name='female_d1_d2_ratios')







