from OpenGL.GL import *
import numpy as np
import glm

class Material:
    def __init__(self, trimesh_material=None):
        self.base_color = glm.vec4(1.0, 1.0, 1.0, 1.0)  # Default white
        self.has_texture = False
        self.texture_id = 0
        
        if trimesh_material is not None:
            # 1. Base color factor (using main_color which abstracts PBR and Simple materials)
            if hasattr(trimesh_material, "main_color") and trimesh_material.main_color is not None:
                color = trimesh_material.main_color
                self.base_color = glm.vec4(
                    float(color[0]) / 255.0,
                    float(color[1]) / 255.0,
                    float(color[2]) / 255.0,
                    float(color[3]) / 255.0
                )
            elif hasattr(trimesh_material, "baseColorFactor"):
                color = trimesh_material.baseColorFactor
                if isinstance(color, (np.ndarray, list)):
                    self.base_color = glm.vec4(
                        color[0],
                        color[1],
                        color[2],
                        color[3] if len(color) > 3 else 1.0
                    )
                        
            # 2. Dynamic in-memory Texture Loading
            img = None
            if hasattr(trimesh_material, "image") and trimesh_material.image is not None:
                img = trimesh_material.image
            elif hasattr(trimesh_material, "baseColorTexture") and trimesh_material.baseColorTexture is not None:
                img = trimesh_material.baseColorTexture
                
            if img is not None:
                try:
                    self.has_texture = True
                    self.texture_id = self._load_texture_from_pil(img)
                except Exception as e:
                    print(f"Error loading material texture in memory: {e}")
                    self.has_texture = False
                    
    def _load_texture_from_pil(self, pil_image):
        # Convert image mode to RGBA if not already
        if pil_image.mode != 'RGBA':
            pil_image = pil_image.convert('RGBA')
            
        img_data = np.array(pil_image, dtype=np.uint8)
        width, height = pil_image.size
        
        # Generate and bind OpenGL texture
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        
        # Set filtering and wrap parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Upload pixel data to GPU memory
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id
        
    def bind(self, shader):
        # Bind base colors and texture flag uniforms
        glUniform4fv(glGetUniformLocation(shader.program_id, "materialColor"), 1, glm.value_ptr(self.base_color))
        glUniform1i(glGetUniformLocation(shader.program_id, "useTexture"), 1 if self.has_texture else 0)
        
        # If texture is present, bind to texture unit 0
        if self.has_texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glUniform1i(glGetUniformLocation(shader.program_id, "ourTexture"), 0)
            
    def unbind(self):
        if self.has_texture:
            glBindTexture(GL_TEXTURE_2D, 0)
            
    def delete(self):
        if self.has_texture:
            glDeleteTextures(1, [self.texture_id])
