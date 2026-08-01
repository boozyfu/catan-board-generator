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
            .rotate(30, expand=False)
        )
    return images


def create_catan_board(resource_dict, tile_size=150):
    """
    Create a Catan-style board from a list of PIL images.

    Args:
   ge] - terrain images
        tile_size: width/height of each hex tile

    Returns:
        PIL.Image.Image containing the assembled board
    """
    static_images = load_board_images()

    image_board = generate_board(resource_dict)

    images = [static_images.get(img) for row in image_board for img in row]

    def hex_mask(size):
        """Create a flat-top hexagon mask."""
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)

        points = [
            (size * 0.25, 0),
            (size * 0.75, 0),
            (size, size * 0.5),
            (size * 0.75, size),
            (size * 0.25, size),
            (0, size * 0.5),
        ]

        draw.polygon(points, fill=255)
        return mask

    def make_hex(image):
        """Resize image and crop into a hex."""
        image = image.convert("RGB")
        image = image.resize((tile_size, tile_size))
        return image

    rows = [3, 4, 5, 4, 3]

    hexes = [make_hex(img) for img in images]

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

    index = 0

    for row, count in enumerate(rows):
        # center shorter rows
        x_offset = (5 - count) * dx / 2

        for col in range(count):
            x = int(x_offset + col * dx)
            y = int(row * dy)

            board.alpha_composite(
                hexes[index],
                (x, y)
            )

            index += 1

    return board
