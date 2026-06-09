from OpenGL.GL import *
import OpenGL.GL.shaders as shaders
import glm


class ShaderProgram:
    def __init__(self, vertex_path, fragment_path):
        self.id = self._compile_from_files(vertex_path, fragment_path)

    def _compile_from_files(self, v_path, f_path):
        with open(v_path, "r") as f:
            vertex_code = f.read()
        with open(f_path, "r") as f:
            fragment_code = f.read()

        vertex = shaders.compileShader(vertex_code, GL_VERTEX_SHADER)
        fragment = shaders.compileShader(fragment_code, GL_FRAGMENT_SHADER)
        return shaders.compileProgram(vertex, fragment)

    def use(self):
        glUseProgram(self.id)

    def set_mat4(self, name, matrix):
        location = glGetUniformLocation(self.id, name)
        glUniformMatrix4fv(location, 1, GL_FALSE, matrix.to_bytes())

    def set_vec3(self, name, vec):
        location = glGetUniformLocation(self.id, name)
        glUniform3fv(location, 1, glm.value_ptr(vec))

    def set_float(self, name, value):
        location = glGetUniformLocation(self.id, name)
        glUniform1f(location, value)
