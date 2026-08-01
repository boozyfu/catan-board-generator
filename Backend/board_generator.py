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

CATAN_COORDS = [
    (-4,  2), (-4,  0), (-4, -2),
    (-2,  3), (-2,  1), (-2, -1), (-2, -3),
    ( 0,  4), ( 0,  2), ( 0,  0), ( 0, -2), ( 0, -4),
    ( 2,  3), ( 2,  1), ( 2, -1), ( 2, -3),
    ( 4,  2), ( 4,  0), ( 4, -2),
]


def load_board_images(tile_size):
    size = tile_size // 2
    img_w = int(2 * size)
    img_h = int(2 * size * math.sin(math.pi / 3))

    images = {}

    for file in st.session_state["image_files"]:
        name = file.split("/")[-1].replace(".png", "")
        img = Image.open(file).convert("RGBA")
        img = img.resize((img_w, img_h), Image.Resampling.LANCZOS)
        images[name] = img

    return images


def render_board(resources, images, tile_size=120):
    size = tile_size / 2

    dx = size * (1 + math.cos(math.pi / 3))
    dy = size * math.sin(math.pi / 3)

    img_w = int(2 * size)
    img_h = int(2 * dy)

    xs = [c[0] for c in CATAN_COORDS]
    ys = [c[1] for c in CATAN_COORDS]

    margin = tile_size

    canvas_w = int((max(xs) - min(xs)) * dx + img_w + 2 * margin)
    canvas_h = int((max(ys) - min(ys)) * dy + img_h + 2 * margin)

    canvas = Image.new("RGBA", (canvas_w, canvas_h), (255, 255, 255, 0))

    center_x = canvas_w / 2
    center_y = canvas_h / 2

    for resource, (gx, gy) in zip(resources, CATAN_COORDS):
        if resource not in images:
            continue

        img = images[resource]

        cx = center_x + gx * dx
        cy = center_y + gy * dy

        canvas.paste(
            img,
            (
                int(cx - size),
                int(cy - dy),
            ),
            img,
        )

    return canvas

