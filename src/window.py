import glfw
from OpenGL.GL import *


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)


class Window:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create window")

        glfw.make_context_current(self.window)

        fb_width, fb_height = glfw.get_framebuffer_size(self.window)
        glViewport(0, 0, fb_width, fb_height)

        glfw.set_framebuffer_size_callback(self.window, framebuffer_size_callback)

        glEnable(GL_DEPTH_TEST)
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

        self.last_frame_time = 0.0
        self.delta_time = 0.0

    def is_running(self):
        return not glfw.window_should_close(self.window)

    def clear(self):
        glClearColor(0.2, 0.3, 0.4, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def is_key_pressed(self, key):
        return glfw.get_key(self.window, key) == glfw.PRESS

    def update_delta_time(self):
        current_time = glfw.get_time()
        self.delta_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        return self.delta_time

    def get_aspect_ratio(self):
        width, height = glfw.get_framebuffer_size(self.window)
        if height == 0:
            height = 1
        return width / height

    def terminate(self):
        glfw.terminate()
