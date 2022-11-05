import pygame as pg
from pygame.locals import *

from OpenGL.GL import *

import sys

from shader_programs import ShaderPrograms
from game_objects import *
from camera import Camera
from mesh import Mesh
from lights import Light
from scene import Scene

class GraphicsProgram:
    def __init__(self, window=(1200,900)):
        self.window = window
        pg.display.set_mode(self.window, pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.shaders = ShaderPrograms()
        self.shaders.get("default").use()
        self.camera = Camera(self)
        
        self.mesh = Mesh(self)
        self.scene = Scene(self)
        self.skybox = SkyboxObject(self)
        self.light = Light(self)
        self.init_game()
    
    def init_game(self):
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        glEnable(GL_DEPTH_TEST)
        glClearColor(125/206, 206/255, 235/255, 1)
        glViewport(0, 0, self.window[0], self.window[1])
    
    def update(self):
        self.delta_time = self.clock.tick(60) * 0.001
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
    
    def init_frame(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    def display(self):
        self.init_frame()
        self.shaders.get("default").use()
        self.camera.update()
        self.light.update()
        
        self.scene.draw()
        
        self.shaders.get("skybox").use()
        self.skybox.draw()
        
        pg.display.flip()
    
    def check_events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == K_ESCAPE:
                        pg.quit()
                        sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.display()   