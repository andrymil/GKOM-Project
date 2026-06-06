import os
import numpy as np
import ctypes
from OpenGL.GL import *


class Skybox:
    CUBE_VERTICES = np.array(
        [
            -1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0, 1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, 1.0,
            -1.0, -1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, 1.0, -1.0,
            -1.0, 1.0, 1.0,
            -1.0, -1.0, 1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            -1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            1.0, -1.0, 1.0,
            -1.0, -1.0, 1.0,
            -1.0, 1.0, -1.0,
            1.0, 1.0, -1.0,
            1.0, 1.0, 1.0,
            1.0, 1.0, 1.0,
            -1.0, 1.0, 1.0,
            -1.0, 1.0, -1.0,
            -1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            -1.0, -1.0, 1.0,
            1.0, -1.0, 1.0,
        ],
        dtype=np.float32,
    )

    def __init__(self, face_paths):
        if len(face_paths) != 6:
            raise ValueError("Skybox needs exactly 6 texture paths.")

        self.texture_id = self._load_cubemap(face_paths)
        self.vao, self.vbo = self._create_cube_mesh()

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
        if max_value != 255:
            raise ValueError(f"Unsupported max value in '{path}': {max_value}")

        if magic == b"P3":
            expected = width * height * 3
            values = np.array([int(value) for value in tokens[4:]], dtype=np.uint8)
            if len(values) != expected:
                raise ValueError(f"Incomplete pixel data in '{path}'.")
            image = values.reshape((height, width, 3))
            return width, height, image

        raise ValueError(f"Unsupported PPM format in '{path}'. Use P3.")

    def _load_cubemap(self, face_paths):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, texture_id)

        for index, path in enumerate(face_paths):
            if not os.path.exists(path):
                raise FileNotFoundError(f"Skybox face not found: {path}")

            width, height, image = self._load_ppm(path)
            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + index,
                0,
                GL_RGB,
                width,
                height,
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                image,
            )

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)

        return texture_id

    def _create_cube_mesh(self):
        vao = glGenVertexArrays(1)
        vbo = glGenBuffers(1)

        glBindVertexArray(vao)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(
            GL_ARRAY_BUFFER,
            self.CUBE_VERTICES.nbytes,
            self.CUBE_VERTICES,
            GL_STATIC_DRAW,
        )

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 3 * self.CUBE_VERTICES.itemsize, ctypes.c_void_p(0)
        )

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        return vao, vbo

    def draw(self):
        glDepthFunc(GL_LEQUAL)
        glDepthMask(GL_FALSE)
        glBindVertexArray(self.vao)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture_id)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        glBindVertexArray(0)
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
