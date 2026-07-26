#!/usr/bin/env python
import sys
import os
import time
import glfw
from OpenGL.GL import *
import glm
from dotenv import load_dotenv

# Import modular engine classes
from engine.window import Window
from engine.shader import Shader
from engine.mesh import Mesh
from engine.config import Config

def main():
    # 0. Load configuration settings
    config = Config()

    # 1. Create Window and OpenGL Context
    window = Window(config.scr_width, config.scr_height, "Antigravity OpenGL Engine (Modular)")
    
    # 2. Configure global OpenGL state
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # 3. Validate command line arguments and compile shaders
    if len(sys.argv) < 2:
        print("Error: A 3D model file path is required.")
        print("Usage: python main.py <path_to_3d_model>")
        sys.exit(1)
        
    model_path = sys.argv[1]
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        sys.exit(1)
        
    shader = Shader("shaders/shader.vert", "shaders/shader.frag")
    mesh = Mesh(model_path)
    
    # 4. Main Rendering Loop
    print(f"Target Frame Rate: {config.target_fps} FPS (Target Frame Time: {config.target_frame_time * 1000:.2f} ms)")
    while not window.should_close():
        frame_start = time.time()
        
        # Handle inputs
        window.process_input()
        
        # Clear screen buffers (dark premium background)
        glClearColor(0.094, 0.094, 0.106, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Bind shaders
        shader.use()
        
        # Model matrix respecting native glTF scene transforms loaded from Blender
        model = glm.mat4(1.0)
        
        # Camera View & Projection matrices from Config module
        view = glm.lookAt(config.cam_pos, config.cam_target, config.cam_up)
        projection = glm.perspective(glm.radians(config.cam_fov), window.get_aspect(), config.cam_near, config.cam_far)
        
        # Upload matrix transformations and lighting parameters to shaders
        shader.set_mat4("model", model)
        shader.set_mat4("view", view)
        shader.set_mat4("projection", projection)
        shader.set_vec3("lightDir", config.light_dir)
        
        # Draw model
        mesh.draw(shader)
        
        # Double buffer swap and OS window event handling
        window.swap_buffers()
        window.poll_events()
        
        # Software FPS Capping logic
        if config.target_frame_time > 0:
            frame_duration = time.time() - frame_start
            sleep_duration = config.target_frame_time - frame_duration
            if sleep_duration > 0:
                time.sleep(sleep_duration)
        
    # 5. Clean up allocated graphics card buffers
    mesh.delete()
    shader.delete()
    window.terminate()
    return 0

if __name__ == '__main__':
    main()
