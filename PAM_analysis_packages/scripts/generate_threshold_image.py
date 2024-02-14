import cv2 as cv2
from plantcv import plantcv as pcv
from skimage import filters

def generate_threshold_image(image_file, thresh, GlobVar):
    """
    generate_threshold_image takes in the tif_file and the threshold (default being yen's threshold). 
    Using PlantCV, it reads the image and extracts 'fmax_plate', then creates a thresholded image (returns 'threshold_image'). 
    It also writes the 'threshold_image' to the outpath/threshold_output/xxx.tif. 
    """
    # Create contrast image and save to output/threshold_output folder
    #fmin_plate, path, filename = pcv.readimage(f"{tif_dir}/tif_frames/{image_file}-1.tif", mode = "native")
    fmax_plate, _, _ = pcv.readimage(f"{GlobVar.tif_dir}/tif_frames/{image_file}-2.tif", mode = "native")
    #fdark_plate, path, filename = pcv.readimage(f"{tif_dir}/tif_frames/{image_file}-3.tif", mode = "native")
    if thresh == "yen":
        threshold_lvl = filters.threshold_yen(image=fmax_plate)
    else:
        threshold_lvl = thresh
    threshold_image = pcv.threshold.binary(gray_img = fmax_plate, threshold = threshold_lvl, object_type = 'light')
    threshold_image = pcv.fill(threshold_image, size = 5)
    cv2.imwrite(f"{GlobVar.outpath}/threshold_output/{image_file}_threshold_image.tif", threshold_image)
    return fmax_plate, threshold_image