import numpy as np


def load_ppm(path: str, flip: bool = False):
    with open(path, "rb") as f:
        raw = f.read()

    tokens = []
    for line in raw.splitlines():
        if b"#" in line:
            line = line[: line.index(b"#")]
        line = line.strip()
        if line:
            tokens.extend(line.split())

    if len(tokens) < 4:
        raise ValueError(f"Invalid PPM file: '{path}'")

    magic = tokens[0]
    width = int(tokens[1])
    height = int(tokens[2])
    max_value = int(tokens[3])

    if magic != b"P3":
        raise ValueError(f"Unsupported PPM format in '{path}'. Use P3.")
    if max_value != 255:
        raise ValueError(f"Unsupported max value in '{path}': {max_value}")

    expected = width * height * 3
    values = np.array([int(v) for v in tokens[4:]], dtype=np.uint8)
    if len(values) != expected:
        raise ValueError(f"Incomplete pixel data in '{path}'.")

    image = values.reshape((height, width, 3))
    if flip:
        image = np.flipud(image)

    return width, height, image
