# DOPAMAP


This repository contains all the code used for the DOPAMAP project (Bjerke et al., manuscript in preparation). All data needed to re-use these scripts are shared via the EBRAINS Knowledge Graph.



**The following scripts are included:**

- ***compile_segmentations:*** Used to combine results from the three ilastik segmentation algorithms used, depending on region of interest, and overlaying the combined segmentations with damage masks that cover and effectively excluded damaged regions from the nutil analysis.

- ***DOPAMAP_create_nut_quant_files:*** Used to batch create nutil quantifier files. The functions used for this can be found in the [nutil scripts repository](https://github.com/ingvildeb/nutil_scripts).

- ***atlas_slicing_GPU:*** Used to generate perfect slices through the planes as defined by the JSON anchoring file of a brain, upon which the difference in region sizes in the "perfect" slice and the "real" slice is calculated. The "real" slice might have parts of regions in the atlas missing (if they were missing from the brain section, the cropping of the images makes it so that parts of the atlas falls outside the image). This script is used to calculate how much of a region is missing from the atlas overlay used for analysis, so that they can be added to the masks and accounted for in further analysis (such missing parts are referred to as "hidden masks" in further scripts).

- ***convert_hidden_masks:*** Used to calculate the hidden mask load for each custom region based on the output files from the atlas_slicing_GPU script, and converting to a format that is compatible with further processing of nutil data in the DOPAMAP_nut_postprocessing script.

- ***DOPAMAP_nut_postprocessing:*** Used to postprocess nutil data (compiling sectionwise data, correcting for damaged areas, calculating 3D densities, interpolating missing sections ...) The functions used for this can be found in the [nutil scripts repository](https://github.com/ingvildeb/nutil_scripts).

- ***DOPAMAP_make_calculations:*** Used to remove outlier values and calculate average densities per animal; calculate total number estimates in cases of whole-region coverage; and compile density, total number, and cell size information per animal into a single sheet per receptor type.

- ***DOPAMAP_descriptive_data_and_ratios:*** Used to create descriptive data files and D1:D2 ratios across sex and age groups. The functions used for this can be found in the [nutil scripts repository](https://github.com/ingvildeb/nutil_scripts).

- ***DOPAMAP_graphing:*** Used to graph data for figures. The functions used for this can be found in the [nutil scripts repository](https://github.com/ingvildeb/nutil_scripts).


