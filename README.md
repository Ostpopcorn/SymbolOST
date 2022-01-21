# SymbolsOST
This is my KiCad library for footprints/touchmarks for my PCBs, but also some helpful symbols.

A bouns is the script `export_kicad_footprints.py` and `config.xml` which makes it easy to add new KiCad footprints to the lib based on svg files. Thanks [svg2mod](https://github.com/RobertBaruch/svg2mod/blob/master/). 



## Usage
When using it in my KiCad projects I follow this pattern since it matches the expected path for my other KiCad libraries. 

- ${KIPRJMOD} 
  - /lib/
     - /SymbolsOST/ 
        -  SymbolsOST.pretty
        -  ...
     - /more-libs ... / 

## Generation of new footprints

The script `export_kicad_footprints.py` uses [svg2mod](https://github.com/RobertBaruch/svg2mod/blob/master/) library (make sure to install it via `python -m pip install svg2mod`) to perform the conversion from svg files to KiCad footprint (.kicad_mod) files. To get the most out of this script a good understanding of [svg2mod/README.md](https://github.com/RobertBaruch/svg2mod/blob/master/README.md) will help.

The svg files should be named according to `{name}_{document_size_in_mm}mm_{layer}`. Some restrictions are: 
* `{name}` can not contain any `_`, since this is how the script splits the string. 
* `{document_size_in_mm}` should be se to match the largest dimension in the svg, since this is used to scale the output to correct size.
* `{layer}` can be anything and is out on the output files name. But this should describe what layers are used. 

 
It read which files to process from config.xml located in the root of the lib. The file is divided into groups in which file and sizes (in mm) are defined. This allows groups (files) to export different sizes. The file is formatted as follows

``` 
<root>
    <group>
        <sizes>
            <size>5</size>
            <size>8</size>
            ...
        </sizes>
        <files>
            <file>ost-bubble_50mm_Copper.svg</file>
            <file>ost-bubble_50mm_SilkScreen.svg</file>
            ...
        </files>
    </group>
    <group>
        <sizes>
            <size>5</size>
            <size>6</size>
            ...
        </sizes>
        <files>
            <file>wifi_50mm_Copper.svg</file>
            <file>wifi_50mm_SilkScreen.svg</file>
            ...
        </files>
    </group>
</root>
``` 
## Trubbleshooting
### My footprint look choppy (too low resolution)
I have not put in the time to expose this setting which svg2mod has, but there is a workaround. Just increase the size of the original svg file, larger dimensions in svg `=>` higher resolution! 