import glm
from OpenGL.GL import *
import numpy as np

class Light:
    def __init__(self, app, position=(2, 2, 0), color=(1, 1, 1)):
        self.shaderId = app.shaders.get("default").shaderId
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        # intensities
        self.Ia = 0.43 * self.color  # ambient
        self.Id = 0.8 * self.color  # diffuse
        self.Is = 1.0 * self.color  # specular
        # locations 
        self.light_pos_loc= glGetUniformLocation(self.shaderId, "u_light.position")
        self.light_Ia_loc= glGetUniformLocation(self.shaderId, "u_light.Ia")
        self.light_Id_loc= glGetUniformLocation(self.shaderId, "u_light.Id")
        self.light_Is_loc= glGetUniformLocation(self.shaderId, "u_light.Is")
        
    def update(self):
        glUniform3fv(self.light_pos_loc,1,np.array(self.position))
        glUniform3fv(self.light_Ia_loc,1,np.array(self.Ia))
        glUniform3fv(self.light_Id_loc,1,np.array(self.Id))
        glUniform3fv(self.light_Is_loc,1,np.array(self.Is))
        
