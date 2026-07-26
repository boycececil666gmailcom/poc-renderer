#version 330 core
out vec4 FragColor;

in vec3 Normal;

void main()
{
    // Map normal directions from [-1, 1] to [0.1, 0.9] range for vibrant colors
    vec3 color = normalize(Normal) * 0.4 + 0.5;
    FragColor = vec4(color, 1.0);
}
