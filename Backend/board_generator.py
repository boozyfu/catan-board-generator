import random
from PIL import Image
import math

#initialize board
ROW_LENGTHS = [3, 4, 5, 4, 3]

fp_resources = {
  "wood": 4,
  "clay": 3,
  "wool": 4,
  "grain": 4,
  "ore": 3,
  "desert": 1}

tp_resources = {
  "wood": 3,
  "clay": 2,
  "wool": 3,
  "grain": 3,
  "ore": 2,
  "desert": 1}

def generate_board(resource_dict):
    tiles = []
    for resource, count in resource_dict.items():
        tiles.extend([resource] * count)
    random.shuffle(tiles)

    board = []
    i = 0
    for row_len in ROW_LENGTHS:
        board.append(tiles[i : i + row_len])
        i += row_len
    return board

def get_hex_spacing(size):
    """Calculate hex grid spacing using proper hexagonal math"""
    dx = size * (1 + math.cos(math.pi / 3)) / 2  # ≈ 0.75 * size
    dy = size * math.sin(math.pi / 3)              # ≈ 0.866 * size
    return dx, dy

def render_board(board, images, tile_size=120):
    """Render the Catan board with proper hexagonal grid math"""
    dx, dy = get_hex_spacing(tile_size)
    
    row_lengths = [len(row) for row in board]
    max_row_len = max(row_lengths)
    
    # Calculate canvas size using hex formulas
    canvas_w = int((max_row_len * dx) + (2 * tile_size))
    canvas_h = int((len(board) + 2) * dy)
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))
    
    for row_idx, row in enumerate(board):
        # Center rows of different lengths
        row_offset = (max_row_len - len(row)) * dx / 2
        y = int(row_idx * dy + tile_size)
        
        for col_idx, resource in enumerate(row):
            x = int(row_offset + col_idx * dx + tile_size)
            
            if resource in images:
                img = images[resource]
                # Center the rotated image within grid position
                offset_x = x - img.width // 2
                offset_y = y - img.height // 2
                canvas.paste(img, (offset_x, offset_y), img)
    
    return canvas
