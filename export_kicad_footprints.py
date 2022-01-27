from pathlib import Path
import os
import xml.etree.ElementTree as ET
import argparse


parser = argparse.ArgumentParser(description="Testing testing")
parser.add_argument('-m','--match', type=str, help='only convert files starting with the given string.')
parser.add_argument('-f','--force', action='store_true',help='force write all files, usual behaviour is to only write missing files.')
# parser.add_argument("-q", "--quiet", action="store_true") # svg2mod dose not support this.


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


def get_pretty_path(path_to_lib, lib_name):
    lib_pretty_name = lib_name+".pretty"
    if isinstance(path_to_lib, str):
        path_to_lib = Path(path_to_lib)
    if not issubclass(type(path_to_lib), Path):
        raise TypeError("Given object is not a path")
    
    # Construct the path
    pretty_folder = path_to_lib / lib_pretty_name
    # Check if it is exists.
    if not pretty_folder.exists():
        #Create folder
        pretty_folder.mkdir()
    else:
        if not pretty_folder.is_dir():
            # If the path is valid but it isnt a folder throw an error
            raise FileExistsError(lib_name+".pretty is not a folder...")
    return pretty_folder


class FileAndSize:
    def __init__(self, input_file, output_path, sizes) -> None:
        self.sizes = list(dict.fromkeys(sizes))
        if not isinstance(self.sizes, list):
            self.sizes = [self.sizes]

        self.input_file: Path = input_file
        if not self.input_file.exists() or not self.input_file.suffix == ".svg":
            raise FileExistsError(
                "Input path:" + str(self.input_file.absolute()) + " dose not exists.")

        self.output_path: Path = output_path
        if not self.output_path.exists():
            raise FileExistsError(
                "Output path:" + str(self.output_path.absolute()) + " dose not exists.")

    def convert(self,force_outout = False):
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
            if ( not output_path.exists() ) or force_outout:
                os.system(cmd_str)
            else:
                print("File exists:", str(output_path.absolute()))

            # Now change tag and name inside the file
            with open(output_path.absolute(), 'rt') as f:
                text = f.read()
            # Remove desc line
            descr_start = text.find("(descr")
            descr_end = text.find(")", descr_start)

            text = text[:(descr_start-2)] + text[(descr_end+2):]
            text = text.replace("tags svg2mod", "tags " + symbol_name)
            text = text.replace("svg2mod", symbol_full_name)

            with open(output_path.absolute(), 'wt') as f:
                f.write(text)


def find_files(input_path):
    """
    If given input_path is a folder then all .svg files will be converted. Else only given .svg¨
    if given output_size_mm = 0 then the original dimension will be used (scale_factor = 1)
    """

    if not isinstance(input_path, list):
        input_path = [input_path]

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


def main():
    # if -f flag, force output
    try:

        args = parser.parse_args()
    except SystemExit:
        print("Please doubble check arguments.")
        return -1
        
    # Get path to were the lib is, it might differ from cwd.
    path_to_lib = get_path_to_lib(lib_name)
    path_to_pretty_folder = get_pretty_path(path_to_lib, lib_name)

    # Configuration is stored in config.xml, both sizes and paths.
    root_node = ET.parse(path_to_lib/'config.xml').getroot()
    for size_group in root_node.findall('group'):
        output_dims = []
        # Append all output dimensions 
        for size in size_group.findall('sizes/size'):
            output_dims.append(int(size.text))

        # Convert all files.
        for file in size_group.findall('files/file'):
            if args.match and file.text[0:len(args.match)] == args.match:
                obj = FileAndSize(path_to_lib/file.text, path_to_pretty_folder, output_dims)
                obj.convert(force_outout = args.force)

if __name__ == "__main__":
    if main():
        print("ojojoj not good!")
