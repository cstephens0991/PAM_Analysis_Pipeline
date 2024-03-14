---
title: "PAM Analysis Pipeline"
author: "Chris Stephens & Sinaeda Anderssen"
date: "2023-02-13"
---

This document will guide you through the pipeline built for the semi-automated extraction of pulse amplitude modulation (PAM) fluorometry data from images generated using the PAM fluorometer:

- Using the Python script *get_fvfm.py* to extract FvFm data from .xpim files generated using the ImagingWin software.      
- Using the ImageJ macro *get_plant_area.txt* to extract plant area data from "contrast" TIF images.        
- Note: separate **options** in these scripts exist for the "**black plates**" cell culture plates which do not result in internal reflection which may affect photosynthetic area quantification.

## Extract photosynthetic efficiency (Y(II)) data from PIM files
### 1. Load the get_fvfm micromamba environment
If you have not done so already (following protocol above), open Gitbash and activate the "get_fvfm" environment:
```bash
micromamba activate get_fvfm
```
If you are unsure what the name of the environment is (in case you didn't use the default name), you can list all environments using `micromamba env list`.

### 2. Usage of get_fvfm.py
Current version is `get_fvfm_v3.py`. 

Check you are in the right directory : `PAM_Analysis_Pipeline/pam_package`. 

```bash
## change directory (cd)
cd pam_package
## list the files that are there (ls)
ls -lrth
```

Notice the `input/` folder. We will put the input files there (xpim files), during step 3. 

To run the "get_fvfm_v3.py" script, enter the following command into `Git Bash`:
```bash
## might take 15-30 seconds
python get_fvfm_v3.py --help
```
This will give you all the available options to the script. Here's a run-through of the available options:

- `--exp-id`: Experiment ID that will be integrated in the folder names. 
- `--xpim-dir`: the directory/folder containing the \*.xpim files. The default is `./runs/input/xpim_files/`. *I do recommend changing this, and using a custom directory, with an experiment identifier.*           
<!-- - `--tif-dir`: the directory/folder containing the \*.tif files. The default is `./runs/input/tif_files/`. *I do recommend changing this, and using a custom directory, with the same experiment identifier as with the \*.xpim files.*           -->
<!-- - `--outpath`: the output directory which will contain results of current run. The default is './runs/fvfm_<TIMESTAMP>'. Using the default will add a timestand to the output folder name. This way, if you run the script several times in a row on the same dataset, it will NOT overwrite the results of previous runs. You can also use a custom name, with an experiment ID (as explained above), but if you run it several times, remember to change the `--outpath` name if you want to keep the results.            -->
- `--well-coord`: CSV file containing the well coordinates. The columns should be the Well names (well_1, well_2 etc), and the rows contain the coordinates (x1,y1,x2,y2). If format is imagej, specify in coord_format option. [default = './input/24_wells_transposed.csv']           
- `--coord-format`: Format of well coordinates. ImageJ sees Well coordinates as: [100, 130, 70, 70] , corresponding to [x_start, y_start, x_width, y_width]. PlantCV sees Well coordinates as: [100, 130, 170, 200], corresponding to [x_start, y_start, x_end, y_end]. By default, it will try to detect the format ('auto'), but can be set to 'plantcv' or 'imagej' (case-sensitive). [default = 'auto']         
- `--threshold`: Threshold to define plant material from background. Default is Yen's threshold, as defined by Yen et al 1995 (10.1109/83.366472). [default = 'yen']        

### 2bis. Folder naming conventions
Inside `pam_package` there is by default an "input" folder. By default, `get_fvfm` will look inside input/xpim_files/ for the .xpim files. This folder is pre-populated with a single .xpim file, if you want to run the script as a test first.        
However, I don't recommend copying your .xpim files inside this pre-made folder. Instead, to organise your files, use experiment IDs: create a folder inside `runs/input` with your experiment ID, for your xpim files. For example, if your experiment is `Exp102`, then you could copy your xpim files here: 

```
runs/input/exp102_xpim
```

Basically, use your experiment ID as a common identifier, that will link all your input and output files together. This experiment ID is the first argument for the script (and is **required**), and using that the script will create the tif folder, as well as the output folder, with custom names:

```
runs/input/<exp_id>_tif
runs/<exp_id>_fvfm_<timestamp>
```

Here is an example run, that takes this into account:

```bash
python get_fvfm_v3.py --exp-id exp102 --xpim-dir ./runs/input/exp102_xpim --well-coord ./plate_formats/24_wells_transposed.csv --coord-format auto --threshold 40
```

The only necessary folder to start the script is therefore the one containing the xpim files, which doesn't exist yet. You can create it very simply like this:

```bash
## replace "<experiment_id>" with the actual experiment ID
mkdir runs/input/<exp_id>_xpim/
```

Check if it was made:

```bash
## check it was made:
ls runs/input/
```

To copy the xpim files, you can either do it in the Windows File Explorer, or if you want to stay inside Git Bash, and you know where your files are, you can run this command:

```bash
## copy files (cp)
cp <path/to/your/xpim>/*.xpim runs/input/<exp_id>_xpim/
# replace the <path/to/your/xpim> with the path that leads to your xpim files. *.xpim will then find all files that end with .xpim
# replace <experiment_id> with the actual folder name you created

## check it worked:
ls runs/input/<exp_id>_xpim/
```

You should see a list of your xpim files. 

### 3. Note on well coordinates 

The files for the 24-well plate coordinates are available in the `plate_formats` folder. 

The default well coordinates were measured by Chris for 24-well plates, of the brand "Sarstedt". If you are using 48-well plates, you will need a custom coordinate file, following the same specifications as the 24-well plates. Be mindful, some 24-well plates might have different dimensions. The idea is to add some coordinate files to this repository in the end, so there is some choice for future users. If you have new plate dimensions, feel free to send them to me so I can add them. 

 - Whilst the script is running, it will print the calculated FvFm values to Git Bash. It will also print the name of each plate image that is analysed and the total number of images analysed as part of the script. In addition, if the script finds anything unusual (e.g. records already present in the folders above which should be empty) then it will print a warning message.
 - Note: An additional python file in the folder “get_fvfm_black_plates_v2.py” is to be used for analysis of images generated using the black cell culture plates provided by Sarstaedt (prod. No.: 94.6000.014).

### 4. Run the script:

```bash 
python get_fvfm_v3.py --exp-id <exp_id> --xpim-dir ./runs/input/<exp_id_xpim>/ --well-coord ./plate_formats/24_wells_transposed.csv --coord-format auto --threshold <your_threshold>
```

### 5. End of script:
Once the script has finished running (message printed: ```End of script. Number of files analysed: [...]```) check the output folder:

![Figure 6: Example output from "get_fvfm_v2.py" script. Note that an error message warning about future deprecation exists. This does not affect the output, and an update is currently in progress to remove this error.).](./screenshots/screenshot_19.jpg)

 - A file `<exp_id>_fvfm_<timestamp>/FvFm_output.csv` should now be present, which contains the Y(II) values of all the .xpim files.
 - In the "threshold_output" folder there should be a series of **contrast images** for each of your plates. These will be used to generate the plant area data...

