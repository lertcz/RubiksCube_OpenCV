import pygame
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
pygame.init() 

class Graphics:
    def __init__(self, screen, display) -> None:
        self.screen = screen
        self.display = display

        self.bitmap_tex = None

        # buttons
        #self.plusImg = pygame.transform.scale(pygame.image.load('images/plus.webp'), (64, 64)).convert_alpha()
        #self.minusImg = pygame.transform.scale(pygame.image.load('images/minus.webp'), (64, 64)).convert_alpha()

        self.BUTTONS = [
            ((95, 535), (30, 30), ("changeSpeed", 1)), #plus button
            ((175, 535), (30, 30), ("changeSpeed", -1)), #minus button
            ((440, 530), (25, 35), ("play_pause", None)), #play/pause button
        ]

    def drawText(self, x, y, text, size, font):
        font = pygame.font.SysFont(font, size)
        textSurface = font.render(text, True, (255, 255, 255, 255)).convert_alpha()
        textData = pygame.image.tostring(textSurface, "RGBA", True)
        glWindowPos2d(x - textSurface.get_width()//2, y)
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    def detectButton(self, pos):
        x, y = pos
        for start, size, function in self.BUTTONS:
            #print(pos, start, size)
            if x in range(start[0], start[0] + size[0]):
                if y in range(start[1], start[1] + size[1]):
                    function, param = function
                    return [function, param]
        else:
            return None

class Button:
    def __init__(self, screen, text, width, height, pos, elevation, function=None) -> None:
        self.screen = screen
        self.function = function

        # atributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        #bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#354B5E"

        # text
        self.text_surf = pygame.font.Font(None, 30).render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
    
    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()
    
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos): #if we colide with the button
            self.top_color = "#D74B4B"
            if pygame.mouse.get_pressed()[0]: #lmb
                self.dynamic_elevation = 0
                self.pressed = True

            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    if self.function: 
                        self.function()
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = "#475F77"
