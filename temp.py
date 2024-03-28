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
            blocks[(current_x, current_y)] = [x_block_size // cell_x_size, y_block_size // cell_y_size]
            current_x += block_x_size
            
        current_y += block_y_size
        
    return blocks

# Example usage
extent = [0, 100, 0, 100]  # [xmin, xmax, ymin, ymax]
cell_size = (10, 10)  # Cell size in meters (in x and y directions)
block_size = 30  # Block size in meters (for both x and y directions)




VAR2

def split_extent_to_blocks(extent, cell_size, block_size):
   """Splits an extent into blocks and returns a dictionary of block information.

   Args:
       extent: A list of extent coordinates in meters as [xmin, xmax, ymin, ymax].
       cell_size: The size of each cell in meters.
       block_size: The size of each block in both x and y directions in meters.

   Returns:
       A dictionary where keys are tuples of block upper left corner coordinates
       (x, y) in meters, and values are lists of number of cells in x and y directions.
   """

   xmin, xmax, ymin, ymax = extent
   num_cells_x = int((xmax - xmin) / cell_size) + 1
   num_cells_y = int((ymax - ymin) / cell_size) + 1

   blocks = {}
   block_rows = int(num_cells_y / block_size) + 1
   block_cols = int(num_cells_x / block_size) + 1

   for y_block in range(block_rows):
       for x_block in range(block_cols):
           block_xmin = xmin + x_block * block_size * cell_size
           block_xmax = min(xmin + (x_block + 1) * block_size * cell_size, xmax)
           block_ymin = ymin + y_block * block_size * cell_size
           block_ymax = min(ymin + (y_block + 1) * block_size * cell_size, ymax)

           block_cells_x = int((block_xmax - block_xmin) / cell_size)
           block_cells_y = int((block_ymax - block_ymin) / cell_size)

           blocks[(block_xmin, block_ymin)] = [block_cells_x, block_cells_y]

   return blocks
