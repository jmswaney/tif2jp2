import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path
import tifffile
# from PIL import Image
import multiprocessing
from skimage.measure import block_reduce


DOWNSAMPLE_OPTIONS = ['2', '4', '8']

def save_as_downsampled(arg_dict):
	input_path = arg_dict['input_path']
	output_path = arg_dict['output_path']
	tif_path = arg_dict['tif_path']
	downsample_factor = arg_dict['downsample_factor']

	tif_img = tifffile.imread(str(tif_path))

	downsampled_tif = block_reduce(tif_img, block_size=(downsample_factor, downsample_factor))
	downsampled_tif = downsampled_tif.astype(tif_img.dtype)

	# img = Image.fromarray(tif_img)

	output_subdir = output_path.joinpath(tif_path.relative_to(input_path).parent)
	output_subdir.mkdir(parents=True, exist_ok=True)

	downsampled_filename = tif_path.stem + '.tif'
	downsampled_path = output_subdir.joinpath(downsampled_filename)

	tifffile.imsave(str(downsampled_path), downsampled_tif)

	# img.save(downsampled_path, quality_mode='rates', quality_layers=[20])

class MainApplication(tk.Frame):

	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)
		self.parent = parent
		self.build_elements()

	def build_elements(self):
		self.parent.title('tif_downsampler')

		# Setup the grid layout
		self.parent.rowconfigure(5, weight=1)
		self.parent.columnconfigure(5, weight=1)
		self.grid(sticky=tk.W + tk.E + tk.N + tk.S)

		# Add an extry box for the input directory
		self.input_entry = tk.Entry(self, width=60)
		self.input_entry.grid(row=1, column=1, padx=2, pady=2, sticky=tk.W)
		self.input_entry.insert(0, 'Browse to the root image directory with tifs -->')

		# Add a progress bar
		self.progress_bar = ttk.Progressbar(self, length=360, mode='determinate')
		self.progress_bar.grid(row=2, column=1, padx=2, pady=2, sticky=tk.E)

		# Create variables to store the directories
		self.input_path = None
		self.output_path = None

		# Make a browse button
		self.browse_btn = tk.Button(self, text='Browse', width=10, command=self.get_directory)
		self.browse_btn.grid(row=1, column=2, sticky=tk.W)

		# Make a convert button
		self.convert_btn = tk.Button(self, text='Convert', width=10, command=self.convert)
		self.convert_btn.grid(row=2, column=2, sticky=tk.W)

		# Give options for downsampling
		self.downsample_factor = tk.StringVar(self.parent)
		self.downsample_factor.set(DOWNSAMPLE_OPTIONS[0])

		self.dropdown = tk.OptionMenu(self.parent, self.downsample_factor, *DOWNSAMPLE_OPTIONS)
		self.dropdown.grid(row=0, column=3, sticky=tk.W)

	def set_entry_text(self, text):
		self.input_entry.delete(0, tk.END)
		self.input_entry.insert(0, text)

	def get_directory(self):
		browse_str = filedialog.askdirectory(parent=self.parent, title='Please select the root image directory')
		in_p = Path(browse_str)
		if in_p.exists():
			self.set_entry_text(str(in_p))
			self.input_path = in_p		

	def convert(self):
		if self.input_path is not None and self.input_path.exists() and self.input_path.is_dir():

			self.output_path = Path(self.input_path.parent).joinpath(str(self.input_path)+'_downsampled')
			self.output_path.mkdir(exist_ok=True)

			tif_paths = list(self.input_path.glob('**/*.tif*'))
			nb_tifs = len(tif_paths)

			self.progress_bar['value'] = 0
			self.progress_bar['maximum'] = nb_tifs-1
			
			arg_dicts = []
			for i, tif_path in enumerate(tif_paths):
				arg_dict = {
					'input_path': self.input_path,
					'output_path': self.output_path,
					'tif_path': tif_path,
					'downsample_factor': int(self.downsample_factor.get()),
				}
				arg_dicts.append(arg_dict)

			nb_cpu = multiprocessing.cpu_count()
			nb_processes = max(1, nb_cpu-1)
			with multiprocessing.Pool(processes=nb_processes) as p:
				for i, _ in enumerate(p.imap_unordered(save_as_downsampled, arg_dicts)):
					self.progress_bar['value'] = i
					self.parent.update()

if __name__ == '__main__':
	multiprocessing.freeze_support()
	root = tk.Tk()
	app = MainApplication(root)
	root.mainloop()