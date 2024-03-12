import numpy as np
import pandas as pd

def is_imageJ_coord(csv_dict):
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