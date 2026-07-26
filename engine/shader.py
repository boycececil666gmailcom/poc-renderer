import sys
from OpenGL.GL import *
import glm

class Shader:
    def __init__(self, vert_path, frag_path):
        # Compile and link program
        self.program_id = self._create_shader_program(vert_path, frag_path)
        
    def use(self):
        glUseProgram(self.program_id)
        
    def set_mat4(self, name, matrix):
        loc = glGetUniformLocation(self.program_id, name)
        glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(matrix))
        
    def delete(self):
        glDeleteProgram(self.program_id)
        
    def _load_source(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading shader file {path}: {e}")
            sys.exit(-1)
            
    def _compile_shader(self, shader_type, source):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)
        
        success = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(shader)
            print(f"Shader compilation failed: {info_log.decode('utf-8')}")
            glDeleteShader(shader)
            sys.exit(-1)
        return shader
        
    def _create_shader_program(self, vert_path, frag_path):
        vert_src = self._load_source(vert_path)
        frag_src = self._load_source(frag_path)
        
        vs = self._compile_shader(GL_VERTEX_SHADER, vert_src)
        fs = self._compile_shader(GL_FRAGMENT_SHADER, frag_src)
        
        program = glCreateProgram()
        glAttachShader(program, vs)
        glAttachShader(program, fs)
        glLinkProgram(program)
        
        success = glGetProgramiv(program, GL_LINK_STATUS)
        if not success:
            info_log = glGetProgramInfoLog(program)
            print(f"Program linking failed: {info_log.decode('utf-8')}")
            glDeleteShader(vs)
            glDeleteShader(fs)
            glDeleteProgram(program)
            sys.exit(-1)
            
        glDeleteShader(vs)
        glDeleteShader(fs)
        return program
