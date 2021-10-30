# Set-ExecutionPolicy RemoteSigned –Scope Process

$sizes = (5,10,20,30,40)
$copper_file_name = "bubbla_50mm_copper.svg"
$silk_screen_file_name = "bubbla_50mm_silk_screen.svg"


$underscore_index =  $copper_file_name.IndexOf('_')
$base_size = $copper_file_name.Substring($underscore_index+1,2)
$base_size = [int] $base_size
Write-Output "size:" $base_size

$symbol_name = $copper_file_name.Substring(0,$underscore_index)

Write-Output $symbol_name
$output_path = "SymbolsOST.pretty"
Write-Output "Output folder:" $output_path

# Copper versions
foreach ($size in $sizes){
	$output_file_name = $symbol_name + "_"+($size)+"mm_Copper"
	$save_path = Join-Path -Path $output_path $output_file_name
	Write-Output "Output file:" $save_path
	#echo (Join-Path -Path $path_to_img "hej")
	Write-Output "Size factor:" ($size/$base_size)
	svg2mod.exe -i $copper_file_name --format pretty --factor ($size/$base_size) -c -o $save_path
}

$underscore_index =  $silk_screen_file_name.IndexOf('_')
$base_size = $silk_screen_file_name.Substring($underscore_index+1,2)
$base_size = [int] $base_size
# Write-Output "size:" $base_size

$symbol_name = $copper_file_name.Substring(0,$underscore_index)

# Silk screen versions
foreach ($size in $sizes){
	$output_file_name = $symbol_name+"_"+($size)+"mm_SilkScreen"
	$save_path = Join-Path -Path $output_path $output_file_name
	Write-Output "Output file:" $save_path
	#echo (Join-Path -Path $path_to_img "hej")
	Write-Output "Size factor:" ($size/$base_size)
	svg2mod.exe -i $silk_screen_file_name --format pretty --factor ($size/$base_size) -c -o $save_path
}


Write-Output "Running python script"
python "fix_names_in_files.py"
Write-Output "Done!"