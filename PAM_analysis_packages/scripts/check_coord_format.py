import numpy as np
import pandas as pd

def is_imageJ(csv_dict):
    '''
    is_imageJ_coord will try to automatically detect the format of the input well coordinates. To do this, it assumes that all wells have equal widths. 
    Therefore, it simply checks whether the last 2 elements of each Well_coord array are always the same. If so, returns True, else returns False.
    '''
    csv_df = pd.DataFrame.from_dict(csv_dict, orient = 'columns')
    x_end = np.unique(csv_df.loc[2])
    y_end = np.unique(csv_df.loc[3])
    if (len(x_end) == 1) and (len(y_end) == 1):
        print("Detected ImageJ format for well coordinates.")
        return True
    else:
        print("Detected coordinate format different from ImageJ.")
        return False

import pandas as pd

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