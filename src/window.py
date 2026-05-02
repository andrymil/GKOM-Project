import glfw
from OpenGL.GL import *


class Window:
    def __init__(self, width, height, title):
        if not glfw.init():
            raise Exception("GLFW Initialization failed")

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Window creation failed")

        glfw.make_context_current(self.window)
        glEnable(GL_DEPTH_TEST)

    def is_running(self):
        return not glfw.window_should_close(self.window)

    def clear(self):
        glClearColor(0.2, 0.3, 0.4, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def update(self):
        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def get_time(self):
        return glfw.get_time()

    def get_aspect_ratio(self):
        width, height = glfw.get_framebuffer_size(self.window)
        if height == 0:
            height = 1
        return width / height

    def terminate(self):
        glfw.terminate()
