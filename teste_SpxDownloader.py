import os
from SpxSystem import SpxDonwloader

csv_folder = os.path.join(os.getcwd(), 'CSV_FILES')

spx = SpxDonwloader()
spx.export_outbound(path_download=csv_folder)