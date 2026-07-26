#version 330 core
out vec4 FragColor;

in vec3 Normal;
in vec2 TexCoords;

uniform vec4 materialColor;
uniform bool useTexture;
uniform sampler2D ourTexture;

void main()
{
    // Start with the base material color
    vec4 baseColor = materialColor;
    
    // Sample texture in memory if present
    if (useTexture)
    {
        baseColor *= texture(ourTexture, TexCoords);
    }
    
    // Apply a simple fake diffuse lighting factor to show depth
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(vec3(0.3, 1.0, 0.5));
    float diffuse = max(dot(norm, lightDir), 0.0) * 0.4 + 0.6;
    
    FragColor = vec4(baseColor.rgb * diffuse, baseColor.a);
}
