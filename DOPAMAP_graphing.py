# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 12:03:06 2023

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

D1R_densities_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_hierarchical_densities.xlsx"
D1R_totals_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_hierarchical_totals.xlsx"
D1R_cell_sizes_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D1R_hierarchical_cell_sizes.xlsx"

D1R_densities_hier = (pd.read_excel(D1R_densities_hier_path)).iloc[0:, 1:]
D1R_totals_hier = (pd.read_excel(D1R_totals_hier_path)).iloc[0:, 1:]
D1R_cell_sizes_hier = (pd.read_excel(D1R_cell_sizes_hier_path)).iloc[0:, 1:]



D2R_densities_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_densities.xlsx"
D2R_totals_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_total_numbers.xlsx"
D2R_cell_sizes_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_cell_pixels.xlsx"


D2R_densities = pd.read_excel(D2R_densities_path)
D2R_densities["Area prostriata"] = np.nan
D2R_totals = pd.read_excel(D2R_totals_path)
D2R_cell_sizes = pd.read_excel(D2R_cell_sizes_path)


D2R_densities_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_hierarchical_densities.xlsx"
D2R_totals_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_hierarchical_totals.xlsx"
D2R_cell_sizes_hier_path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\Derived_data\Numbers\D2R_hierarchical_cell_sizes.xlsx"

D2R_densities_hier = (pd.read_excel(D2R_densities_hier_path)).iloc[0:, 1:]
D2R_totals_hier = (pd.read_excel(D2R_totals_hier_path)).iloc[0:, 1:]
D2R_cell_sizes_hier = (pd.read_excel(D2R_cell_sizes_hier_path)).iloc[0:, 1:]



## Get custom region names from excel file:

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'
read_customregs = pd.read_csv(customregsfile, sep = ";")


## list regions at various levels of hierarchy
hierarchy_regs = (read_customregs['Hierarchy'].unique()).tolist()
major_regs = (read_customregs['Hierarchy_major'].unique()).tolist()
medium_hier_regs = (read_customregs['Hierarchy_medium'].unique()).tolist()


regions_to_hierarchy_dict = dict(zip(read_customregs['Region name'], read_customregs['Hierarchy']))

## Get counts and mean values per age group

D1R_count = (D1R_densities.groupby("age").count()).iloc[0:,2:]
D2R_count = (D2R_densities.groupby("age").count()).iloc[0:,2:]

D1R_densities_mean = D1R_densities.groupby("age").mean()
D2R_densities_mean = D2R_densities.groupby("age").mean()    

D1R_cell_sizes_mean = D1R_cell_sizes.groupby("age").mean()
D2R_cell_sizes_mean = D2R_cell_sizes.groupby("age").mean()   

D1R_totals_mean = D1R_totals.groupby("age").mean()
D2R_totals_mean = D2R_totals.groupby("age").mean() 

D1R_densities_hier_mean = D1R_densities_hier.groupby("age").mean()
D2R_densities_hier_mean = D2R_densities_hier.groupby("age").mean()