```bash
## what is in the output folder
ls -lrth fvfm_<exp_id>_<timestamp>
```

## Extract plant area data from "Contrast" images
First, the ImageJ macro needs the output directories (folders) to be already created. If this is not the case, it will crash. 

```bash
## create the plant_area_data output directory, as well as the debug subfolder
# mkdir = make directory. -p option enables creation of subdirectory as well
mkdir -p runs/plant_area_<exp_id>/debug/
```


Right now, the input and output directories are "hardcoded", meaning they have to be changed before running the macro. In other words, if you use the "get_plant_area.txt" macro as is, it will look for the contrast images in a folder named "input_dir" (which doesn't exist) and try to write the output to a folder named "output_dir" (also does not exist). This little python script will replace these generic folder names with your actual names.            
The `input` directory is the <output_dir>/threshold_output/, where `output_dir` is the one created by the `get_fvfm_v3.py` script (automatically made using your Exp_ID, and the Timestamp). 
```bash
## 
python replace_inout_macro.py --input <fvfm_exp_id_timestamp> --output plant_area_<exp_id> --macro-in macros/get_plant_area.txt --macro-out macros/get_plant_area_mod.txt
```

The file created (specified by `--macro-out`) is the one you have to be used in ImageJ. 

Open ImageJ. Select "Plugins > Macros > Run... ". Then navigate to `PAM_Analysis_Pipeline/PAM_analysis_packages/` and select the modified `get_plant_area_mod.txt` macro you just created.

 - Note: An alternative ImageJ macro file exists called “Contrast_area_quant_black_plates_v2.txt”. This file is to be used for analysis of images using the black cell culture plates provided by Sarstaedt (prod. No.: 94.6000.014), as the well locations are different from standard plates.

![Figure 7: Method for running Macro files in ImageJ](./screenshots/Screenshot_10.jpg)

When you choose the macro, ImageJ will open a window and prompt you to **choose a folder**, which contains your data. There you just have to click on `runs`, and then `Select`, and you're good to go ! 

 - Note: This macro (and older iterations) require ImageJ 1.53e and Java 1.8.0 to run correctly. You can check your version of ImageJ/Java by opening ImageJ and right-clicking on the bottom banner:
 
 ![Figure 8: Right-clicking the bottom banner of ImageJ will provide the version of ImageJ and Java installed.](./screenshots/screenshot_20.jpg)

- When the script is running correctly, a number of windows will open up. Four windows show the results from the analysis. 

- An additional window named "Log" will also be generated:

![Figure 9: Example contents of the ImageJ 'Log' window](./screenshots/Screenshot_11.jpg)

- This file shows an overview of what the script has run, and should help with any troubleshooting. The first two lines show the folder paths selected for the input and output files, as understood by the script. If you have trouble with running the script, check these lines to make sure the path names are being read correctly (and reflect the true path to your required folders). The following lines in the Log file display which files have been analysed by the script. If 1) files of other formats (e.g. .csv files) or 2) other folders are present within the input directory, additional lines in the log will identify that they have been detected (but not processed).

