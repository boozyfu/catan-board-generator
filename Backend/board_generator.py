import random
from PIL import Image, ImageDraw
import math
import streamlit as st
#initialize
row_lengths = [3, 4, 5, 4, 3]
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
    for row_len in row_lengths:
        board.append(tiles[i : i + row_len])
        i += row_len
    return board

@st.cache_data
def load_board_images(tile_size=120):
    images = {}
    # Convert list to tuple for hashability
    image_files = st.session_state["image_files"]
    for file in image_files:
        name = file.split("/")[-1].replace(".png", "")
        images[name] = (
            Image.open(file)
            .convert("RGBA")
            .resize((tile_size, tile_size))
        )
    return images


def create_catan_board(resource_dict, game_type, tile_size=150):
    """
    Create a Catan-style board from a list of PIL images.

    Args:
   ge] - terrain images
        tile_size: width/height of each hex tile

    Returns:
        PIL.Image.Image containing the assembled board
    """
    tp_numbers = []
    fp_numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    
    def generate_numbers(game_type):
        num_list_lookup = {"fp": fp_numbers,
                     "tp": tp_numbers}
        num_list = num_list_lookup[game_type]
  
        random.shuffle(num_list)

        return num_list
  
    static_images = load_board_images()

    image_board = generate_board(resource_dict)

    num_list = generate_numbers(game_type)

    hex_list = [img for row in image_board for img in row]

    desert_idx = hex_list.index("desert")
  
    num_list.insert(desert_idx, None)
    hexes = [static_images.get(img) for img in hex_list]
    number_tiles = [num_list[idx] for idx, _ in enumerate(hex_list)]
    
    rows = [3, 4, 5, 4, 3]

    # spacing for flat-top hexes
    dx = tile_size * 0.75
    dy = tile_size * 0.86

    board_width = int(dx * 5 + tile_size)
    board_height = int(dy * 5 + tile_size)

    board = Image.new(
        "RGBA",
        (board_width, board_height),
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(board)

    index = 0

    for col, count in enumerate(rows):
        # center shorter rows
        y_offset = abs(2-col) * (dy / 2)

        for row in range(count):
            x = int(col * dx)
            y = int(row * dy + y_offset)

            board.alpha_composite(
                hexes[index],
                (x, y)
            )
            number = number_tiles[index]
            cx = x + tile_size // 2
            cy = y + tile_size // 2
            r = tile_size // 7
            draw.ellipse(
                (cx-r, cy-r, cx+r, cy+r),
                fill="white",
                outline="black",
                width=2)

            
            color = "red" if number in (6, 8) else "black"

            text = str(number)
            bbox = draw.textbbox((0, 0), text)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]

            draw.text(
                (cx - tw/2, cy - th/2),
                text,
                fill=color
            )
        
            index += 1

    return board


def create_catan_board_svg(resource_dict, game_type, tile_size=150, font_size=16):
    """
    Create a Catan-style board as SVG with adjustable font size.

    Args:
        resource_dict: Dictionary of terrain resources
        game_type: "fp" or "tp" for game type
        tile_size: width/height of each hex tile
        font_size: Size of the numbers (in pixels/points)

    Returns:
        SVG string that can be displayed with st.write(..., unsafe_allow_html=True)
    """
    tp_numbers = []
    fp_numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    
    def generate_numbers(game_type):
        num_list_lookup = {"fp": fp_numbers, "tp": tp_numbers}
        num_list = num_list_lookup[game_type]
        random.shuffle(num_list)
        return num_list
  
    image_board = generate_board(resource_dict)
    num_list = generate_numbers(game_type)
    
    hex_list = [img for row in image_board for img in row]
    desert_idx = hex_list.index("desert")
    num_list.insert(desert_idx, None)
    
    # Get image file paths from session state
    image_files = st.session_state.get("image_files", {})
    image_lookup = {file.split("/")[-1].replace(".png", ""): file for file in image_files}
    
    number_tiles = [num_list[idx] for idx, _ in enumerate(hex_list)]
    rows = [3, 4, 5, 4, 3]

    # Spacing for flat-top hexes
    dx = tile_size * 0.75
    dy = tile_size * 0.86

    board_width = int(dx * 5 + tile_size)
    board_height = int(dy * 5 + tile_size)

    # Start SVG
    svg_lines = [
        f'<svg width="{board_width}" height="{board_height}" xmlns="http://www.w3.org/2000/svg">'
    ]

    index = 0

    for col, count in enumerate(rows):
        # Center shorter rows
        y_offset = abs(2 - col) * (dy / 2)

        for row in range(count):
            x = int(col * dx)
            y = int(row * dy + y_offset)

            # Add hex tile image
            resource = hex_list[index]
            image_path = image_lookup.get(resource)
            if image_path:
                svg_lines.append(
                    f'  <image x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" href="{image_path}" />'
                )

            number = number_tiles[index]
            if number is not None:
                cx = x + tile_size // 2
                cy = y + tile_size // 2
                r = int(tile_size // 7)

                # Circle background
                svg_lines.append(
                    f'  <circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="black" stroke-width="2" />'
                )

                # Number text
                color = "red" if number in (6, 8) else "black"
                svg_lines.append(
                    f'  <text x="{cx}" y="{cy}" font-size="{font_size}" font-weight="bold" '
                    f'text-anchor="middle" dominant-baseline="middle" fill="{color}">{number}</text>'
                )

            index += 1

    svg_lines.append('</svg>')
    
    return '\n'.join(svg_lines)
