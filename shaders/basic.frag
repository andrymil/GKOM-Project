#version 330 core
in vec3 FragPos;
in vec3 Normal;
in vec2 TexCoord;

out vec4 color;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 objectColor;
uniform vec3 lightColor;
uniform sampler2D objectTexture;
uniform bool useTexture;
uniform bool useColorKey;
uniform vec3 colorKey;

void main() {

  float ambientStrength = 0.2;
  vec3 ambient = ambientStrength * lightColor;

  vec3 norm = normalize(Normal);
  vec3 lightDir = normalize(lightPos - FragPos);
  float diff = max(dot(norm, lightDir), 0.0);
  vec3 diffuse = diff * lightColor;

  float specularStrength = 0.5;
  vec3 viewDir = normalize(viewPos - FragPos);
  vec3 reflectDir = reflect(-lightDir, norm);

  float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
  vec3 specular = specularStrength * spec * lightColor;

  vec3 baseColor = objectColor;
  if (useTexture) {
    vec3 texColor = texture(objectTexture, TexCoord).rgb;
    if (useColorKey && distance(texColor, colorKey) < 0.02) {
      discard;
    }
    baseColor *= texColor;
  }

  vec3 result = (ambient + diffuse + specular) * baseColor;
  color = vec4(result, 1.0);
}
