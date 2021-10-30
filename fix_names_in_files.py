
import os

lib_name = "SymbolOST"
lib_pretty_name = lib_name+".pretty"

tag = "symbol"

def get_propper_path():
    path_of_the_directory= os.getcwd()
    directory_list = os.listdir()
    # Finding the folder
    if lib_name == os.path.basename(path_of_the_directory):
        return path_of_the_directory
        print("cwd")
    else:
        lib_folder_name = "lib"
        lib_path = os.path.join(path_of_the_directory,lib_folder_name)
        if not os.path.isdir(lib_path):
            lib_path = path_of_the_directory
        path_to_symbol_folder = ""

        path_to_symbol_folder = os.path.join(lib_path,lib_name)
        print(path_to_symbol_folder)
        if not os.path.isdir(path_to_symbol_folder):
            raise FileNotFoundError("Could not locate dir...")
        return path_to_symbol_folder


def main():
    # path_of_the_directory= 'E:\Python for Data Science'
    path_of_the_directory = get_propper_path()
    # step into pretty folder
    pretty_folder = os.path.join(path_of_the_directory,lib_pretty_name)
    
    # Here the folder is found
    for filename in os.listdir(pretty_folder):
        # replace Copper with cu
        # replace SilkScreen with ss

        # replace svg2mod with propper name
        # set a good tag (name up to first _ or to size marking (first number))
        # See how to remove ss from top of cu ones.
        file_path = os.path.join(pretty_folder,filename)
        output_file_path = file_path # os.path.join(pretty_folder,"out_"+filename)
        #if os.path.isfile(f):
        with open(file_path,'rt') as f:
            text = f.read()
            # first replace the tag

        replacement_string = filename.split(".kicad_mod")[0]
        replacement_string = replacement_string.replace("SilkScreen", "ss")
        replacement_string = replacement_string.replace("Copper", "cu")
        tag = replacement_string.split("_")[0]

        text = text.replace("tags svg2mod", "tags " + tag )
        text = text.replace("svg2mod",replacement_string )

        with open(output_file_path,'wt') as f:
            f.write(text)
    
    

if __name__ == "__main__":
    main()