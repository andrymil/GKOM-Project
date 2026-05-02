import numpy as np
import glm
from OpenGL.GL import *

from src.window import Window
from src.shader import ShaderProgram


def main():
    app_window = Window(800, 600, "GKOM - Billboarding (Etap 1)")

    shader = ShaderProgram("./shaders/basic.vert", "./shaders/basic.frag")

    vertices = np.array(
        [
            0.5,
            0.5,
            0.0,
            0.5,
            -0.5,
            0.0,
            -0.5,
            0.5,
            0.0,
            0.5,
            -0.5,
            0.0,
            -0.5,
            -0.5,
            0.0,
            -0.5,
            0.5,
            0.0,
        ],
        dtype=np.float32,
    )

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(
        0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0)
    )
    glEnableVertexAttribArray(0)

    while app_window.is_running():
        app_window.clear()

        projection = glm.perspective(
            glm.radians(45.0), app_window.get_aspect_ratio(), 0.1, 100.0
        )
        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -3.0))

        model = glm.mat4(1.0)
        model = glm.rotate(model, float(app_window.get_time()), glm.vec3(1.0, 0.0, 0.0))

        shader.use()
        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)
        shader.set_mat4("model", model)

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)

        app_window.update()

    app_window.terminate()


if __name__ == "__main__":
    main()
