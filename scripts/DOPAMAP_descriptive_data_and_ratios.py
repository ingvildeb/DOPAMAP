# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:29:51 2023

@author: ingvieb
"""

import pandas as pd
import numpy as np
import nutil_scripts.graphing_functions as ngf





""" Set up paths to data files """

# D1R

D1R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\D1R_densities.xlsx"
D1R_totals_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\D1R_total_numbers.xlsx"
D1R_cell_sizes_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\D1R_cell_pixels.xlsx"


D1R_densities = pd.read_excel(D1R_densities_path)
D1R_densities["Area prostriata"] = np.nan
D1R_totals = pd.read_excel(D1R_totals_path)
D1R_cell_sizes = pd.read_excel(D1R_cell_sizes_path)


# D2R

D2R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\D2R_densities.xlsx"
D2R_totals_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\D2R_total_numbers.xlsx"
D2R_cell_sizes_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D2R\D2R_cell_pixels.xlsx"


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




""" Get descriptive statistics for excel files """

# path to save excel files
derived_data_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\\"


## Summarize data by hierarchy and save to excel

# densities
D1R_hierarchical_densities = ngf.group_data_by_hierarchy(D1R_densities, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D1R_hierarchical_densities.to_excel("D1R_hierarchical_densities.xlsx")

D2R_hierarchical_densities = ngf.group_data_by_hierarchy(D2R_densities, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_densities.to_excel("D2R_hierarchical_densities.xlsx")

# total numbers
D1R_hierarchical_totals = ngf.group_data_by_hierarchy(D1R_totals, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D1R_hierarchical_totals.to_excel("D1R_hierarchical_totals.xlsx")

D2R_hierarchical_totals = ngf.group_data_by_hierarchy(D2R_totals, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_totals.to_excel("D2R_hierarchical_totals.xlsx")

# cell sizes
D1R_hierarchical_cell_sizes = ngf.group_data_by_hierarchy(D1R_cell_sizes, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D1R_hierarchical_cell_sizes.to_excel("D1R_hierarchical_cell_sizes.xlsx")

D2R_hierarchical_cell_sizes = ngf.group_data_by_hierarchy(D2R_cell_sizes, hierarchy_regs, regions_to_hierarchy_dict, ['ID', 'age', 'sex'])
D2R_hierarchical_cell_sizes.to_excel("D2R_hierarchical_cell_sizes.xlsx")




## Get and save descriptive statistics     
        

data_dfs = [D1R_densities, D1R_totals, D1R_cell_sizes, D2R_densities, D2R_totals, D2R_cell_sizes, D1R_hierarchical_densities, D1R_hierarchical_totals, D1R_hierarchical_cell_sizes,
            D2R_hierarchical_densities, D2R_hierarchical_totals, D2R_hierarchical_cell_sizes]
   
    
output_names = ["D1R_densities", "D1R_totals", "D1R_cell_sizes", "D2R_densities", "D2R_totals", "D2R_cell_sizes", "D1R_hierarchical_densities", "D1R_hierarchical_totals", 
                "D1R_hierarchical_cell_sizes", "D2R_hierarchical_densities", "D2R_hierarchical_totals", "D2R_hierarchical_cell_sizes"]

for data_df, output_name in zip(data_dfs, output_names):
    ngf.get_descriptive_statistics(data_df, derived_data_path + output_name + "_perAge", grouping = ["age"])

for data_df, output_name in zip(data_dfs, output_names):
    ngf.get_descriptive_statistics(data_df, derived_data_path + output_name + "_perAgeAndSex", grouping = ["age", "sex"])







""" Calculate ratios """

######### SET UP DATA FOR RATIOS

ages = ["P17", "P25", "P35", "P49", "P70"]


## GROUPED MEANS AND COUNTS PER AGE, RECEPTOR

D1R_count = (D1R_densities.groupby("age").count()).iloc[0:,2:]
D2R_count = (D2R_densities.groupby("age").count()).iloc[0:,2:]

D1R_densities_mean = D1R_densities.groupby("age").mean()
D2R_densities_mean = D2R_densities.groupby("age").mean()    

D1R_hierarchical_densities_mean = D1R_hierarchical_densities.groupby("age").mean()
D2R_hierarchical_densities_mean = D2R_hierarchical_densities.groupby("age").mean()

D1R_hierarchical_densities_count = (D1R_hierarchical_densities.groupby("age").count()).iloc[0:,2:]
D2R_hierarchical_densities_count = (D2R_hierarchical_densities.groupby("age").count()).iloc[0:,2:]

### GROUPED MEANS AND COUNTS PER AGE, SEX, RECEPTOR

# custom regions level

D1R_grouped_means = D1R_densities.groupby(["age", "sex"]).mean()
D1R_grouped_counts = D1R_densities.groupby(["age", "sex"]).count()

D2R_grouped_means = D2R_densities.groupby(["age", "sex"]).mean()
D2R_grouped_counts = D2R_densities.groupby(["age", "sex"]).count()

# hierarchical regions level

D1R_hier_grouped_means = D1R_hierarchical_densities.groupby(["age", "sex"]).mean()
D1R_hier_grouped_counts = D1R_hierarchical_densities.groupby(["age", "sex"]).count()

D2R_hier_grouped_means = D2R_hierarchical_densities.groupby(["age", "sex"]).mean()
D2R_hier_grouped_counts = D2R_hierarchical_densities.groupby(["age", "sex"]).count()


# EXTRACT MEAN AND COUNT VALUE FOR EACH GROUP

# custom regions level

D1R_m17_mean, D1R_m25_mean, D1R_m35_mean, D1R_m49_mean, D1R_m70_mean = ((D1R_grouped_means.loc[age, "M"]) for age in ages)
D1R_f17_mean, D1R_f25_mean, D1R_f35_mean, D1R_f49_mean, D1R_f70_mean = ((D1R_grouped_means.loc[age, "F"]) for age in ages)

D1R_m17_count, D1R_m25_count, D1R_m35_count, D1R_m49_count, D1R_m70_count = ((D1R_grouped_counts.loc[age, "M"])[1:] for age in ages)
D1R_f17_count, D1R_f25_count, D1R_f35_count, D1R_f49_count, D1R_f70_count = ((D1R_grouped_counts.loc[age, "F"])[1:] for age in ages)

D2R_m17_mean, D2R_m25_mean, D2R_m35_mean, D2R_m49_mean, D2R_m70_mean = ((D2R_grouped_means.loc[age, "M"]) for age in ages)
D2R_f17_mean, D2R_f25_mean, D2R_f35_mean, D2R_f49_mean, D2R_f70_mean = ((D2R_grouped_means.loc[age, "F"]) for age in ages)

D2R_m17_count, D2R_m25_count, D2R_m35_count, D2R_m49_count, D2R_m70_count = ((D2R_grouped_counts.loc[age, "M"])[1:] for age in ages)
D2R_f17_count, D2R_f25_count, D2R_f35_count, D2R_f49_count, D2R_f70_count = ((D2R_grouped_counts.loc[age, "F"])[1:] for age in ages)

# hierarchical regions level

D1R_hier_m17_mean, D1R_hier_m25_mean, D1R_hier_m35_mean, D1R_hier_m49_mean, D1R_hier_m70_mean = ((D1R_hier_grouped_means.loc[age, "M"]) for age in ages)
D1R_hier_f17_mean, D1R_hier_f25_mean, D1R_hier_f35_mean, D1R_hier_f49_mean, D1R_hier_f70_mean = ((D1R_hier_grouped_means.loc[age, "F"]) for age in ages)

D1R_hier_m17_count, D1R_hier_m25_count, D1R_hier_m35_count, D1R_hier_m49_count, D1R_hier_m70_count = ((D1R_hier_grouped_counts.loc[age, "M"])[1:] for age in ages)
D1R_hier_f17_count, D1R_hier_f25_count, D1R_hier_f35_count, D1R_hier_f49_count, D1R_hier_f70_count = ((D1R_hier_grouped_counts.loc[age, "F"])[1:] for age in ages)

D2R_hier_m17_mean, D2R_hier_m25_mean, D2R_hier_m35_mean, D2R_hier_m49_mean, D2R_hier_m70_mean = ((D2R_hier_grouped_means.loc[age, "M"]) for age in ages)
D2R_hier_f17_mean, D2R_hier_f25_mean, D2R_hier_f35_mean, D2R_hier_f49_mean, D2R_hier_f70_mean = ((D2R_hier_grouped_means.loc[age, "F"]) for age in ages)

D2R_hier_m17_count, D2R_hier_m25_count, D2R_hier_m35_count, D2R_hier_m49_count, D2R_hier_m70_count = ((D2R_hier_grouped_counts.loc[age, "M"])[1:] for age in ages)
D2R_hier_f17_count, D2R_hier_f25_count, D2R_hier_f35_count, D2R_hier_f49_count, D2R_hier_f70_count = ((D2R_hier_grouped_counts.loc[age, "F"])[1:] for age in ages)



### OVERALL D1:D2 RATIO (male / female data combined)

D1R_D2R_ratio = ngf.calculate_ratio(D1R_densities_mean, D2R_densities_mean, D1R_count, D2R_count)
D1R_D2R_ratio = D1R_D2R_ratio.transpose()
D1R_D2R_ratio.to_excel("d1-d2_ratio.xlsx")

D1R_D2R_ratio_hierarchical = ngf.calculate_ratio(D1R_hierarchical_densities_mean, D2R_hierarchical_densities_mean, 
                                             D1R_hierarchical_densities_count, D2R_hierarchical_densities_count)

D1R_D2R_ratio_hierarchical = D1R_D2R_ratio_hierarchical.transpose()
D1R_D2R_ratio_hierarchical.to_excel("d1-d2_ratio_hierarchical.xlsx")



# SEX SPECIFIC D1:D2 RATIO

# male

male_d1_d2_ratios_P17 = ngf.calculate_ratio(D1R_hier_m17_mean, D2R_hier_m17_mean, D1R_hier_m17_count, D2R_hier_m17_count)
male_d1_d2_ratios_P25 = ngf.calculate_ratio(D1R_hier_m25_mean, D2R_hier_m25_mean, D1R_hier_m25_count, D2R_hier_m25_count)
male_d1_d2_ratios_P35 = ngf.calculate_ratio(D1R_hier_m35_mean, D2R_hier_m35_mean, D1R_hier_m35_count, D2R_hier_m35_count)
male_d1_d2_ratios_P49 = ngf.calculate_ratio(D1R_hier_m49_mean, D2R_hier_m49_mean, D1R_hier_m49_count, D2R_hier_m49_count)
male_d1_d2_ratios_P70 = ngf.calculate_ratio(D1R_hier_m70_mean, D2R_hier_m70_mean, D1R_hier_m70_count, D2R_hier_m70_count)

male_d1_d2_ratios = pd.concat([male_d1_d2_ratios_P17, male_d1_d2_ratios_P25, male_d1_d2_ratios_P35, male_d1_d2_ratios_P49, male_d1_d2_ratios_P70], axis = 1)
male_d1_d2_ratios.columns = [ages]


# female

female_d1_d2_ratios_P17 = ngf.calculate_ratio(D1R_hier_f17_mean, D2R_hier_f17_mean, D1R_hier_f17_count, D2R_hier_f17_count)
female_d1_d2_ratios_P25 = ngf.calculate_ratio(D1R_hier_f25_mean, D2R_hier_f25_mean, D1R_hier_f25_count, D2R_hier_f25_count)
female_d1_d2_ratios_P35 = ngf.calculate_ratio(D1R_hier_f35_mean, D2R_hier_f35_mean, D1R_hier_f35_count, D2R_hier_f35_count)
female_d1_d2_ratios_P49 = ngf.calculate_ratio(D1R_hier_f49_mean, D2R_hier_f49_mean, D1R_hier_f49_count, D2R_hier_f49_count)
female_d1_d2_ratios_P70 = ngf.calculate_ratio(D1R_hier_f70_mean, D2R_hier_f70_mean, D1R_hier_f70_count, D2R_hier_f70_count)

female_d1_d2_ratios = pd.concat([female_d1_d2_ratios_P17, female_d1_d2_ratios_P25, female_d1_d2_ratios_P35, female_d1_d2_ratios_P49, female_d1_d2_ratios_P70], axis = 1)
female_d1_d2_ratios.columns = [ages]


with pd.ExcelWriter('sex-specific_d1-d2_ratios.xlsx') as writer:
    male_d1_d2_ratios.to_excel(writer, sheet_name='male_d1_d2_ratios')
    female_d1_d2_ratios.to_excel(writer, sheet_name='female_d1_d2_ratios')




# INDIVIDUAL VALUES FOR D1:D2 RELATIVE PROPORTION


list_of_individual_ratios = []
for i, j in D1R_hierarchical_densities.iterrows():
    age = j["age"]
    sex = j["sex"]
    ID = j["ID"]
    D2_values = D2R_hier_grouped_means.loc[age,sex]
    D1_values = j[3:]

    relative_ratio = ((D1_values-D2_values) / (D1_values+D2_values))
    df = pd.DataFrame(relative_ratio)
    df.columns=[ID]
    df = df.transpose()
    list_of_individual_ratios.append(df)

relative_ratio_df = pd.concat(list_of_individual_ratios)
relative_ratio_df.index.name = 'ID'
relative_ratio_df = relative_ratio_df.reset_index()
relative_ratio_df.insert(1, "age", D1R_hierarchical_densities["age"])
relative_ratio_df.insert(2, "sex", D1R_hierarchical_densities["sex"], True)


list_of_individual_D2_ratios = []
for i, j in D2R_hierarchical_densities.iterrows():
    age = j["age"]
    sex = j["sex"]
    ID = j["ID"]
    D2_means = D2R_hier_grouped_means.loc[age,sex]
    D2_values = j[3:]

    relative_D2_ratio = ((D2_values-D2_means) / (D2_values+D2_means))
    df_D2 = pd.DataFrame(relative_D2_ratio)
    df_D2.columns=[ID]
    df_D2 = df_D2.transpose()
    list_of_individual_D2_ratios.append(df_D2)

relative_ratio_D2_df = pd.concat(list_of_individual_D2_ratios)
relative_ratio_D2_df.index.name = 'ID'
relative_ratio_D2_df = relative_ratio_D2_df.reset_index()
relative_ratio_D2_df.insert(1, "age", D2R_hierarchical_densities["age"])
relative_ratio_D2_df.insert(2, "sex", D2R_hierarchical_densities["sex"], True)

with pd.ExcelWriter('individual-relative-proportions.xlsx') as writer:
    relative_ratio_df.to_excel(writer, sheet_name='d1_d2_proportions')
    relative_ratio_D2_df.to_excel(writer, sheet_name='d2_to_d2')


# SEX SPECIFIC D1:D2 RELATIVE PROPORTION

# male

male_d1_d2_ratios_P17 = ngf.calculate_relative_expression(D1R_hier_m17_mean, D2R_hier_m17_mean, D1R_hier_m17_count, D2R_hier_m17_count)
male_d1_d2_ratios_P25 = ngf.calculate_relative_expression(D1R_hier_m25_mean, D2R_hier_m25_mean, D1R_hier_m25_count, D2R_hier_m25_count)
male_d1_d2_ratios_P35 = ngf.calculate_relative_expression(D1R_hier_m35_mean, D2R_hier_m35_mean, D1R_hier_m35_count, D2R_hier_m35_count)
male_d1_d2_ratios_P49 = ngf.calculate_relative_expression(D1R_hier_m49_mean, D2R_hier_m49_mean, D1R_hier_m49_count, D2R_hier_m49_count)
male_d1_d2_ratios_P70 = ngf.calculate_relative_expression(D1R_hier_m70_mean, D2R_hier_m70_mean, D1R_hier_m70_count, D2R_hier_m70_count)

male_d1_d2_ratios = pd.concat([male_d1_d2_ratios_P17, male_d1_d2_ratios_P25, male_d1_d2_ratios_P35, male_d1_d2_ratios_P49, male_d1_d2_ratios_P70], axis = 1)
male_d1_d2_ratios.columns = [ages]


# female

female_d1_d2_ratios_P17 = ngf.calculate_relative_expression(D1R_hier_f17_mean, D2R_hier_f17_mean, D1R_hier_f17_count, D2R_hier_f17_count)
female_d1_d2_ratios_P25 = ngf.calculate_relative_expression(D1R_hier_f25_mean, D2R_hier_f25_mean, D1R_hier_f25_count, D2R_hier_f25_count)
female_d1_d2_ratios_P35 = ngf.calculate_relative_expression(D1R_hier_f35_mean, D2R_hier_f35_mean, D1R_hier_f35_count, D2R_hier_f35_count)
female_d1_d2_ratios_P49 = ngf.calculate_relative_expression(D1R_hier_f49_mean, D2R_hier_f49_mean, D1R_hier_f49_count, D2R_hier_f49_count)
female_d1_d2_ratios_P70 = ngf.calculate_relative_expression(D1R_hier_f70_mean, D2R_hier_f70_mean, D1R_hier_f70_count, D2R_hier_f70_count)

female_d1_d2_ratios = pd.concat([female_d1_d2_ratios_P17, female_d1_d2_ratios_P25, female_d1_d2_ratios_P35, female_d1_d2_ratios_P49, female_d1_d2_ratios_P70], axis = 1)
female_d1_d2_ratios.columns = [ages]


with pd.ExcelWriter('sex-specific_d1-d2_relativeExpression.xlsx') as writer:
    male_d1_d2_ratios.to_excel(writer, sheet_name='male_d1_d2_relativeExpression')
    female_d1_d2_ratios.to_excel(writer, sheet_name='female_d1_d2_relativeExpression')



### MALE / FEMALE RATIO FOR D1R (not used in paper)

# custom regions level 


D1R_P17_M_F_ratio = ngf.calculate_ratio(D1R_m17_mean, D1R_f17_mean, D1R_m17_count, D1R_f17_count)
D1R_P25_M_F_ratio = ngf.calculate_ratio(D1R_m25_mean, D1R_f25_mean, D1R_m25_count, D1R_f25_count)
D1R_P35_M_F_ratio = ngf.calculate_ratio(D1R_m35_mean, D1R_f35_mean, D1R_m35_count, D1R_f35_count)
D1R_P49_M_F_ratio = ngf.calculate_ratio(D1R_m49_mean, D1R_f49_mean, D1R_m49_count, D1R_f49_count)
D1R_P70_M_F_ratio = ngf.calculate_ratio(D1R_m70_mean, D1R_f70_mean, D1R_m70_count, D1R_f70_count)

D1R_male_female_ratios = pd.concat([D1R_P17_M_F_ratio, D1R_P25_M_F_ratio, D1R_P35_M_F_ratio, D1R_P49_M_F_ratio, D1R_P70_M_F_ratio], axis = 1)
D1R_male_female_ratios.columns = [ages]

D1R_mean_values = D1R_grouped_means.transpose()

# hierarchical regions level
    
D1R_hier_P17_M_F_ratio = ngf.calculate_ratio(D1R_hier_m17_mean, D1R_hier_f17_mean, D1R_hier_m17_count, D1R_hier_f17_count)
D1R_hier_P25_M_F_ratio = ngf.calculate_ratio(D1R_hier_m25_mean, D1R_hier_f25_mean, D1R_hier_m25_count, D1R_hier_f25_count)
D1R_hier_P35_M_F_ratio = ngf.calculate_ratio(D1R_hier_m35_mean, D1R_hier_f35_mean, D1R_hier_m35_count, D1R_hier_f35_count)
D1R_hier_P49_M_F_ratio = ngf.calculate_ratio(D1R_hier_m49_mean, D1R_hier_f49_mean, D1R_hier_m49_count, D1R_hier_f49_count)
D1R_hier_P70_M_F_ratio = ngf.calculate_ratio(D1R_hier_m70_mean, D1R_hier_f70_mean, D1R_hier_m70_count, D1R_hier_f70_count)

D1R_hier_male_female_ratios = pd.concat([D1R_hier_P17_M_F_ratio, D1R_hier_P25_M_F_ratio, D1R_hier_P35_M_F_ratio, D1R_hier_P49_M_F_ratio, D1R_hier_P70_M_F_ratio], axis = 1)
D1R_hier_male_female_ratios.columns = [ages]

D1R_hier_mean_values = D1R_hier_grouped_means.transpose()



### MALE / FEMALE RATIO FOR D2R (not used in paper)

D2R_P17_M_F_ratio = ngf.calculate_ratio(D2R_m17_mean, D2R_f17_mean, D2R_m17_count, D2R_f17_count)
D2R_P25_M_F_ratio = ngf.calculate_ratio(D2R_m25_mean, D2R_f25_mean, D2R_m25_count, D2R_f25_count)
D2R_P35_M_F_ratio = ngf.calculate_ratio(D2R_m35_mean, D2R_f35_mean, D2R_m35_count, D2R_f35_count)
D2R_P49_M_F_ratio = ngf.calculate_ratio(D2R_m49_mean, D2R_f49_mean, D2R_m49_count, D2R_f49_count)
D2R_P70_M_F_ratio = ngf.calculate_ratio(D2R_m70_mean, D2R_f70_mean, D2R_m70_count, D2R_f70_count)

D2R_male_female_ratios = pd.concat([D2R_P17_M_F_ratio, D2R_P25_M_F_ratio, D2R_P35_M_F_ratio, D2R_P49_M_F_ratio, D2R_P70_M_F_ratio], axis = 1)
D2R_male_female_ratios.columns = [ages]

D2R_mean_values = D2R_grouped_means.transpose()


# hierarchical regions level

D2R_hier_P17_M_F_ratio = ngf.calculate_ratio(D2R_hier_m17_mean, D2R_hier_f17_mean, D2R_hier_m17_count, D2R_hier_f17_count)
D2R_hier_P25_M_F_ratio = ngf.calculate_ratio(D2R_hier_m25_mean, D2R_hier_f25_mean, D2R_hier_m25_count, D2R_hier_f25_count)
D2R_hier_P35_M_F_ratio = ngf.calculate_ratio(D2R_hier_m35_mean, D2R_hier_f35_mean, D2R_hier_m35_count, D2R_hier_f35_count)
D2R_hier_P49_M_F_ratio = ngf.calculate_ratio(D2R_hier_m49_mean, D2R_hier_f49_mean, D2R_hier_m49_count, D2R_hier_f49_count)
D2R_hier_P70_M_F_ratio = ngf.calculate_ratio(D2R_hier_m70_mean, D2R_hier_f70_mean, D2R_hier_m70_count, D2R_hier_f70_count)

D2R_hier_male_female_ratios = pd.concat([D2R_hier_P17_M_F_ratio, D2R_hier_P25_M_F_ratio, D2R_hier_P35_M_F_ratio, D2R_hier_P49_M_F_ratio, D2R_hier_P70_M_F_ratio], axis = 1)
D2R_hier_male_female_ratios.columns = [ages]

D2R_hier_mean_values = D2R_hier_grouped_means.transpose()


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











