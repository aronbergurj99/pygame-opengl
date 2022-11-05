from game_objects import *

class Scene:
    def __init__(self, app) -> None:
        self.game_objects = []
        self.app = app
        for x in range(10):
            for z in range(10):
                self.game_objects.append(CatObject(self.app, pos=(x+3,0,z+8), scale=(0.1,0.1,0.1)))
    
    def draw(self):
        for obj in self.game_objects:
            obj.draw()