import sys
from OpenGL.GL import *
import numpy as np
import trimesh
import glm

from engine.material import Material

class MeshPrimitive:
    def __init__(self, mesh_obj):
        # 1. Extract vertices and normal arrays
        vertices = mesh_obj.vertices[mesh_obj.faces].astype('float32').reshape(-1)
        normals = mesh_obj.vertex_normals[mesh_obj.faces].astype('float32').reshape(-1)
        self.vertex_count = len(vertices) // 3
        
        # 2. Initialize in-memory material extraction
        trimesh_mat = None
        if hasattr(mesh_obj, "visual") and mesh_obj.visual is not None:
            if hasattr(mesh_obj.visual, "material") and mesh_obj.visual.material is not None:
                trimesh_mat = mesh_obj.visual.material
                
        self.material = Material(trimesh_mat)
        
        # 3. Extract UV coordinates if a texture is bound
        self.VBO_uv = 0
        if self.material.has_texture and hasattr(mesh_obj.visual, "uv"):
            uvs = mesh_obj.visual.uv[mesh_obj.faces].astype('float32').reshape(-1)
        else:
            self.material.has_texture = False  # Disable if UVs are missing
            
        # 4. Generate OpenGL buffers
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # Vertex coordinates VBO
        self.VBO_pos = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_pos)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(0)
        
        # Normal vectors VBO
        self.VBO_normal = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO_normal)
        glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(1)
        
        # Texture coordinates (UV) VBO
        if self.material.has_texture:
            self.VBO_uv = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.VBO_uv)
            glBufferData(GL_ARRAY_BUFFER, uvs.nbytes, uvs, GL_STATIC_DRAW)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 0, None)
            glEnableVertexAttribArray(2)
            
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def draw(self, shader):
        # Bind the material color and texture to the active shader
        self.material.bind(shader)
        
        # Render the geometry primitive
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, self.vertex_count)
        glBindVertexArray(0)
        
        # Clean up bindings
        self.material.unbind()
        
    def delete(self):
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(1, [self.VBO_pos])
        glDeleteBuffers(1, [self.VBO_normal])
        if self.VBO_uv:
            glDeleteBuffers(1, [self.VBO_uv])
        self.material.delete()

class Mesh:
    def __init__(self, model_path):
        # 1. Load model
        print(f"Loading model: {model_path}")
        scene_or_mesh = trimesh.load(model_path)
            
        # 2. Compute bounding limits and compile primitives from glTF scene
        scene = scene_or_mesh
        self.center = scene.centroid
        size = scene.extents
        max_dim = max(size)
        self.scale_factor = 1.5 / max_dim if max_dim > 0 else 1.0
        
        # Compile primitives with scene node transforms applied
        self.primitives = []
        for node_name in scene.graph.nodes_geometry:
            transform, geometry_name = scene.graph[node_name]
            # Copy base geometry mesh and apply transform matrix
            geom = scene.geometry[geometry_name].copy()
            geom.apply_transform(transform)
            # Create mesh primitive
            self.primitives.append(MeshPrimitive(geom))
            
    def draw(self, shader):
        for primitive in self.primitives:
            primitive.draw(shader)
            
    def delete(self):
        for primitive in self.primitives:
            primitive.delete()
