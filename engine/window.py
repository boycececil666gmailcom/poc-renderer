import glfw

class Window:
    def __init__(self, width, height, title):
        # Initialize GLFW
        glfw.init()
        
        # Configure window context settings
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        
        # Create GLFW window
        self.handle = glfw.create_window(width, height, title, None, None)
        
        # Bind the OpenGL context
        glfw.make_context_current(self.handle)
        
        # Register resizing event callback
        glfw.set_framebuffer_size_callback(self.handle, self._framebuffer_size_callback)
        
    def _framebuffer_size_callback(self, window, width, height):
        from OpenGL.GL import glViewport
        glViewport(0, 0, width, height)
        
    def should_close(self):
        return glfw.window_should_close(self.handle)
        
    def swap_buffers(self):
        glfw.swap_buffers(self.handle)
        
    def poll_events(self):
        glfw.poll_events()
        
    def process_input(self):
        if glfw.get_key(self.handle, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(self.handle, True)
            
    def get_size(self):
        return glfw.get_framebuffer_size(self.handle)
        
    def get_aspect(self):
        width, height = self.get_size()
        return width / height if height > 0 else 1.0
        
    def terminate(self):
        glfw.terminate()
