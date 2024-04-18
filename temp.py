import re
import glob
import os
import pandas as pd
def extract_number(filename):
    pattern = r"\d{4}"  # Matches exactly four digits
    match = re.search(pattern, filename[12:17])  # Search within specific range
    if match:
        try:
            return int(match.group(0))
        except ValueError:
            raise ValueError(f"Could not convert extracted string '{match.group(0)}' to integer")
    else:
        return None  # Indicate that no number was found
tif_location = r'path_to_rasters'
filenames = glob.glob(os.path.join((tif_location, '*.tif'))
txt_file = r'path_to_textak'
txt_file_new = r'path_to_textak_new'


df_textak = pd.read_csv(txt_file, header=None)
        
for filename in filenames:
    extracted_number = extract_number(filename)
    if extracted_number is not None:
        df_textak.loc[df_textak.iloc[:, 1] == extracted_number, -1] = filename

        print(f"Extracted number from '{filename}': {extracted_number}")
    else:
        print(f"No number found in '{filename}'")

df_textak.to_csv(txt_file_new, header=None, index=False)



