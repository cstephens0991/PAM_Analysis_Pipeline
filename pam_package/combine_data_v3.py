import pandas as pd
import glob
import re
import numpy as np
import argparse
import os

def main():
    fvfm, pa_dir, outpath = parsing_arguments()
    ## if outpath does not exist, create it
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    ## Read the FvFm data
    fvfm_data = pd.read_csv(f"{fvfm}")
    unique_plate_names = fvfm_data["Plate"].unique()

    ## Concatenate the plant area data
    plant_area_data = concat_plant_area_data(pa_dir, unique_plate_names)

    ## Check the plate name correspondance
    check_plate_names(plant_area_data, fvfm_data)

    ## Merge the data and dropped some of the columns
    merged_data = plant_area_data.merge(fvfm_data, how="inner", on=["Plate", "Well"])
    merged_data = merged_data.drop(columns=["Count", "Average Size", "%Area", "Mean", "Unnamed: 0"])

    # Combine ImageJ area score and FvFm score into a single value
    merged_data["Area_FvFm"] = merged_data["Total Area"] * merged_data["FvFm"]
    merged_data["FvFm_corrected"] = np.where(merged_data["Total Area"] == 0, 0, merged_data["FvFm"])
    merged_data.to_csv(f"{outpath}/combined_output.csv", index = False)

def parsing_arguments():
    parser = argparse.ArgumentParser(
        prog='combine_data_v3.py',
        description='This script is used to combine data from ImageJ (Plant Area) and the fvfm data (from get_fvfm_v3.py).')
    parser.add_argument('--fvfm-file', help="Path to the output csv file of get_fvfm_v3.py. This is a necessary argument.")
    parser.add_argument('--pa-dir', default = "./plant_area_data/",
                        help="Path to directory containing the *.tif files. [default = './plant_area_data/']")
    parser.add_argument('--outpath', help=f"Path to output directory which will contain the combined_output.csv file.")
    args = vars(parser.parse_args())
    fvfm = os.path.abspath(args["fvfm_file"])
    pa_dir = os.path.abspath(args["pa_dir"])
    outpath = os.path.abspath(args["outpath"])

    return fvfm, pa_dir, outpath

def concat_plant_area_data(pa_dir, plate_names):
    total_data = pd.DataFrame([], columns=["Plate", "Count", "Total Area", "Average Size", "%Area", "Mean"])
    for plate_name in plate_names:
        ## open file with the plate name
        plate_data = pd.read_csv(f"{pa_dir}/{plate_name}_threshold_image.csv")
        if plate_data.shape[0] != 24:
            print(f"{plate_name} length is {plate_data.shape[0]}")
        plate_data["Plate"] = plate_name
        plate_data["Well"] = np.arange(1, (len(plate_data)+1)).astype(int)
        ## add "Well" in front of numbers in Well column
        plate_data.Well = plate_data.Well.apply(lambda x: '_'.join(["Well", str(x)]))
        plate_data = plate_data.drop(columns="Slice")
        total_data = pd.concat([total_data, plate_data], axis=0)
    return total_data

def check_plate_names(plant_area_data, fvfm_data):
    # Get the plate names from the plant area data
    pa_plate_names = plant_area_data["Plate"].unique()
    # Get the plate names from the fvfm data
    fvfm_plate_names = fvfm_data["Plate"].unique()
    # Check if the plate names are the same
    if np.all(pa_plate_names == fvfm_plate_names):
        print("Plate names are the same in both datasets")
    else:
        print("Plate names are not the same in both datasets, please check this and re-run.")
        print(f"Plant area data plate names: {pa_plate_names.head()}")
        print(f"Fvfm plate names: {fvfm_plate_names.head()}")
        ## kill the program in this case
        exit()

if __name__ == '__main__':
    main()