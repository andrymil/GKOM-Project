import numpy as np
import glm
from OpenGL.GL import *
import glfw

from src.window import Window
from src.shader import ShaderProgram
from src.model import Model
from src.camera import Camera

last_x = 400
last_y = 300
first_mouse = True
camera = Camera((0.0, 1.0, 5.0))


def mouse_callback(window, xpos, ypos):
    global last_x, last_y, first_mouse

    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos

    last_x = xpos
    last_y = ypos

    camera.process_mouse(xoffset, yoffset)


def process_input(app_window, dt):
    if app_window.is_key_pressed(glfw.KEY_ESCAPE):
        glfw.set_window_should_close(app_window.window, True)

    if app_window.is_key_pressed(glfw.KEY_W):
        camera.process_keyboard("FORWARD", dt)
    if app_window.is_key_pressed(glfw.KEY_S):
        camera.process_keyboard("BACKWARD", dt)
    if app_window.is_key_pressed(glfw.KEY_A):
        camera.process_keyboard("LEFT", dt)
    if app_window.is_key_pressed(glfw.KEY_D):
        camera.process_keyboard("RIGHT", dt)
    if app_window.is_key_pressed(glfw.KEY_SPACE):
        camera.process_keyboard("UP", dt)
    if app_window.is_key_pressed(glfw.KEY_LEFT_SHIFT):
        camera.process_keyboard("DOWN", dt)


def main():
    app_window = Window(800, 600, "GKOM - Billboarding (Phase 1 & 2 Preview)")

    glfw.set_cursor_pos_callback(app_window.window, mouse_callback)

    shader = ShaderProgram("shaders/basic.vert", "shaders/basic.frag")

    tree_model = Model("models/tree_cone.obj")
    cube_model = Model("models/cube.obj")
    sphere_model = Model("models/sphere.obj")

    while app_window.is_running():

        dt = app_window.update_delta_time()

        process_input(app_window, dt)

        app_window.clear()

        projection = glm.perspective(
            glm.radians(45.0), app_window.get_aspect_ratio(), 0.1, 100.0
        )

        view = camera.get_view_matrix()

        shader.use()

        light_position = glm.vec3(0.0, 5.0, 2.0)
        shader.set_vec3("lightPos", light_position)

        shader.set_vec3("viewPos", camera.position)

        shader.set_vec3("lightColor", glm.vec3(1.0, 1.0, 1.0))

        shader.set_mat4("projection", projection)
        shader.set_mat4("view", view)

        model_tree = glm.mat4(1.0)
        model_tree = glm.translate(model_tree, glm.vec3(-2.5, 0.0, 0.0))
        shader.set_mat4("model", model_tree)
        shader.set_vec3("objectColor", glm.vec3(0.2, 0.8, 0.2))
        tree_model.draw()

        model_sphere = glm.mat4(1.0)
        model_sphere = glm.translate(model_sphere, glm.vec3(0.0, 0.0, 0.0))
        shader.set_mat4("model", model_sphere)
        shader.set_vec3("objectColor", glm.vec3(0.2, 0.5, 0.9))
        sphere_model.draw()

        model_cube = glm.mat4(1.0)
        model_cube = glm.translate(model_cube, glm.vec3(2.5, 0.0, 0.0))
        shader.set_mat4("model", model_cube)
        shader.set_vec3("objectColor", glm.vec3(0.8, 0.2, 0.2))
        cube_model.draw()

        app_window.update()

    app_window.terminate()


if __name__ == "__main__":
    main()
