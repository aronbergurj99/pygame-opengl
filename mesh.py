from textures import Textures
from models import Models

class Mesh:
    def __init__(self, app):
        self.app = app
        self.textures = Textures()
        self.models = Models(app.shaders)