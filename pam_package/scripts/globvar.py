# globvar.py
## set global variables
class GlobVar:
    def __init__(self, xpim_dir, tif_dir, debug, outpath, wells):
        self.xpim_dir = xpim_dir
        self.tif_dir = tif_dir
        self.debug = debug
        self.outpath = outpath
        self.wells = wells
# global debug_cropped
# debug_cropped = "./debug/cropped_images"
# global xpim_dir
# global tif_dir
# global outpath
# global wells