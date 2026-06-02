import glfw
import glm
from OpenGL.GL import *

from src.window import Window
from src.shader import ShaderProgram
from src.model import Model
from src.camera import Camera
from src.skybox import Skybox


class Application:
    def __init__(self, scene_mode="trees"):
        if scene_mode not in ("trees", "clouds"):
            raise ValueError("Scene mode must be 'trees' or 'clouds'.")

        self.scene_mode = scene_mode
        self.window = Window(800, 600, f"GKOM - Billboarding ({scene_mode})")

        self.camera = Camera((0.0, 1.0, 7.0))
        self.last_x = 400
        self.last_y = 300
        self.first_mouse = True
        self.billboards_paused = False
        self.r_was_pressed = False
        self.frozen_camera_position = glm.vec3(self.camera.position)

        glfw.set_cursor_pos_callback(self.window.window, self.mouse_callback)

        self.shader = ShaderProgram("shaders/basic.vert", "shaders/basic.frag")
        self.skybox_shader = ShaderProgram("shaders/skybox.vert", "shaders/skybox.frag")
        self.billboard_model = Model("models/billboard.obj")

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

        self.tree_positions = [
            glm.vec3(-4.0, 0.0, -3.0),
            glm.vec3(-2.0, 0.0, -5.0),
            glm.vec3(1.5, 0.0, -4.5),
            glm.vec3(4.0, 0.0, -2.8),
        ]
        self.cloud_positions = [
            glm.vec3(-3.5, 3.0, -4.0),
            glm.vec3(-1.0, 3.6, -6.0),
            glm.vec3(1.8, 2.8, -4.8),
            glm.vec3(4.2, 3.2, -5.6),
        ]

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
            self.billboards_paused = not self.billboards_paused
            if self.billboards_paused:
                self.frozen_camera_position = glm.vec3(self.camera.position)
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

    def _build_billboard_matrix(self, position, right, up, forward, scale_x, scale_y):
        model_matrix = glm.mat4(1.0)
        model_matrix[0] = glm.vec4(right * scale_x, 0.0)
        model_matrix[1] = glm.vec4(up * scale_y, 0.0)
        model_matrix[2] = glm.vec4(forward, 0.0)
        model_matrix[3] = glm.vec4(position, 1.0)
        return model_matrix

    def _get_billboard_camera_position(self):
        if self.billboards_paused:
            return self.frozen_camera_position
        return self.camera.position

    def _axial_billboard_matrix(self, position, scale_x, scale_y):
        to_camera = self._get_billboard_camera_position() - position
        forward = glm.vec3(to_camera.x, 0.0, to_camera.z)

        if glm.length(forward) < 0.0001:
            forward = glm.vec3(0.0, 0.0, 1.0)
        else:
            forward = glm.normalize(forward)

        up = glm.vec3(0.0, 1.0, 0.0)
        right = glm.normalize(glm.cross(up, forward))
        return self._build_billboard_matrix(position, right, up, forward, scale_x, scale_y)

    def _world_oriented_billboard_matrix(self, position, scale_x, scale_y):
        to_camera = self._get_billboard_camera_position() - position

        if glm.length(to_camera) < 0.0001:
            to_camera = glm.vec3(0.0, 0.0, 1.0)
        else:
            to_camera = glm.normalize(to_camera)

        world_up = glm.vec3(0.0, 1.0, 0.0)
        right = glm.cross(world_up, to_camera)
        if glm.length(right) < 0.0001:
            right = glm.vec3(1.0, 0.0, 0.0)
        else:
            right = glm.normalize(right)

        up = glm.normalize(glm.cross(to_camera, right))
        return self._build_billboard_matrix(position, right, up, to_camera, scale_x, scale_y)

    def render_billboard(self, position, color, scale_x, scale_y, mode):
        if mode == "axial":
            model_matrix = self._axial_billboard_matrix(position, scale_x, scale_y)
        else:
            model_matrix = self._world_oriented_billboard_matrix(position, scale_x, scale_y)

        self.shader.set_mat4("model", model_matrix)
        self.shader.set_vec3("objectColor", color)
        self.billboard_model.draw()

    def render_billboard_scene(self):
        if self.scene_mode == "trees":
            for position in self.tree_positions:
                self.render_billboard(
                    position=position,
                    color=glm.vec3(0.2, 0.7, 0.2),
                    scale_x=1.2,
                    scale_y=2.6,
                    mode="axial",
                )
        else:
            for position in self.cloud_positions:
                self.render_billboard(
                    position=position,
                    color=glm.vec3(0.9, 0.9, 0.95),
                    scale_x=2.8,
                    scale_y=1.4,
                    mode="world",
                )

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

            self.render_billboard_scene()

            self.skybox_shader.use()
            skybox_view = glm.mat4(glm.mat3(self.camera.get_view_matrix()))
            self.skybox_shader.set_mat4("view", skybox_view)
            self.skybox_shader.set_mat4("projection", projection)
            glUniform1i(glGetUniformLocation(self.skybox_shader.id, "skybox"), 0)
            self.skybox.draw()

            self.window.update()

        self.window.terminate()
