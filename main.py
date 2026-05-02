import numpy as np
import glm
from OpenGL.GL import *

from src.window import Window
from src.shader import ShaderProgram
from src.model import Model


def main():
    app_window = Window(800, 600, "GKOM - Billboarding (Phase 1)")

    shader = ShaderProgram("shaders/basic.vert", "shaders/basic.frag")
    my_model = Model("models/test_model.obj")

    while app_window.is_running():
        app_window.clear()

        projection = glm.perspective(
            glm.radians(45.0), app_window.get_aspect_ratio(), 0.1, 100.0
        )

        camera_pos = glm.vec3(0.0, 0.0, -5.0)
        view = glm.translate(glm.mat4(1.0), camera_pos)

        model_matrix = glm.mat4(1.0)
        model_matrix = glm.rotate(
            model_matrix, float(app_window.get_time()), glm.vec3(0.0, 1.0, 0.0)
        )

        shader.use()

        light_position = glm.vec3(2.0, 5.0, 2.0)

        shader.set_vec3("lightPos", light_position)
        shader.set_vec3("viewPos", glm.vec3(0.0, 0.0, 5.0))
        shader.set_vec3("lightColor", glm.vec3(1.0, 1.0, 1.0))
        shader.set_vec3("objectColor", glm.vec3(0.2, 0.8, 0.2))

        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)
        shader.set_mat4("model", model_matrix)

        my_model.draw()

        app_window.update()

    app_window.terminate()


if __name__ == "__main__":
    main()
