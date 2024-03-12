import math
import pandas as pd
from scripts import Analyse_FvFm_new
from skimage import filters
from plantcv import plantcv as pcv
from PIL import Image

def get_fvfm_per_well(image_file, key, thresh, fmax_plate, GlobVar):
    """
    get_fvfm_per_well takes in the tif_file (image_file), the threshold (default = yen), the fmax_plate, and the Well_number (key). 
    'image_file' is actually the basename for the tif_stack (imagefile-1, imagefile-2 and imagefile-3.tif). 
    imagefile-1.tif, imagefile-2.tif and imagefile-3.tif are opened using Image (PIL package), cropped to the current Well coordinates, and cropped image is saved (named as 'fmin', 'fmax', and 'fdark', respectively). 
    Then with PlantCV, cropped images are read and 'fmin', 'fmax' and 'fdark' are extracted from corresponding images. 
    Threshold value is used to filter out highlighted plate areas, and 'threshold_image' is created.
    FvFm values are calculated and a DataFrame with these values is returned. 
    """
    # Create images for each well
    # For each plate image, the image is opened, cropped and the cropped image is saved
    with Image.open(f"{GlobVar.tif_dir}/tif_frames/{image_file}-1.tif") as plate_fmin:
        cropped_fmin = plate_fmin.crop(GlobVar.wells[key])
        cropped_fmin.save(f"{GlobVar.debug}/fmin/{image_file}_fmin_{key}.tif", format=None)
        
    with Image.open(f"{GlobVar.tif_dir}/tif_frames/{image_file}-2.tif") as plate_fmax:
        cropped_fmax = plate_fmax.crop(GlobVar.wells[key])
        cropped_fmax.save(f"{GlobVar.debug}/fmax/{image_file}_fmax_{key}.tif", format=None)
        
    with Image.open(f"{GlobVar.tif_dir}/tif_frames/{image_file}-3.tif") as plate_fdark:
        cropped_fdark = plate_fdark.crop(GlobVar.wells[key])
        cropped_fdark.save(f"{GlobVar.debug}/fdark/{image_file}_fdark_{key}.tif", format=None)
    
    # Read back in using pcv functions (reads in images as numpy arrays)
    fmin, _, _ = pcv.readimage(f"{GlobVar.debug}/fmin/{image_file}_fmin_{key}.tif", mode="native")
    fmax, _, _ = pcv.readimage(f"{GlobVar.debug}/fmax/{image_file}_fmax_{key}.tif", mode="native")
    fdark, _, _ = pcv.readimage(f"{GlobVar.debug}/fdark/{image_file}_fdark_{key}.tif", mode="native")

    # Return threshold value based on Yen’s method.
    if thresh == "yen":
        threshold_lvl = filters.threshold_yen(image=fmax_plate)
    else:
        threshold_lvl = thresh
    # Use the threshold value to filter out highlighted plate areas
    threshold_image = pcv.threshold.binary(gray_img=fmax, threshold=threshold_lvl, object_type='light')
    threshold_image = pcv.fill(threshold_image, size=5)

    # Carry out FvFm calculation
    part_Fv = Analyse_FvFm_new.analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=threshold_image, bins=256, label="fluor")
    if math.isnan(part_Fv):
        print(f"fvfm for {image_file}, {key} is nan!")
    df = pd.DataFrame([[image_file, key, part_Fv]], columns = ["Plate", "Well", "FvFm"])
    return df, threshold_image