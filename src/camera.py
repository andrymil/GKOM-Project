import glm
import math


class Camera:
    def __init__(self, position):
        self.position = glm.vec3(position)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)

        self.yaw = -90.0
        self.pitch = 0.0

        self.speed = 3.5
        self.sensitivity = 0.1

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_keyboard(self, direction, delta_time):
        velocity = self.speed * delta_time
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":

            self.position -= glm.normalize(glm.cross(self.front, self.up)) * velocity
        if direction == "RIGHT":
            self.position += glm.normalize(glm.cross(self.front, self.up)) * velocity
        if direction == "UP":
            self.position += self.up * velocity
        if direction == "DOWN":
            self.position -= self.up * velocity

    def process_mouse(self, xoffset, yoffset):
        xoffset *= self.sensitivity
        yoffset *= self.sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        new_front = glm.vec3()
        new_front.x = math.cos(glm.radians(self.yaw)) * math.cos(
            glm.radians(self.pitch)
        )
        new_front.y = math.sin(glm.radians(self.pitch))
        new_front.z = math.sin(glm.radians(self.yaw)) * math.cos(
            glm.radians(self.pitch)
        )
        self.front = glm.normalize(new_front)
