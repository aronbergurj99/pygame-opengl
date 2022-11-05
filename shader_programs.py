
from OpenGL.GL import *
import OpenGL
import sys

class ShaderPrograms:
    def __init__(self):
        self.shaders = {}
        self.shaders["default"] = BaseShader("default")
        self.shaders["skybox"] = BaseShader("skybox")
        
    def get(self, shader_name):
        return self.shaders[shader_name]
    
class BaseShader: 
    def __init__(self, shader):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        with open (sys.path[0] + f"/shaders/{shader}.vert") as shader_file:
            glShaderSource(vert_shader, shader_file.read())
        glCompileShader(vert_shader)
        if glGetShaderiv(vert_shader, GL_COMPILE_STATUS) != 1:
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))
    

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        with open (sys.path[0] + f"/shaders/{shader}.frag") as shader_file:
            glShaderSource(frag_shader, shader_file.read())
        glCompileShader(frag_shader)
        if glGetShaderiv(frag_shader, GL_COMPILE_STATUS) != 1:
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))
        
        self.shaderId = glCreateProgram()
        glAttachShader(self.shaderId, vert_shader)
        glAttachShader(self.shaderId, frag_shader)
        glLinkProgram(self.shaderId)
        
    def use(self):
        try:
            glUseProgram(self.shaderId)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.shaderId))
            raise