def unique_list(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


######### SETTING UP SELECTED DATA

included_regions = ["Motor areas", "Somatosensory areas", "Gustatory and visceral areas", "Anterior cingulate areas", "Prefrontal areas", "Retrosplenial areas", "Olfactory areas", "Hippocampal region",
                    "Cortical subplate", "Striatum", "Striatum-like amygdalar areas", "Pallidum", "Thalamus, sensory-motor cortex related", "Thalamus, polymodal association cortex related", "Hypothalamus, other",
                    "Hypothalamic medial zone", "Hypothalamic lateral zone"]
included_columns = ["ID", "age", "sex", *included_regions]


## define outliers

outliers_D1R = {
    "C19": ["Motor areas"], 
    "E15": ["Somatosensory areas"], 
    "C68": ["Prefrontal areas"],
    "C53": ["Prefrontal areas"], 
    "C108": ["Retrosplenial areas"], 
    "D13": ["Thalamus, sensory-motor cortex related"],
    "E62": ["Thalamus, sensory-motor cortex related", "Thalamus, polymodal association cortex related", "Hypothalamic medial zone"],
    "C45": ["Striatum-like amygdalar areas", "Hypothalamic medial zone"],
    "C17": ["Hippocampal region", "Hypothalamic medial zone"]
    }

outliers_D2R = {
    "D166": ["Motor areas"],
    "D235": ["Gustatory and visceral areas"],
    "D123": ["Anterior cingulate areas"],
    "D143": ["Olfactory areas"],
    "D157": ["Pallidum"],
    "D197": ["Hypothalamic medial zone", "Hypothalamic lateral zone"],
    "D146": ["Hypothalamic medial zone", "Hypothalamic lateral zone"]
    }

## remove outliers from selected data
selected_D1_data = D1R_densities_hier[included_columns]
selected_D1_data = selected_D1_data.set_index("ID")

selected_D2_data = D2R_densities_hier[included_columns]
selected_D2_data = selected_D2_data.set_index("ID")

outlier_dicts = [outliers_D1R, outliers_D2R]
dfs = [selected_D1_data, selected_D2_data]


for outlier_dict, df in zip(outlier_dicts, dfs):
        
    for key in outlier_dict:
        excluded_regions = outlier_dict.get(key)
    
        for region in excluded_regions:
            df.loc[key, region] = np.nan
        
        
selected_D1_data = selected_D1_data.reset_index()
selected_D2_data = selected_D2_data.reset_index()

## get means for each age group and sex

grouped_D1_data = selected_D1_data.groupby(["age", "sex"]).mean()
grouped_D2_data = selected_D2_data.groupby(["age", "sex"]).mean()

ages = ["P17", "P25", "P35", "P49", "P70"]

D1R_hier_m17_mean, D1R_hier_m25_mean, D1R_hier_m35_mean, D1R_hier_m49_mean, D1R_hier_m70_mean = ((grouped_D1_data.loc[age, "M"]) for age in ages)
D1_male_df = pd.DataFrame([D1R_hier_m17_mean, D1R_hier_m25_mean, D1R_hier_m35_mean, D1R_hier_m49_mean, D1R_hier_m70_mean])

D1R_hier_f17_mean, D1R_hier_f25_mean, D1R_hier_f35_mean, D1R_hier_f49_mean, D1R_hier_f70_mean = ((grouped_D1_data.loc[age, "F"]) for age in ages)
D1_female_df = pd.DataFrame([D1R_hier_f17_mean, D1R_hier_f25_mean, D1R_hier_f35_mean, D1R_hier_f49_mean, D1R_hier_f70_mean])

D2R_hier_m17_mean, D2R_hier_m25_mean, D2R_hier_m35_mean, D2R_hier_m49_mean, D2R_hier_m70_mean = ((grouped_D2_data.loc[age, "M"]) for age in ages)
D2_male_df = pd.DataFrame([D2R_hier_m17_mean, D2R_hier_m25_mean, D2R_hier_m35_mean, D2R_hier_m49_mean, D2R_hier_m70_mean])

D2R_hier_f17_mean, D2R_hier_f25_mean, D2R_hier_f35_mean, D2R_hier_f49_mean, D2R_hier_f70_mean = ((grouped_D2_data.loc[age, "F"]) for age in ages)
D2_female_df = pd.DataFrame([D2R_hier_f17_mean, D2R_hier_f25_mean, D2R_hier_f35_mean, D2R_hier_f49_mean, D2R_hier_f70_mean])




grouped_D1_sem = selected_D1_data.groupby(["age", "sex"]).sem()
grouped_D2_sem = selected_D2_data.groupby(["age", "sex"]).sem()

D1R_hier_m17_sem, D1R_hier_m25_sem, D1R_hier_m35_sem, D1R_hier_m49_sem, D1R_hier_m70_sem = ((grouped_D1_sem.loc[age, "M"]) for age in ages)
D1_male_sem_df = pd.DataFrame([D1R_hier_m17_sem, D1R_hier_m25_sem, D1R_hier_m35_sem, D1R_hier_m49_sem, D1R_hier_m70_sem])

D1R_hier_f17_sem, D1R_hier_f25_sem, D1R_hier_f35_sem, D1R_hier_f49_sem, D1R_hier_f70_sem = ((grouped_D1_sem.loc[age, "F"]) for age in ages)
D1_female_sem_df = pd.DataFrame([D1R_hier_f17_sem, D1R_hier_f25_sem, D1R_hier_f35_sem, D1R_hier_f49_sem, D1R_hier_f70_sem])


D2R_hier_m17_sem, D2R_hier_m25_sem, D2R_hier_m35_sem, D2R_hier_m49_sem, D2R_hier_m70_sem = ((grouped_D2_sem.loc[age, "M"]) for age in ages)
D2_male_sem_df = pd.DataFrame([D2R_hier_m17_sem, D2R_hier_m25_sem, D2R_hier_m35_sem, D2R_hier_m49_sem, D2R_hier_m70_sem])

D2R_hier_f17_sem, D2R_hier_f25_sem, D2R_hier_f35_sem, D2R_hier_f49_sem, D2R_hier_f70_sem = ((grouped_D2_sem.loc[age, "F"]) for age in ages)
D2_female_sem_df = pd.DataFrame([D2R_hier_f17_sem, D2R_hier_f25_sem, D2R_hier_f35_sem, D2R_hier_f49_sem, D2R_hier_f70_sem])



############ GRAPHING

import nutil_scripts.graphing_functions as grf
from matplotlib.pyplot import figure  
from mpl_toolkits.mplot3d import Axes3D

# GRAPHING SELECTED REGIONS



plt.figure(figsize=(17, 25))

for n, region in enumerate(included_regions):
    # add a new subplot iteratively
    ax = plt.subplot(6, 3, n + 1)


    plt.errorbar(ages, D1_female_df[region].values, label = "D1R female", marker='s', linewidth = 2.5, ls = '-', c = '#dc582a', yerr = D1_female_sem_df[region].values, elinewidth = 1)
    plt.errorbar(ages, D1_male_df[region].values, label = "D1R male", marker='s', linewidth = 2.5, ls = '-', c = '#003b49', yerr = D1_male_sem_df[region].values, elinewidth = 1)
    plt.errorbar(ages, D2_female_df[region].values, label = "D2R female", marker='o', linewidth = 2.5, ls = '--', c = '#dc582a', yerr = D2_female_sem_df[region].values, elinewidth = 1)
    plt.errorbar(ages, D2_male_df[region].values, label = "D2R male", marker='o', linewidth = 2.5, ls = '--', c = '#003b49', yerr = D2_male_sem_df[region].values, elinewidth = 1)
    
   
    # chart formatting
    ax.set_title(region.upper())


ax.legend()
    
plt.savefig("allgraphs.svg")
plt.show()





#matplotlib.rcParams.update({'font.size': 22})

color_list = grf.set_region_colors(customregsfile)
color_list_hier = grf.set_region_colors(customregsfile, R_col = "R_hier", G_col = "G_hier", B_col = "B_hier")
color_list_hier = unique_list(color_list_hier)
ls_list_hier = ['-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':','--', '-.', '-', ':']
region_list = grf.set_region_names(customregsfile)    



#### CREATE LINE PLOTS FOR HIGHER HIERARCHICAL REGIONS

### D1R

import mpld3
from mpld3 import plugins
from mpld3.utils import get_id
import numpy as np
import collections
import matplotlib.pyplot as plt




fig = plt.figure(figsize = (25,25), dpi=80)

ax1 = fig.add_subplot(2,1,1)

l1 = []
columns = []
for column, color, lstyle in zip(D1R_densities_hier_mean, color_list_hier, ls_list_hier):
    data = D1R_densities_hier_mean[column] 
    l1.append(ax1.plot(data, c = color, linewidth = 2.5, ls = lstyle))
    columns.append(column)
    
ax1.set_ylim(0, 25000)
#ax1.rc('font', size=28)
#plt.legend(loc=(1.04, 0))
plugins.connect(fig, plugins.InteractiveLegendPlugin(l1, columns, ax=ax1,  start_visible=False))
mpld3.save_html(fig, 'bigtest.html')
# plt.savefig('D1R_devplot_wholebrain.svg', bbox_inches='tight')    
# plt.show()    
    
    
### D2R


figure(figsize = (30,30), dpi=80)

for column, color, lstyle in zip(D2R_densities_hier_mean, color_list_hier, ls_list_hier):
    data = D2R_densities_hier_mean[column] 
    plt.plot(data, c = color, label = column, linewidth = 2.5, ls = lstyle)
    
plt.ylim(0, 25000)
plt.rc('font', size=40)
plt.legend(loc=(1.04, 0))
plt.savefig('D2R_devplot_wholebrain.svg', bbox_inches='tight')    
plt.show()    




## function to create a dict of maximum values for regions within a hierarchical level
#  get_regs_from_sr = lambda e:  (read_customregs[(read_customregs[superregions_col] == e)])[regions_col].tolist()


def create_maxval_dict(customregsfile, superregions_col, regions_col, datafiles):
    maxval_list = []
    read_customregs = pd.read_csv(customregsfile, sep = ";")  
    superregion_list = ((read_customregs[superregions_col]).unique()).tolist()
    print(superregion_list)

    
    data = pd.concat(datafiles)
    for sreg in superregion_list:       
        regs_in_superreg = (read_customregs[(read_customregs[superregions_col] == sreg)])[regions_col].tolist()
        flat_list = np.array([data[region].values for region in regs_in_superreg])
        flat_list[np.isnan(flat_list)] = 0        
        maxval = flat_list.max()

        
        maxval_list.append(maxval)
        maxval_dict = dict(zip(superregion_list, maxval_list))
    return(maxval_dict)
    

    
maxval_dict_major_hier = create_maxval_dict(customregsfile, "Hierarchy_major", "Region name", [D1R_densities_mean, D2R_densities_mean])
maxval_dict_medium_hier = create_maxval_dict(customregsfile, "Hierarchy", "Region name", [D1R_densities_mean, D2R_densities_mean])




## function to create line graphs per hierarchical level




def create_line_graphs_per_hierarchy_level(customregsfile, superregions_col, regions_col, maxval_dict, datafile, plot_prefix = ""):
    
    read_customregs = pd.read_csv(customregsfile, sep = ";")  
    superregion_list = ((read_customregs[superregions_col]).unique()).tolist()    
    
    for sreg in superregion_list:
        figure(figsize = (20,10), dpi=80)
    
        regs_in_superreg = ((read_customregs[(read_customregs[superregions_col] == sreg)])[regions_col]).tolist()
        regs_in_superreg = unique_list(regs_in_superreg)
                
        ylim = maxval_dict.get(sreg)
   
        for region in regs_in_superreg:            
            data = datafile[region]
            plt.plot(data, label = region)
        
        plt.ylim(0, (ylim + 1000))
        plt.rc('font', size=10)
        plt.legend()
        plt.savefig(plot_prefix + str(sreg) + '.svg', bbox_inches='tight')    
        plt.show()

##### CREATE LINE PLOTS WITH FINE REGIONS ORGANIZED PER MEDIUM LEVEL HIERARCHICAL REGION

create_line_graphs_per_hierarchy_level(customregsfile, "Hierarchy", "Region name", maxval_dict_medium_hier, D1R_densities_mean, "D1R_devplot_")
create_line_graphs_per_hierarchy_level(customregsfile, "Hierarchy", "Region name", maxval_dict_medium_hier, D2R_densities_mean, "D2R_devplot_")
    
    
##### CREATE LINE PLOTS WITH MEDIUM LEVEL REGIONS ORGANIZED PER MAJOR HIERARCHICAL REGION


create_line_graphs_per_hierarchy_level(customregsfile, "Hierarchy_major", "Hierarchy", maxval_dict_major_hier, D1R_densities_hier_mean, "D1R_devplot_hier_")
create_line_graphs_per_hierarchy_level(customregsfile, "Hierarchy_major", "Hierarchy", maxval_dict_major_hier, D1R_densities_hier_mean, "D2R_devplot_hier_")



##### CREATE BAR PLOTS PER AGE

    


# create plots for D1R densities

D1R_P70_densities_mean = D1R_densities_mean.loc["P70",:]
D1R_P49_densities_mean = D1R_densities_mean.loc["P49",:]
D1R_P35_densities_mean = D1R_densities_mean.loc["P35",:]
D1R_P25_densities_mean = D1R_densities_mean.loc["P25",:]
D1R_P17_densities_mean = D1R_densities_mean.loc["P17",:]

grf.create_allen_bar_graph("D1R_P70", input_dir = D1R_P70_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D1R_P49", input_dir = D1R_P49_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D1R_P35", input_dir = D1R_P35_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D1R_P25", input_dir = D1R_P25_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D1R_P17", input_dir = D1R_P17_densities_mean, color_list = color_list, region_list = region_list)

grf.create_allen_hbar_graph("D1R_P70", input_dir = D1R_P70_densities_mean, color_list = color_list, region_list = region_list)


# create plots for D2R densities
            
D2R_P70_densities_mean = D2R_densities_mean.loc["P70",:]
D2R_P49_densities_mean = D2R_densities_mean.loc["P49",:]
D2R_P35_densities_mean = D2R_densities_mean.loc["P35",:]
D2R_P25_densities_mean = D2R_densities_mean.loc["P25",:]
D2R_P17_densities_mean = D2R_densities_mean.loc["P17",:]

grf.create_allen_bar_graph("D2R_P70", input_dir = D2R_P70_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D2R_P49", input_dir = D2R_P49_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D2R_P35", input_dir = D2R_P35_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D2R_P25", input_dir = D2R_P25_densities_mean, color_list = color_list, region_list = region_list)
grf.create_allen_bar_graph("D2R_P17", input_dir = D2R_P17_densities_mean, color_list = color_list, region_list = region_list)
    
grf.create_allen_hbar_graph("D2R_P70", input_dir = D2R_P70_densities_mean, color_list = color_list, region_list = region_list)




# create plots for D1R totals

D1R_P70_totals_mean = D1R_totals_mean.loc["P70",:]
grf.create_allen_hbar_graph("D1R_P70", input_dir = D1R_P70_totals_mean, color_list = color_list, region_list = region_list)










































