# Fluorescence Analysis

import os
import cv2
import numpy as np
import pandas as pd
## from plotnine import ggplot, geom_label, aes, geom_line
from plantcv.plantcv import print_image, plot_image, fatal_error, params, outputs
# from plantcv.plantcv import plot_image
# from plantcv.plantcv import fatal_error
# from plantcv.plantcv import params
# from plantcv.plantcv import outputs
from PIL import Image, ImageSequence
import sys
import os
import cv2 as cv2
from plantcv import plantcv as pcv
from skimage import filters
import math

def analyze_fvfm(fdark, fmin, fmax, mask, bins=256, label="default"):
    """Analyze PSII camera images.
    Inputs:
    fdark       = grayscale fdark image
    fmin        = grayscale fmin image
    fmax        = grayscale fmax image
    mask        = mask of plant (binary, single channel)
    bins        = number of bins (1 to 256 for 8-bit; 1 to 65,536 for 16-bit; default is 256)
    label       = optional label parameter, modifies the variable name of observations recorded
    Returns:
    analysis_images = list of images (fvfm image and fvfm histogram ggplot object)
    :param fdark: numpy.ndarray
    :param fmin: numpy.ndarray
    :param fmax: numpy.ndarray
    :param mask: numpy.ndarray
    :param bins: int
    :param label: str
    :return analysis_images: numpy.ndarray
    """
    # Auto-increment the device counter
    params.device += 1
    # Check that fdark, fmin, and fmax are grayscale (single channel)
    if not all(len(np.shape(i)) == 2 for i in [fdark, fmin, fmax]):
        fatal_error("The fdark, fmin, and fmax images must be grayscale images.")

    # QC Fdark Image
    # CS: This was edited as the fdark image was throwing an error error: OpenCV(4.6.0) D:\bld\libopencv_1671461696155\work\modules\core\src\arithm.cpp:230: error: (-215:Assertion failed) (mtype == CV_8U || mtype == CV_8S) && _mask.sameSize(*psrc1) in function 'cv::binary_op'
    fdark_mask = cv2.bitwise_and(fdark, fdark, mask=mask)
    if np.amax(fdark_mask) > 2000:
        qc_fdark = False
    else:
        qc_fdark = True

    # Mask Fmin and Fmax Image
    fmin_mask = cv2.bitwise_and(fmin, fmin, mask=mask)
    fmax_mask = cv2.bitwise_and(fmax, fmax, mask=mask)

    # Calculate Fvariable, where Fv = Fmax - Fmin (masked)
    fv = np.subtract(fmax_mask, fmin_mask)
    
    # When Fmin is greater than Fmax, a negative value is returned.
    # Because the data type is unsigned integers, negative values roll over, resulting in nonsensical values
    # Wherever Fmin is greater than Fmax, set Fv to zero
    fv[np.where(fmax_mask < fmin_mask)] = 0
    analysis_images = []

    # Calculate Fv/Fm (Fvariable / Fmax) where Fmax is greater than zero
    # By definition above, wherever Fmax is zero, Fvariable will also be zero
    # To calculate the divisions properly we need to change from unit16 to float64 data types
    fvfm = fv.astype(np.float64)

    fmax_flt = fmax_mask.astype(np.float64)
    fvfm[np.where(fmax_mask > 0)] /= fmax_flt[np.where(fmax_mask > 0)]
    analysis_images.append(fvfm)

    # Calculate the median Fv/Fm value for non-zero pixels
    fvfm_median = np.median(fvfm[np.where(fvfm > 0)])

    # This command is currently commented to see if it is responsible for the error genrated when running the script...
    # fvfm_mean = np.mean(fvfm[np.where(fvfm > 0)])
    # Calculate the histogram of Fv/Fm non-zero values
    fvfm_hist, fvfm_bins = np.histogram(fvfm[np.where(fvfm > 0)], bins, range=(0, 1))
    # fvfm_bins is a bins + 1 length list of bin endpoints, so we need to calculate bin midpoints so that
    # the we have a one-to-one list of x (FvFm) and y (frequency) values.
    # To do this we add half the bin width to each lower bin edge x-value
    midpoints = fvfm_bins[:-1] + 0.5 * np.diff(fvfm_bins)

    # Calculate which non-zero bin has the maximum Fv/Fm value
    max_bin = midpoints[np.argmax(fvfm_hist)]
    
    # Create a dataframe
    # dataset = pd.DataFrame({'Plant Pixels': fvfm_hist, 'Fv/Fm': midpoints})
    # Make the histogram figure using plotnine
    # fvfm_hist_fig = (ggplot(data=dataset, mapping=aes(x='Fv/Fm', y='Plant Pixels'))
    #                  + geom_line(color='green', show_legend=True)
    #                  + geom_label(label='Peak Bin Value: ' + str(max_bin),
    #                               x=.15, y=205, size=8, color='green'))
    # analysis_images.append(fvfm_hist_fig)
    # print(f"fvfm_median = {fvfm_median}")
    # print(f"fvfm_max = {max_bin}")
    # print(f"fvfm_mean = {fvfm_mean}")
    if params.debug == 'print':
        print_image(fmin_mask, os.path.join(params.debug_outdir, str(params.device) + '_fmin_mask.png'))
        print_image(fmax_mask, os.path.join(params.debug_outdir, str(params.device) + '_fmax_mask.png'))
        print_image(fv, os.path.join(params.debug_outdir, str(params.device) + '_fv_convert.png'))
        # fvfm_hist_fig.save(os.path.join(params.debug_outdir, str(params.device) + '_fv_hist.png'), verbose=False)
    elif params.debug == 'plot':
        plot_image(fmin_mask, cmap='gray')
        plot_image(fmax_mask, cmap='gray')
        plot_image(fv, cmap='gray')
        
    outputs.add_observation(sample=label, variable='fvfm_hist', trait='Fv/Fm frequencies',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=list,
                            value=fvfm_hist.tolist(), label=np.around(midpoints, decimals=len(str(bins))).tolist())
    outputs.add_observation(sample=label, variable='fvfm_hist_peak', trait='peak Fv/Fm value',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=float,
                            value=float(max_bin), label='none')
    outputs.add_observation(sample=label, variable='fvfm_median', trait='Fv/Fm median',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=float,
                            value=float(np.around(fvfm_median, decimals=4)), label='none')
    outputs.add_observation(sample=label, variable='fdark_passed_qc', trait='Fdark passed QC',
                            method='plantcv.plantcv.fluor_fvfm', scale='none', datatype=bool,
                            value=qc_fdark, label='none')

    # Store images
    outputs.images.append(analysis_images)

    # return analysis_images
    return fvfm_median

