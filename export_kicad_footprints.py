from pathlib import Path
import os

lib_name = "SymbolOST"
lib_pretty_name = lib_name+".pretty"

tag = "symbol"

def get_path_to_lib():
    cwd = Path.cwd()
    
    if lib_name == cwd.name :
        print("cwd")
        return cwd
    
    # If not the cwd, check if the folder is a child to the cwd
    maybe_folder = cwd / lib_name
    if maybe_folder.exists() and maybe_folder.is_dir():
        print("Child to cwd!")
        return maybe_folder

    # If not there, check its parrent first.
    if cwd.parent.name == lib_name :#lib_name == os.path.pardir(path_of_the_directory):
        print("Parrent of cwd")
        return cwd.parent
    raise FileExistsError("Cant find "+ lib_name +" Folder")

def get_pretty_path(path_to_lib):
    if isinstance(path_to_lib,str):
        path_to_lib = Path(path_to_lib)
    if not issubclass(type(path_to_lib), Path):
        raise TypeError("Given object is not a path")
        
    pretty_folder = path_to_lib / lib_pretty_name
    if not (pretty_folder.exists() and pretty_folder.is_dir()):
        raise FileExistsError("Cant find "+lib_name+".pretty Folder")
    return pretty_folder

def create_pretty_files(input_path,output_path, output_sizeses_mm = 0):
    """
    If given input_path is a folder then all .svg files will be converted. Else only given .svg¨
    if given output_size_mm = 0 then the original dimension will be used (scale_factor = 1)
    """
    if not isinstance(input_path, list):
        input_path = [input_path]

    if not isinstance(output_sizeses_mm, list):
        output_sizeses_mm = [output_sizeses_mm]

    # Remove duplicates
    output_sizeses_mm = list(dict.fromkeys(output_sizeses_mm))

    files_to_convert = []
    for path in input_path:
        # If given input is a string, convert it.
        if not issubclass(type(path), Path):
            path = Path(path)

        if not path.exists():
            raise FileExistsError("Input path:" + path.absolute() + " dose not exists.")
        if path.is_dir():
            for subpath in path.iterdir():
                if subpath.suffix == ".svg":
                    files_to_convert.append(subpath)
        else:
            if subpath.suffix == ".svg":
                files_to_convert.append(path)
            
    if not output_path.exists():
        raise FileExistsError("Output path:" + output_path.absolute() + " dose not exists.")
    
    # Here files_to_convert contains all files that should be processed.
    for svg in files_to_convert:
        split_name = svg.stem.split("_")
        # Extract name from file name
        symbol_name = split_name[0]
        # Extract dimension from file name
        orig_size = split_name[1].split("mm")[0]
        orig_size = int(orig_size)
        # Extract type from file name
        symbol_type = split_name[2]
        # Now construct command to pass to svg2mod
        for size in output_sizeses_mm:
            if size >0:
                scale_factor = size/orig_size
                size_str = str(size)
            else:
                scale_factor = 1
                size_str = str(orig_size)
            co_path = output_path / (symbol_name + "_" + size_str +"mm_"+symbol_type + ".kicad_mod")
            #svg2mod.exe -i $silk_screen_file_name --format pretty --factor ($size/$base_size) -c -o $save_path
            cmd_str = "svg2mod -i " + str(svg.absolute()) + " --format pretty --factor " + str(scale_factor) + " -c -o " + str(co_path.absolute())
            os.system(cmd_str)
    pass

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
    path_to_lib = get_path_to_lib()
    path_to_pretty_folder = get_pretty_path(path_to_lib)
    output_dims = [5,8,10,12,14,16,20,25]
    created_files = create_pretty_files(path_to_lib,path_to_pretty_folder)

    # main()