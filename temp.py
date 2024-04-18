import re
import glob
import os
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

df_textak = pd.read_csv(txt_file, header=None)
        
for filename in filenames:
    extracted_number = extract_number(filename)
    if extracted_number is not None:
        df_textak.loc[df_textak.iloc[:, 1] == extracted_number, -1] = filename

        print(f"Extracted number from '{filename}': {extracted_number}")
    else:
        print(f"No number found in '{filename}'")





# Calculate window based on upper left corner and size
  window_x_off = int(math.floor((x_upper_left - geo_transform[0]) / cell_size_x))
  window_y_off = int(math.floor((y_upper_left - geo_transform[3]) / cell_size_y))
  

def split_extent_to_blocks(extent, cell_size_x, cell_size_y, block_size):
  """Splits an extent into blocks and returns a dictionary of block information.

  Args:
      extent: A list of extent coordinates in meters as [xmin, xmax, ymin, ymax].
      cell_size_x: The size of each cell in x direction in meters (positive value).
      cell_size_y: The size of each cell in y direction in meters (negative value).
      block_size: The size of each block in both x and y directions in meters.

  Returns:
      A dictionary where keys are tuples of block upper left corner coordinates
      (x, y) in meters, and values are lists of number of cells in x and y directions.
  """

  xmin, xmax, ymin, ymax = extent
  num_cells_x = int((xmax - xmin) / cell_size_x) + 1
  num_cells_y = int((ymax - ymin) / abs(cell_size_y)) + 1  # Use abs for positive count

  blocks = {}
  block_rows = int(num_cells_y / block_size) + 1
  block_cols = int(num_cells_x / block_size) + 1

  for y_block in range(block_rows):
    for x_block in range(block_cols):
      block_xmin = xmin + x_block * block_size * cell_size_x
      block_xmax = min(xmin + (x_block + 1) * block_size * cell_size_x, xmax)

      # Adjust for negative cell_size_y
      block_ymin = ymax - (y_block + 1) * block_size * abs(cell_size_y)
      block_ymax = max(ymax - y_block * block_size * abs(cell_size_y), ymin)

      block_cells_x = int((block_xmax - block_xmin) / cell_size_x)
      block_cells_y = int((block_ymax - block_ymin) / abs(cell_size_y))

      blocks[(block_xmin, block_ymin)] = [block_cells_x, block_cells_y]

  return blocks


# Example usage
extent = [0, 100, 0, 100]  # [xmin, xmax, ymin, ymax]
cell_size = (10, 10)  # Cell size in meters (in x and y directions)
block_size = 30  # Block size in meters (for both x and y directions)




VAR2

def split_extent_to_blocks(extent, cell_size, block_size):
    xmin, xmax, ymin, ymax = extent
    block_x_size = block_y_size = block_size
    cell_x_size, cell_y_size = cell_size
    
    blocks = {}
    current_y = ymin
    
    while current_y < ymax:
        current_x = xmin
        y_block_size = min(block_y_size, ymax - current_y)
        
        while current_x < xmax:
            x_block_size = min(block_x_size, xmax - current_x)
            blocks[(current_x, current_y)] = [x_block_size // cell_x_size, -y_block_size // cell_y_size]  # Negating y_block_size for downwards y-axis
            current_x += block_x_size
            
        current_y += block_y_size
        
    return blocks

# Example usage
extent = [0, 100, 0, -100]  # [xmin, xmax, ymin, ymax] where ymin is negative to account for downwards y-axis
cell_size = (10, 10)  # Cell size in meters (in x and y directions)
block_size = 30  # Block size in meters (for both x and y directions)

blocks = split_extent_to_blocks(extent, cell_size, block_size)
print(blocks)

x_min, y_min, x_max, y_max = extent

  # Iterate through the extent row by row.
  for y in range(y_min, y_max, block_size):
    # Calculate how many cells fit in the remaining extent.
    num_cells_in_row = int(math.ceil((x_max - x_min) / block_size))

    # Iterate through the row column by column.
    for x in range(x_min, x_max, block_size):
      # Adjust block size if it doesn't fit in the remaining extent.
      if x + block_size > x_max:
        actual_block_size = x_max - x
      else:
        actual_block_size = block_size

      # Add block to the dictionary.
      blocks[(x, y)] = (num_cells_in_row, actual_block_size)

  return blocks

