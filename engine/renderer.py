import time
import glm
from OpenGL.GL import *

from engine.window import Window
from engine.shader import Shader
from engine.mesh import Mesh
from engine.camera import Camera
from engine.config import Config

class Renderer:
    """Elegant OpenGL Renderer managing frame rendering pipeline and performance."""

    def __init__(self, window: Window, config: Config):
        self.window = window
        self.config = config
        self.clear_color = (0.094, 0.094, 0.106, 1.0)
        
        # Configure global OpenGL pipeline parameters
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def render_frame(self, shader: Shader, mesh: Mesh, camera: Camera, model_matrix: glm.mat4 = None) -> None:
        """Executes a single render frame pass."""
        if model_matrix is None:
            model_matrix = glm.mat4(1.0)

        # Clear color and depth buffers
        glClearColor(*self.clear_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Activate shader program and bind uniform matrices
        shader.use()
        shader.set_mat4("model", model_matrix)
        shader.set_mat4("view", camera.get_view_matrix())
        shader.set_mat4("projection", camera.get_projection_matrix(self.window.get_aspect()))
        shader.set_vec3("lightDir", self.config.light_dir)

        # Draw mesh primitives
        mesh.draw(shader)

        # Swap buffers and poll OS window events
        self.window.swap_buffers()
        self.window.poll_events()

    def limit_frame_rate(self, frame_start_time: float) -> None:
        """Applies software frame rate limiting based on Config settings."""
        if self.config.target_frame_time > 0:
            duration = time.time() - frame_start_time
            remaining = self.config.target_frame_time - duration
            if remaining > 0:
                time.sleep(remaining)
