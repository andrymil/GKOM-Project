import glfw
import glm
from OpenGL.GL import *

from src.window import Window
from src.shader import ShaderProgram
from src.model import Model
from src.camera import Camera
from src.skybox import Skybox


class Application:
    def __init__(self):
        self.window = Window(800, 600, "GKOM - Billboarding")

        self.camera = Camera((0.0, 1.0, 7.0))
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.planes_rotation_paused = False
        self.r_was_pressed = False
        self.planes_rotation_offset = 0.0
        self.planes_pause_started_at = 0.0

        glfw.set_cursor_pos_callback(self.window.window, self.mouse_callback)

        self.shader = ShaderProgram("shaders/basic.vert", "shaders/basic.frag")
        self.skybox_shader = ShaderProgram("shaders/skybox.vert", "shaders/skybox.frag")
        self.shoe_model = Model("models/shoe.obj")
        self.cube_model = Model("models/cube.obj")
        self.sphere_model = Model("models/sphere.obj")
        self.plane_model = Model("models/plane.obj")

        self.skybox = Skybox(
            [
                "textures/skybox/right.ppm",
                "textures/skybox/left.ppm",
                "textures/skybox/top.ppm",
                "textures/skybox/bottom.ppm",
                "textures/skybox/front.ppm",
                "textures/skybox/back.ppm",
            ]
        )

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

        r_is_pressed = self.window.is_key_pressed(glfw.KEY_R)
        if r_is_pressed and not self.r_was_pressed:
            current_time = glfw.get_time()
            if not self.planes_rotation_paused:
                self.planes_rotation_paused = True
                self.planes_pause_started_at = current_time
            else:
                paused_duration = current_time - self.planes_pause_started_at
                self.planes_rotation_offset += paused_duration
                self.planes_rotation_paused = False
        self.r_was_pressed = r_is_pressed

    def render_object(
        self,
        model,
        position,
        color,
        scale=1.0,
        fix_angle=0.0,
        fix_axis=glm.vec3(1, 0, 0),
        anim_angle=0.0,
        anim_axis=glm.vec3(0, 1, 0),
    ):
        model_matrix = glm.mat4(1.0)

        model_matrix = glm.translate(model_matrix, position)

        if anim_angle != 0.0:
            model_matrix = glm.rotate(model_matrix, anim_angle, anim_axis)

        if fix_angle != 0.0:
            model_matrix = glm.rotate(model_matrix, fix_angle, fix_axis)

        if scale != 1.0:
            model_matrix = glm.scale(model_matrix, glm.vec3(scale))

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
                model=self.shoe_model,
                position=glm.vec3(-2.5, 0.0, 0.0),
                color=glm.vec3(0.2, 0.8, 0.2),
                scale=0.3,
                fix_angle=glm.radians(-90.0),
                fix_axis=glm.vec3(1.0, 0.0, 0.0),
                anim_angle=time_val,
                anim_axis=glm.vec3(0, 1, 0),
            )
            self.render_object(
                model=self.sphere_model,
                position=glm.vec3(0.0, 0.0, 0.0),
                color=glm.vec3(0.2, 0.5, 0.9),
            )
            self.render_object(
                model=self.cube_model,
                position=glm.vec3(2.5, 0.0, 0.0),
                color=glm.vec3(0.8, 0.2, 0.2),
                anim_angle=time_val * 0.8,
                anim_axis=glm.vec3(1.0, 1.0, 0.0),
            )
            if self.planes_rotation_paused:
                plane_time = self.planes_pause_started_at - self.planes_rotation_offset
            else:
                plane_time = time_val - self.planes_rotation_offset

            self.render_object(
                model=self.plane_model,
                position=glm.vec3(-4.2, -0.8, -2.8),
                color=glm.vec3(0.9, 0.9, 0.9),
                scale=2.2,
                anim_angle=plane_time * 0.45,
                anim_axis=glm.vec3(0.0, 1.0, 0.0),
            )
            self.render_object(
                model=self.plane_model,
                position=glm.vec3(4.2, 1.7, -3.2),
                color=glm.vec3(0.9, 0.9, 0.9),
                scale=1.8,
                fix_angle=glm.radians(90.0),
                fix_axis=glm.vec3(1.0, 0.0, 0.0),
                anim_angle=plane_time * 0.35,
                anim_axis=glm.vec3(0.0, 0.0, 1.0),
            )

            self.skybox_shader.use()
            skybox_view = glm.mat4(glm.mat3(self.camera.get_view_matrix()))
            self.skybox_shader.set_mat4("view", skybox_view)
            self.skybox_shader.set_mat4("projection", projection)
            glUniform1i(glGetUniformLocation(self.skybox_shader.id, "skybox"), 0)
            self.skybox.draw()

            self.window.update()

        self.window.terminate()