# CS: This script extracts the individual frames from the stacked TIF file.

def extract_frames(infile,outdir):
    '''
    input:  infile - a multiframe image file
            outdir - the directory to save each of the frames of the image file
    output: the side effect of running this function will be new files using the basename from infile appended with the frame id (1, 2, 3,...).

    Note: you can use . to save to the same directory or .. to save to a directory up one level. Otherwise outdir should be absolute or relative to your working directory.
    '''

    bn = os.path.splitext(os.path.basename(infile))[0]

    with Image.open(infile) as im:
        index = 1
        for frame in ImageSequence.Iterator(im):
        # CS: save to export directory - combine bn (basename of file) and index (index number of frame)
            frame.save(os.path.join(outdir,"%s-%d.tif" % (bn,index)))
            index += 1

# if __name__ == "__main__":
#     extract_frames(sys.argv[1],sys.argv[2])

def convert2plantcv(csv_dict):
    """
    Convert2plantcv is a function that will transform the Plate Well coordinates from the ImageJ format, to the one that PlantCV uses. 
    ImageJ sees Well coordinates as:  [100, 130, 70, 70]  , corresponding to [x_start, y_start, x_width, y_width].
    PlantCV sees Well coordinates as: [100, 130, 170, 200], corresponding to [x_start, y_start, x_end, y_end]. 
    This script will be able to take in both types of coordinates, but if the format is ImageJ, it will convert the data to a PlantCV compatible format. 
    """
    plantcv_coord = {}
    for key, value in csv_dict.items():
        x_start = value[0]; y_start = value[1]; x_width = value[2]; y_width = value[3]
        plantcv_coord[key] = [x_start, y_start, x_start+x_width, y_start+y_width]
        # print(f"{key}: {csv_dict[key]}")
        # print(f"{key}: {new_dict[key]}")
    return plantcv_coord

def generate_threshold_image(image_file, thresh, GlobVar):
    """
    generate_threshold_image takes in the tif_file and the threshold (default being yen's threshold). 
    Using PlantCV, it reads the image and extracts 'fmax_plate', then creates a thresholded image (returns 'threshold_image'). 
    It also writes the 'threshold_image' to the outpath/threshold_output/xxx.tif. 
    """
    # Create contrast image and save to output/threshold_output folder
    #fmin_plate, path, filename = pcv.readimage(f"{tif_dir}/tif_frames/{image_file}-1.tif", mode = "native")
    image2read = os.path.abspath(f"{GlobVar.tif_dir}/tif_frames/{image_file}-2.tif")
    print(image2read)
    fmax_plate, _, _ = pcv.readimage(image2read, mode = "native")
    #fdark_plate, path, filename = pcv.readimage(f"{tif_dir}/tif_frames/{image_file}-3.tif", mode = "native")
    if thresh == "yen":
        threshold_lvl = filters.threshold_yen(image=fmax_plate)
    else:
        threshold_lvl = thresh
    threshold_image = pcv.threshold.binary(gray_img = fmax_plate, threshold = threshold_lvl, object_type = 'light')
    threshold_image = pcv.fill(threshold_image, size = 5)
    cv2.imwrite(f"{GlobVar.outpath}/threshold_output/{image_file}_threshold_image.tif", threshold_image)
    return fmax_plate, threshold_image

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
    part_Fv = analyze_fvfm(fdark=fdark, fmin=fmin, fmax=fmax, mask=threshold_image, bins=256, label="fluor")
    if math.isnan(part_Fv):
        print(f"fvfm for {image_file}, {key} is nan!")
    df = pd.DataFrame([[image_file, key, part_Fv]], columns = ["Plate", "Well", "FvFm"])
    return df, threshold_image

def is_imageJ(wells_dict):
    '''
    is_imageJ will try to automatically detect the format of the input well coordinates. To do this, it assumes that all wells have equal widths. 
    Therefore, it simply checks whether the last 2 elements of each Well_coord array are always the same. If so, returns True, else returns False.
    '''
    csv_df = pd.DataFrame.from_dict(wells_dict, orient = 'columns')
    x_end = np.unique(csv_df.loc[2])
    y_end = np.unique(csv_df.loc[3])
    if (len(x_end) == 1) and (len(y_end) == 1):
        print("Detected ImageJ format for well coordinates.")
        return True
    else:
        print("Detected coordinate format different from ImageJ.")
        return False
