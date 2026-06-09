class Material:
    def __init__(self, ambient=0.2, specular=0.5, shininess=32.0):
        self.ambient = ambient
        self.specular = specular
        self.shininess = shininess

    def apply(self, shader):
        shader.set_float("ambientStrength", self.ambient)
        shader.set_float("specularStrength", self.specular)
        shader.set_float("shininess", self.shininess)
