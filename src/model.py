import os
import numpy as np
from OpenGL.GL import *


class Model:
    def __init__(self, filepath):
        self.vertices = []
        self.vao = 0
        self.vbo = 0
        self.vertex_count = 0

        self._load_obj(filepath)
        self._setup_mesh()

    def _load_obj(self, filepath):
        if not os.path.exists(filepath):
            print(f"Error: Could not find file '{filepath}'")
            return

        temp_vertices = []
        final_vertices = []

        print(f"Loading model: {filepath}...")

        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("v "):
                    parts = line.split()

                    temp_vertices.append(
                        (float(parts[1]), float(parts[2]), float(parts[3]))
                    )

                elif line.startswith("f "):
                    parts = line.split()
                    for i in range(1, 4):
                        idx = int(parts[i].split("/")[0]) - 1
                        final_vertices.extend(temp_vertices[idx])

        self.vertices = np.array(final_vertices, dtype=np.float32)
        self.vertex_count = len(self.vertices) // 3
        print(f"Model loaded successfully. Vertices count: {self.vertex_count}")

    def _setup_mesh(self):
        if len(self.vertices) == 0:
            return

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(
            GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW
        )

        glVertexAttribPointer(
            0, 3, GL_FLOAT, GL_FALSE, 3 * self.vertices.itemsize, ctypes.c_void_p(0)
        )
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        if self.vao != 0:
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
            glBindVertexArray(0)
