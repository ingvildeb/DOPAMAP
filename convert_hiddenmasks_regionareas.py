# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:00:42 2022

@author: ingvieb
"""

import pandas as pd
import numpy as np
import glob
import os

commonpath = r'Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P70\*\00_nonlin_registration_files/'
allpaths = glob.glob(commonpath)
#allfiles = glob.glob(commonpath + "*_statistics.xlsx")

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'

# path = r"Y:\Dopamine_receptors\Analysis\QUINT_analysis\D1R\P70\D1R_P70_M_C22\00_nonlin_registration_files//"
# file = path + "C22_nonlinear_summary_statistics.xlsx"
resourcepath = r"Y:\Dopamine_receptors\Analysis\resources//" 

customregions = r"Y:\Dopamine_receptors\Analysis\resources//" + "CustomRegions_Allen2017_DOPAMAP.xlsx"

customregions = pd.read_excel(customregions, usecols="B:GY")
customregions = customregions[2:]
customregions = pd.DataFrame(customregions)

regionnames = pd.read_csv(customregsfile, sep=';', usecols =['Region name'])
regionnames = regionnames.values
regionnames = np.insert(regionnames, 0, 'Sections', axis=None)

# convert custom regions into a dataframe with column for id and customregion name

df = pd.DataFrame()

for column in customregions:

    selection = customregions[column]
    selection = pd.DataFrame(selection)
    selection = selection.dropna()
    value = str(selection.columns)
    value = value[8:-19]
    selection.insert(1, "custom region", value)
    selection.columns = ["region ID", "custom region"]
    #print(selection)
    df = pd.concat((df,selection))
    
    
writer = pd.ExcelWriter(resourcepath + "ID_to_custom" + '.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='ID_to_custom', index=False)
writer.save()

# convert the dataframe for custom regions into a dictionary with region ID as the key, used to map ids to names later

mydict = df.set_index('region ID')['custom region'].to_dict()

selectionpaths = allpaths[1:4]
#selection_files = allfiles[1:4]

# ids = []

# for f in allpaths:
#     f = f.split("_n")[0]
#     f = f.split("_")[5]
#     f = f.split("\\")[0]
#     ids.append(f)

    

for path in allpaths:
    
    f = path.split("_n")[0]
    f = f.split("_")[5]
    f = f.split("\\")[0]
    ID = f
    

    
    #file = glob.glob(path + '*_statistics.xlsx')
    file = path + '/' + ID + '_nonlinear_summary_statistics.xlsx'
    
    if not os.path.exists(file):
        print(f"{file} does not exist!")
        continue 
   
    
    #get names of worksheets in excel file 
    
    sheetnames = pd.read_excel(file, sheet_name=None)
    
    mylist = []
    
    for name in sheetnames:
        name = name.lower()
        name = name.split(sep="_s")[1]
        name = name.split(sep=".")[0]
        name = int(name)
        mylist.append(name)
    
    # loop through sheetnames and make them into dataframes compatible with the format used later
    
    region_pixels_df = pd.DataFrame()
    
    for name in sheetnames:
        read = pd.read_excel(file, usecols=["Region ID", "pix whole section"], sheet_name=name)
        region_pixels = pd.DataFrame(read)
    #    print(t, read)
        
            
        region_pixels['Custom Region'] = region_pixels['Region ID'].map(mydict)
        region_pixels_summary = (region_pixels.groupby('Custom Region')["pix whole section"].sum())
        region_pixels_summary = pd.DataFrame(region_pixels_summary)
        region_pixels_summary = region_pixels_summary.reset_index('Custom Region')
        # region_pixels_summary = region_pixels_summary[['Custom Region', 'mean']]
        
        
        
        ### ENSURE ALL REGIONS ARE IN DATAFRAME AND SORTED CORRECTLY
        
        added_regions = []
        
        for region in regionnames[1:]:
            if region not in region_pixels_summary['Custom Region'].values:
                added_regions.append(region)
            
        ## make a new dataframe from regions list 
        nonincluded_regions = pd.DataFrame(added_regions, columns=['Custom Region'])
        
        ## then add regions to the DataFrame of object mean sizes with empty value for mean
        region_pixels_summary2 = pd.concat([region_pixels_summary, nonincluded_regions])
        
        #now all the regions are included in the dataframe but they are not sorted in the same way as the other nutil reports.
        
        #create a mapping column based on the sorting in the reports containing counts and masks (hierarchical sorting according to CCF) for custom sorting of regions:
        df_mapping = pd.DataFrame({'Custom Region': regionnames})
        sort_mapping = df_mapping.reset_index().set_index('Custom Region')
        
        #apply sorting to dataframe with object mean sizes:
        region_pixels_summary2['Sorted Regions'] = region_pixels_summary2['Custom Region'].map(sort_mapping['index'])
        region_pixels_summary2 = region_pixels_summary2.sort_values('Sorted Regions')
        
        region_pixels_summary2 = region_pixels_summary2[['Custom Region', 'pix whole section']]
        region_pixels_summary2_transposed = region_pixels_summary2.transpose()
        region_pixels_summary2_transposed = region_pixels_summary2_transposed[1:]
        region_pixels_summary2_transposed.columns = regionnames[1:]
    
    
        #print(hidden_masks_summary2_transposed)
        
        region_pixels_df = pd.concat((region_pixels_df, region_pixels_summary2_transposed))
        
    region_pixels_df = region_pixels_df.reset_index(drop=True)
    region_pixels_df.insert(0, "Section number", mylist, True)
    
    
       
        
    writer = pd.ExcelWriter(path + ID + "_region_pixels" + '.xlsx', engine='xlsxwriter')
    region_pixels_df.to_excel(writer, sheet_name='region_pixels', index=False)
    writer.save()
    
    print(ID, " finished successfully")
    
    break
    