#!/usr/bin/env python
import sys
import os
import time

from engine import Config, Window, Shader, Mesh, Camera, Renderer

DEFAULT_MODEL_PATH = os.path.join("gltf", "toyota_supra.gltf")

def main():
    # 1. Load configuration and initialize context
    config = Config()
    window = Window(config.scr_width, config.scr_height, "Antigravity OpenGL Engine (Modular)")
    renderer = Renderer(window, config)

    # 2. Select 3D model path (Migrated to GLTF by default)
    model_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL_PATH
    if not os.path.exists(model_path):
        print(f"Error: Model file '{model_path}' not found.")
        sys.exit(1)

    # 3. Load graphics resources and camera
    shader = Shader("shaders/shader.vert", "shaders/shader.frag")
    mesh = Mesh(model_path)
    camera = Camera(
        pos=config.cam_pos,
        target=config.cam_target,
        fov=config.cam_fov,
        near=config.cam_near,
        far=config.cam_far
    )

    print(f"Loaded Model: {model_path}")
    print(f"Target Frame Rate: {config.target_fps} FPS")

    # 4. Main Rendering Loop
    try:
        while not window.should_close():
            frame_start = time.time()

            window.process_input()
            renderer.render_frame(shader, mesh, camera)
            renderer.limit_frame_rate(frame_start)
    finally:
        # 5. Clean up allocated graphics card buffers
        mesh.delete()
        shader.delete()
        window.terminate()

    return 0

if __name__ == '__main__':
    main()
