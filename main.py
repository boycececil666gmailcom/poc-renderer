#!/usr/bin/env python
import sys
import os
import glfw
from OpenGL.GL import *
import glm
from dotenv import load_dotenv

# Import modular engine classes
from engine.window import Window
from engine.shader import Shader
from engine.mesh import Mesh

# Load environment variables
load_dotenv()

# Window configuration
SCR_WIDTH = int(os.environ.get("SCR_WIDTH", 1280))
SCR_HEIGHT = int(os.environ.get("SCR_HEIGHT", 720))

def main():
    # 1. Create Window and OpenGL Context
    window = Window(SCR_WIDTH, SCR_HEIGHT, "Antigravity OpenGL Engine (Modular)")
    
    # 2. Configure global OpenGL state
    glEnable(GL_DEPTH_TEST)
    
    # 3. Compile shaders and load mesh
    shader = Shader("shaders/shader.vert", "shaders/shader.frag")
    
    model_path = sys.argv[1] if len(sys.argv) > 1 else None
    mesh = Mesh(model_path)
    
    # 4. Main Rendering Loop
    while not window.should_close():
        # Handle inputs
        window.process_input()
        
        # Clear screen buffers (dark premium background)
        glClearColor(0.094, 0.094, 0.106, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Bind shaders
        shader.use()
        
        # Real-time rotation & normalization transformation matrix calculations
        time = glfw.get_time()
        model = glm.mat4(1.0)
        model = glm.rotate(model, time * glm.radians(45.0), glm.vec3(0.5, 1.0, 0.0))
        model = glm.scale(model, glm.vec3(mesh.scale_factor))
        model = glm.translate(model, glm.vec3(-mesh.center[0], -mesh.center[1], -mesh.center[2]))
        
        # Camera & Projection matrices
        view = glm.translate(glm.mat4(1.0), glm.vec3(0.0, 0.0, -2.5))
        projection = glm.perspective(glm.radians(45.0), window.get_aspect(), 0.1, 100.0)
        
        # Upload matrix transformations to shaders
        shader.set_mat4("model", model)
        shader.set_mat4("view", view)
        shader.set_mat4("projection", projection)
        
        # Draw model
        mesh.draw(shader)
        
        # Double buffer swap and OS window event handling
        window.swap_buffers()
        window.poll_events()
        
    # 5. Clean up allocated graphics card buffers
    mesh.delete()
    shader.delete()
    window.terminate()
    return 0

if __name__ == '__main__':
    main()
