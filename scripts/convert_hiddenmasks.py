# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 11:00:42 2022

@author: ingvieb
"""

import pandas as pd
import numpy as np
import glob
import os


# must be run for each age group separately, and make sure customregions point to the right file depending on the atlas used

commonpath = r'Y:\Dopamine_receptors\Analysis\QUINT_analysis\D*R\P17\*\00_nonlin_registration_files/'
allpaths = glob.glob(commonpath)

resourcedir = 'Y:/Dopamine_receptors/Analysis/resources//'
customregsfile = resourcedir + 'customregions.csv'


resourcepath = r"Y:\Dopamine_receptors\Analysis\resources//" 

customregions = r"Y:\Dopamine_receptors\Analysis\resources//" + "CustomRegions_Allen2017_Newmaster.xlsx"

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
    df = pd.concat((df,selection))
    
    
writer = pd.ExcelWriter(resourcepath + "ID_to_custom" + '.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='ID_to_custom', index=False)
writer.save()

# convert the dataframe for custom regions into a dictionary with region ID as the key, used to map ids to names later

mydict = df.set_index('region ID')['custom region'].to_dict()

   

for path in allpaths:
    
    f = path.split("_n")[0]
    f = f.split("_")[5]
    f = f.split("\\")[0]
    ID = f
    

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
    
    hidden_masks_df = pd.DataFrame()
    
    for name in sheetnames:
        read = pd.read_excel(file, usecols=["Region ID", "percent absent", "pix whole section", "pix cropped section"], sheet_name=name)
        hidden_masks = pd.DataFrame(read)


        hidden_masks['Custom Region'] = hidden_masks['Region ID'].map(mydict)
        pix_whole_sum = (hidden_masks.groupby('Custom Region')['pix whole section'].sum())
        pix_cropped_sum = (hidden_masks.groupby('Custom Region')['pix cropped section'].sum())
        hidden_masks_summary = 1 - (pix_cropped_sum / pix_whole_sum)
        
        hidden_masks_summary = hidden_masks_summary.reset_index('Custom Region')
        hidden_masks_summary = hidden_masks_summary.rename(columns={'Custom Region': 'Custom Region', 0: 'sum absent proportion'})
        hidden_masks_summary = hidden_masks_summary[['Custom Region','sum absent proportion']]
        
        
        
        ### ENSURE ALL REGIONS ARE IN DATAFRAME AND SORTED CORRECTLY
        
        added_regions = []
        
        for region in regionnames[1:]:
            if region not in hidden_masks_summary['Custom Region'].values:
                added_regions.append(region)
            
        ## make a new dataframe from regions list 
        nonincluded_regions = pd.DataFrame(added_regions, columns=['Custom Region'])
        
        ## then add regions to the DataFrame of object mean sizes with empty value for mean
        hidden_masks_summary2 = pd.concat([hidden_masks_summary, nonincluded_regions])
        
        #now all the regions are included in the dataframe but they are not sorted in the same way as the other nutil reports.
        
        #create a mapping column based on the sorting in the reports containing counts and masks (hierarchical sorting according to CCF) for custom sorting of regions:
        df_mapping = pd.DataFrame({'Custom Region': regionnames})
        sort_mapping = df_mapping.reset_index().set_index('Custom Region')
        
        #apply sorting to dataframe with object mean sizes:
        hidden_masks_summary2['Sorted Regions'] = hidden_masks_summary2['Custom Region'].map(sort_mapping['index'])
        hidden_masks_summary2 = hidden_masks_summary2.sort_values('Sorted Regions')
        
        hidden_masks_summary2 = hidden_masks_summary2[['Custom Region', 'sum absent proportion']]
        hidden_masks_summary2_transposed = hidden_masks_summary2.transpose()
        hidden_masks_summary2_transposed = hidden_masks_summary2_transposed[1:]
        hidden_masks_summary2_transposed.columns = regionnames[1:]

        
        hidden_masks_df = pd.concat((hidden_masks_df, hidden_masks_summary2_transposed))
        
    hidden_masks_df = hidden_masks_df.reset_index(drop=True)
    hidden_masks_df.insert(0, "Section number", mylist, True)
    
    
       
        
    writer = pd.ExcelWriter(path + ID + "_hidden_mask_loads" + '.xlsx', engine='xlsxwriter')
    hidden_masks_df.to_excel(writer, sheet_name='hidden_mask_loads', index=False)
    writer.save()
    
    print(ID, " finished successfully")
    

    
    