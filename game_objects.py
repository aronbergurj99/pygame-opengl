from models import *
import glm
import numpy as np

class BaseObject:
    def __init__(self, app, model="cube", texture="test", pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        
        self.shader = app.shaders.get("default")
        self.model = self.app.mesh.models.get(model)
        self.texture = self.app.mesh.textures.get(texture)
        self.model_matrix = self.get_model_matrix()
        self.model_m_loc = glGetUniformLocation(self.shader.shaderId, "m_model")
        
        
    def get_model_matrix(self):
        model_matrix = glm.mat4()
        # translate
        model_matrix = glm.translate(model_matrix, self.pos)
        # rotate
        model_matrix = glm.rotate(model_matrix, self.rot.z, glm.vec3(0, 0, 1))
        model_matrix = glm.rotate(model_matrix, self.rot.y, glm.vec3(0, 1, 0))
        model_matrix = glm.rotate(model_matrix, self.rot.x, glm.vec3(1, 0, 0))
        # scale
        model_matrix = glm.scale(model_matrix, self.scale)
        return model_matrix
        
    def update(self):
        self.model_matrix = self.get_model_matrix()
        glUniformMatrix4fv(self.model_m_loc, 1, True, np.array(self.model_matrix))
        
    def draw(self):
        self.texture.use()
        self.update()
        self.model.draw()
        
class CubeObject(BaseObject):
    def __init__(self, app, model="cube", texture="test", pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, model, texture, pos, rot, scale)
        
class CatObject(BaseObject):
    def __init__(self, app, model="cat", texture="cat", pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, model, texture, pos, rot, scale)

class SkyboxObject(BaseObject):
    def __init__(self, app, model="skybox", texture="skybox", pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, model, texture, pos, rot, scale)
        self.shaderId = self.model.shaderId
        self.proj_loc = glGetUniformLocation(self.shaderId, "m_proj")
        self.view_loc = glGetUniformLocation(self.shaderId, "m_view")
        
    def update(self):
        glUniformMatrix4fv(self.proj_loc, 1, True, np.array(self.app.camera.m_proj))
        glUniformMatrix4fv(self.view_loc, 1, True, np.array(glm.mat4(glm.mat3(self.app.camera.m_view))))
    
    def draw(self):
        glUniform1i(glGetUniformLocation(self.shaderId, "u_texture0"), 0);
        self.update()
        self.texture.use()
        self.model.draw()