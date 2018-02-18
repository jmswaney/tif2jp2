import cx_Freeze
import sys
import os

includes = ['PIL', 'tifffile']
include_files = [r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\DLLs\tcl86t.dll',
	r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\DLLs\tk86t.dll',
	'logo.ico']

os.environ['TCL_LIBRARY'] = r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Justin Swaney\Anaconda3\envs\tif2jp2\tcl\tk8.6'

base = None

if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [cx_Freeze.Executable('src/tif2jp2.py', base=base, icon='logo.ico')]

cx_Freeze.setup(
	name = 'tif2jp2',
	options = {'build_exe': {'packages': ['tkinter', 'PIL', 'tifffile', 'numpy', 'lxml', 'pkg_resources._vendor'], 'include_files': include_files, 'includes': includes}},
	version = '0.01',
	description = 'An app to convert tifs to JPEG2000',
	executables = executables
	)