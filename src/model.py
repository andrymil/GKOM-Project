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
        temp_normals = []
        final_data = []

        print(f"Loading model: {filepath}...")

        with open(filepath, "r") as f:
            for line in f:
                if line.startswith("v "):
                    parts = line.split()
                    temp_vertices.append(
                        (float(parts[1]), float(parts[2]), float(parts[3]))
                    )
                elif line.startswith("vn "):
                    parts = line.split()
                    temp_normals.append(
                        (float(parts[1]), float(parts[2]), float(parts[3]))
                    )
                elif line.startswith("f "):
                    parts = line.split()
                    for i in range(1, 4):
                        v_data = parts[i].split("/")
                        v_idx = int(v_data[0]) - 1

                        vx, vy, vz = temp_vertices[v_idx]

                        nx, ny, nz = 0.0, 1.0, 0.0

                        if len(v_data) >= 3 and v_data[2] != "":
                            n_idx = int(v_data[2]) - 1
                            nx, ny, nz = temp_normals[n_idx]

                        final_data.extend([vx, vy, vz, nx, ny, nz])

        self.vertices = np.array(final_data, dtype=np.float32)

        self.vertex_count = len(self.vertices) // 6
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

        stride = 6 * self.vertices.itemsize

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        if self.vao != 0:
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
            glBindVertexArray(0)
