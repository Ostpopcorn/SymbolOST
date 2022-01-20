from pathlib import Path
import os




lib_name = "SymbolOST"

def get_path_to_lib(lib_name):
    cwd = Path.cwd()

    if lib_name == cwd.name:
        print("cwd")
        return cwd

    # If not the cwd, check if the folder is a child to the cwd
    maybe_folder = cwd / lib_name
    if maybe_folder.exists() and maybe_folder.is_dir():
        print("Child to cwd!")
        return maybe_folder

    maybe_folder = cwd / "lib"
    if maybe_folder.exists() and maybe_folder.is_dir():
        maybe_folder /= lib_name
        if maybe_folder.exists() and maybe_folder.is_dir():
            print("Project root!")
            return maybe_folder

    # If not there, check its parrent first.
    # lib_name == os.path.pardir(path_of_the_directory):
    if cwd.parent.name == lib_name:
        print("Parrent of cwd")
        return cwd.parent
    raise FileExistsError("Cant find " + lib_name + " Folder")


def get_pretty_path(path_to_lib,lib_name):
    lib_pretty_name = lib_name+".pretty"
    if isinstance(path_to_lib, str):
        path_to_lib = Path(path_to_lib)
    if not issubclass(type(path_to_lib), Path):
        raise TypeError("Given object is not a path")

    pretty_folder = path_to_lib / lib_pretty_name
    if not (pretty_folder.exists() and pretty_folder.is_dir()):
        raise FileExistsError("Cant find "+lib_name+".pretty Folder")
    return pretty_folder

class FileAndSize:
    def __init__(self, input_file, output_path, sizes) -> None:
        self.sizes = list(dict.fromkeys(sizes))
        if not isinstance(self.sizes, list):
            self.sizes = [self.sizes]

        self.input_file:Path = input_file
        if not self.input_file.exists() or not self.input_file.suffix == ".svg":
            raise FileExistsError(
                "Input path:" + self.input_file.absolute() + " dose not exists.")

        self.output_path:Path = output_path
        if not self.output_path.exists():
            raise FileExistsError(
                "Output path:" + self.output_path.absolute() + " dose not exists.")
    
    def convert(self):
        split_name = self.input_file.stem.split("_")
        # Extract name from file name
        symbol_name = split_name[0]
        # Extract dimension from file name
        orig_size = split_name[1].split("mm")[0]
        orig_size = int(orig_size)
        # Extract type from file name
        symbol_type = split_name[2]
        # Now construct command to pass to svg2mod
        for size in self.sizes:
            if size > 0:
                scale_factor = size/orig_size
                size_str = str(size)
            else:
                scale_factor = 1
                size_str = str(orig_size)
            symbol_full_name = symbol_name + "_" + size_str + "mm_"+symbol_type
            output_path = self.output_path / \
                (symbol_full_name + ".kicad_mod")
            # svg2mod.exe -i $silk_screen_file_name --format pretty --factor ($size/$base_size) -c -o $save_path
            cmd_str = "svg2mod -i " + str(self.input_file.absolute()) + " --format pretty --factor " + str(
                scale_factor) + " -c -o " + str(output_path.absolute())
            os.system(cmd_str)

            # Now change tag and name inside the file
            with open(output_path.absolute(), 'rt') as f:
                text = f.read()
            # Remove desc line
            descr_start = text.find("(descr")
            descr_end   = text.find(")",descr_start)
            
            text = text[:(descr_start-2)] + text[(descr_end+2):]
            text = text.replace("tags svg2mod", "tags " + symbol_name)
            text = text.replace("svg2mod", symbol_full_name)

            with open(output_path.absolute(), 'wt') as f:
                f.write(text)

def create_pretty_files(input_path, output_base_path, output_sizeses_mm=0):
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
            raise FileExistsError(
                "Input path:" + path.absolute() + " dose not exists.")
        if path.is_dir():
            for subpath in path.iterdir():
                if subpath.suffix == ".svg":
                    files_to_convert.append(subpath)
        else:
            if subpath.suffix == ".svg":
                files_to_convert.append(path)

    if not output_base_path.exists():
        raise FileExistsError(
            "Output path:" + output_base_path.absolute() + " dose not exists.")

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
            if size > 0:
                scale_factor = size/orig_size
                size_str = str(size)
            else:
                scale_factor = 1
                size_str = str(orig_size)
            symbol_full_name = symbol_name + "_" + size_str + "mm_"+symbol_type
            output_path = output_base_path / \
                (symbol_full_name + ".kicad_mod")
            # svg2mod.exe -i $silk_screen_file_name --format pretty --factor ($size/$base_size) -c -o $save_path
            cmd_str = "svg2mod -i " + str(svg.absolute()) + " --format pretty --factor " + str(
                scale_factor) + " -c -o " + str(output_path.absolute())
            os.system(cmd_str)

            # Now change tag and name inside the file
            with open(output_path.absolute(), 'rt') as f:
                text = f.read()
            # Remove desc line
            descr_start = text.find("(descr")
            descr_end   = text.find(")",descr_start)
            
            text = text[:(descr_start-2)] + text[(descr_end+2):]
            text = text.replace("tags svg2mod", "tags " + symbol_name)
            text = text.replace("svg2mod", symbol_full_name)

            with open(output_path.absolute(), 'wt') as f:
                f.write(text)
    pass


if __name__ == "__main__":
    path_to_lib = get_path_to_lib(lib_name)
    path_to_pretty_folder = get_pretty_path(path_to_lib,lib_name)
    output_dims = [5, 8, 10, 12, 14, 16, 20, 25]
    # created_files = create_pretty_files(path_to_lib, path_to_pretty_folder,output_dims)
    file = FileAndSize(path_to_lib/"bubbla_50mm_Copper.svg",path_to_pretty_folder,output_dims)
    file.convert()
    file = FileAndSize(path_to_lib/"bubbla_50mm_SilkScreen.svg",path_to_pretty_folder,output_dims)
    file.convert()