All necessary data also saved to the ouput directory, so ImageJ windows can be closed once the script has finished running. The easiest way to do this is to right-click on the ImageJ icon at the bottom of the screen and select "Close all windows".

- In your output directory a .csv files should now be present for each contrast image analysed. Additionally, in the "debug" folder, there should be a .jpg image of the contrast image with the areas analysed using the _"Analyse particles"_ ImageJ function have been collected. **Please check the images in this debug file!** If you encounter unusual results during your analysis, it may be due to the incorrect positioning of a plate in the image. Plates which are not correctly positioned will have to be manually processed.

## Combine Plant Area Data and FvFm:

To combine the FvFm data in a .csv file together with the Plant Area generated using the ImageJ macro, run the **"combine_data.py"** script. In Git Bash, enter the following command:
```bash
python combine_data_v3.py --fvfm-file runs/fvfm_<exp_id>_<timestamp>/FvFm_output.csv --pa-dir runs/plant_area_<exp_id>/ --outpath ./runs/<exp_id>_combined/
```
# check that the combine_data will create the output folder, and add option for filename. 

- Note: The same warning is outputted as for the "get_fvfm_v3.py" script. Again, this does not affect the results, and will be removed in future versions.

In the "output" folder, a file named "Combined_output.csv" should now be present. This csv file should has five columns:

 - **Plate**: The name given of the plate analysed
 - **Well**: The number of the well analysed (see image below for well numbering system)
 - **Total Area**: The plant area output from ImageJ of the well
 - **FvFm**: The FvFm value for the plants in the well
 - **Area_FvFm**: The plant area score x FvFm score.

![Figure 10: Numbering of wells in 24-well plates](./screenshots/Screenshot_13.jpg)

This "Combined_output.csv" file can now be used for data analysis.

