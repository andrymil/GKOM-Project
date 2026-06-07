import os
import numpy as np
from OpenGL.GL import *


class Texture2D:
    def __init__(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Texture not found: {path}")

        self.id = glGenTextures(1)
        width, height, image = self._load_ppm(path)

        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGB,
            width,
            height,
            0,
            GL_RGB,
            GL_UNSIGNED_BYTE,
            image,
        )
        glGenerateMipmap(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glBindTexture(GL_TEXTURE_2D, 0)

    def _load_ppm(self, path):
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
        values = np.array([int(value) for value in tokens[4:]], dtype=np.uint8)
        if len(values) != expected:
            raise ValueError(f"Incomplete pixel data in '{path}'.")

        image = np.flipud(values.reshape((height, width, 3)))
        return width, height, image

    def bind(self, unit=0):
        glActiveTexture(GL_TEXTURE0 + unit)
        glBindTexture(GL_TEXTURE_2D, self.id)
