import glfw
import glm
from OpenGL.GL import *

from src.window import Window
from src.shader import ShaderProgram
from src.model import Model
from src.camera import Camera


class Application:
    def __init__(self):
        self.window = Window(800, 600, "GKOM - Billboarding")

        self.camera = Camera((0.0, 1.0, 7.0))
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True

        glfw.set_cursor_pos_callback(self.window.window, self.mouse_callback)

        self.shader = ShaderProgram("shaders/basic.vert", "shaders/basic.frag")
        self.tree_model = Model("models/tree_cone.obj")
        self.cube_model = Model("models/cube.obj")
        self.sphere_model = Model("models/sphere.obj")

    def mouse_callback(self, window, xpos, ypos):
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False

        xoffset = xpos - self.last_x
        yoffset = self.last_y - ypos

        self.last_x = xpos
        self.last_y = ypos

        self.camera.process_mouse(xoffset, yoffset)

    def process_input(self, dt):
        if self.window.is_key_pressed(glfw.KEY_ESCAPE):
            glfw.set_window_should_close(self.window.window, True)

        if self.window.is_key_pressed(glfw.KEY_W):
            self.camera.process_keyboard("FORWARD", dt)
        if self.window.is_key_pressed(glfw.KEY_S):
            self.camera.process_keyboard("BACKWARD", dt)
        if self.window.is_key_pressed(glfw.KEY_A):
            self.camera.process_keyboard("LEFT", dt)
        if self.window.is_key_pressed(glfw.KEY_D):
            self.camera.process_keyboard("RIGHT", dt)
        if self.window.is_key_pressed(glfw.KEY_SPACE):
            self.camera.process_keyboard("UP", dt)
        if self.window.is_key_pressed(glfw.KEY_LEFT_SHIFT):
            self.camera.process_keyboard("DOWN", dt)

    def render_object(
        self,
        model,
        position,
        color,
        rotation_angle=0.0,
        rotation_axis=glm.vec3(0, 1, 0),
    ):
        model_matrix = glm.mat4(1.0)
        model_matrix = glm.translate(model_matrix, position)

        if rotation_angle != 0.0:
            model_matrix = glm.rotate(model_matrix, rotation_angle, rotation_axis)

        self.shader.set_mat4("model", model_matrix)
        self.shader.set_vec3("objectColor", color)
        model.draw()

    def run(self):
        while self.window.is_running():
            dt = self.window.update_delta_time()
            self.process_input(dt)

            self.window.clear()

            self.shader.use()

            projection = glm.perspective(
                glm.radians(45.0), self.window.get_aspect_ratio(), 0.1, 100.0
            )
            self.shader.set_mat4("projection", projection)
            self.shader.set_mat4("view", self.camera.get_view_matrix())

            self.shader.set_vec3("lightPos", glm.vec3(0.0, 5.0, 2.0))
            self.shader.set_vec3("viewPos", self.camera.position)
            self.shader.set_vec3("lightColor", glm.vec3(1.0, 1.0, 1.0))

            time_val = glfw.get_time()

            self.render_object(
                self.tree_model,
                glm.vec3(-2.5, 0.0, 0.0),
                glm.vec3(0.2, 0.8, 0.2),
                time_val,
            )
            self.render_object(
                self.sphere_model, glm.vec3(0.0, 0.0, 0.0), glm.vec3(0.2, 0.5, 0.9)
            )
            self.render_object(
                self.cube_model,
                glm.vec3(2.5, 0.0, 0.0),
                glm.vec3(0.8, 0.2, 0.2),
                time_val * 0.8,
                glm.vec3(1.0, 1.0, 0.0),
            )

            self.window.update()

        self.window.terminate()
