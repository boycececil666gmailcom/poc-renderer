import sys
from OpenGL.GL import *
import numpy as np
import trimesh

class Mesh:
    def __init__(self, model_path=None):
        # 1. Load model or generate fallback torus
        if model_path:
            print(f"Loading model: {model_path}")
            scene_or_mesh = trimesh.load(model_path)
            if isinstance(scene_or_mesh, trimesh.Scene):
                print("Concatenating scene geometry...")
                mesh = scene_or_mesh.dump(concatenate=True)
            else:
                mesh = scene_or_mesh
        else:
            print("No model path provided. Loading default test_cube.glb...")
            scene_or_mesh = trimesh.load("test_cube.glb")
            if isinstance(scene_or_mesh, trimesh.Scene):
                mesh = scene_or_mesh.dump(concatenate=True)
            else:
                mesh = scene_or_mesh
            
        # 2. Extract vertex details
        print("Processing mesh data...")
        vertices = mesh.vertices[mesh.faces].astype('float32').reshape(-1)
        normals = mesh.vertex_normals[mesh.faces].astype('float32').reshape(-1)
        
        self.vertex_count = len(vertices) // 3
        print(f"Loaded mesh with {self.vertex_count} vertices.")
        
        # 3. Calculate normalization transform parameters (centering and scaling)
        self.center = mesh.centroid
        size = mesh.extents
        max_dim = max(size)
        self.scale_factor = 1.5 / max_dim if max_dim > 0 else 1.0
        
        # 4. Generate and bind OpenGL buffers (VAO & VBOs)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # Position Buffer
        self.VBO_pos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_pos)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        # Normal Buffer
        self.VBO_normal = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_normal)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        
        # Unbind VBOs & VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def draw(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        glBindVertexArray(0)
        
    def delete(self):
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(1, [self.VBO_pos])
        glDeleteBuffers(1, [self.VBO_normal])
