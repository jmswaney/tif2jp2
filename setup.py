import cx_Freeze
import sys
import os

includes = ['tifffile', 'skimage']
include_files = [r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\DLLs\tcl86t.dll',
	r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\DLLs\tk86t.dll',
	'logo.ico']

os.environ['TCL_LIBRARY'] = r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\tcl\tk8.6'

base = None

if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [cx_Freeze.Executable('src/tif_downsampler.py', base=base, icon='logo.ico')]

cx_Freeze.setup(
	name = 'tif_downsampler',
	options = {'build_exe': {'packages': ['tkinter', 'skimage', 'multiprocessing', 'tifffile', 'numpy', 'lxml', 'pkg_resources._vendor'], 
			'include_files': include_files, 'includes': includes}},
	version = '0.02',
	description = 'An app to convert tifs to JPEG2000',
	executables = executables
	)