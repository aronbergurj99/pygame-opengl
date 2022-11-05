import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import ctypes
import pywavefront

class Models:
    def __init__(self, shaders):
        self.models = {}
        self.models["cube"] = CubeModel(shaders.get("default").shaderId)
        self.models["cat"] = CatModel(shaders.get("default").shaderId)
        self.models["skybox"] = SkyboxModel(shaders.get("skybox").shaderId)
        
    def get(self, name):
        return self.models[name]
        
class BaseModel:
    def __init__(self, shaderId):
        self.shaderId = shaderId
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        vertex_data = self.get_vertex_data()
        
        self.vertex_count = (len(vertex_data) // 8 ) 
        
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        position_loc = glGetAttribLocation(self.shaderId, "a_position")
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(
            position_loc,
            3, GL_FLOAT, False, 8 * sizeof(GLfloat), ctypes.c_void_p(5 * sizeof(GLfloat)))
        
        # glVertexAttribPointer(
        #     glGetAttribLocation(self.shaderId, "a_normal"),
        #     3, GL_FLOAT, False, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        texture_cord_loc = glGetAttribLocation(self.shaderId, "a_texcord0")
        glEnableVertexAttribArray(texture_cord_loc)
        glVertexAttribPointer(
            texture_cord_loc,
            2, GL_FLOAT, False, 8 * sizeof(GLfloat), ctypes.c_void_p(0 * sizeof(GLfloat)))
            
            
    def get_vertex_data(self):
        pass
    
    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0,self.vertex_count)
    
    
class CubeModel(BaseModel):
    def __init__(self, shaderId):
        super().__init__(shaderId)
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype=np.float32).reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data.flatten()

class CatModel(BaseModel):
    def __init__(self, shaderId):
        super().__init__(shaderId)
        
    def get_vertex_data(self):
        objs = pywavefront.Wavefront('objects/cat/20430_Cat_v1_NEW.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

class SkyboxModel(BaseModel):
    def __init__(self, shaderId):
        self.shaderId = shaderId
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        vertex_data = self.get_vertex_data()
        
        self.vertex_count = (len(vertex_data) // 3) 
        
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        position_loc = glGetAttribLocation(self.shaderId, "a_position")
        glEnableVertexAttribArray(position_loc)
        glVertexAttribPointer(
            position_loc,
            3, GL_FLOAT, False, 3 * sizeof(GLfloat), ctypes.c_void_p(0 * sizeof(GLfloat)))
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')
        return vertex_data.flatten()
