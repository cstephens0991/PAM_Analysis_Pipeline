import argparse

def main():
    input_dir, output_dir, macro_in, macro_out, coord = parsing_arguments()
    with open(macro_in, "r") as file:
        data = file.read()
        data = data.replace("input_dir", input_dir)
        data = data.replace("output_dir", output_dir)
        #if coord is not None:
            ## read the csv file with the coordinates
            ## replace the entire centre of the macro to create a new version iwht all coordinates
    with open(macro_out, "w") as file:
        file.write(data)

def parsing_arguments():
    parser = argparse.ArgumentParser(
        prog='replace_inout_macro.py',
        description='This script will replace the input and output directory in the imageJ macro (get_plant_area.txt).')
    parser.add_argument('--input', help="Name of your get_fvfm output directory.", required=True)
    parser.add_argument('--output', help = "Name of the directory where the plant area data will be stored.", default = "plant_area_data")
    parser.add_argument('--macro-in', help = "Name of the imageJ macro file [default = get_plant_area.txt].", default = "get_plant_area.txt")
    parser.add_argument('--macro-out', help = "Name of the output imageJ macro file [default = get_plant_area_mod.txt].", default = "get_plant_area_mod.txt")
    parser.add_argument('--plate-coordinates', help = "Path to the CSV file containing the coodinates for the wells of the plate, if it is not standard 24 well plates.", default = None)
    args = vars(parser.parse_args())
    input_dir = args["input"]
    output_dir = args["output"]
    macro_in = args["macro_in"]
    macro_out = args["macro_out"]
    coord = args["plate_coordinates"]
    return input_dir, output_dir, macro_in, macro_out, coord

if __name__ == '__main__':
    main()