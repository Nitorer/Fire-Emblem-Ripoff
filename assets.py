import pygame
import os

def load_images(folder_path="Assets"):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            path = os.path.join(folder_path, filename)
            key = os.path.splitext(filename)[0]
            images[key] = pygame.image.load(path).convert_alpha()
    return images

class SpriteSheet:
    def __init__(self, image_path, frame_width, frame_height):
        self.sheet = pygame.image.load(image_path).convert()
        self.sheet.set_colorkey((255,0,255))
        self.frame_width = frame_width
        self.frame_height = frame_height
        
    def get_frame(self, col, row):
        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), (col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height))
        return frame
    
class Animation:
    def __init__(self, frames, frame_duration):
        self.frames = frames
        self.frame_duration = frame_duration 
        self.current_time = 0
        self.index = 0
        
    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.frame_duration:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.frames)
            
    def get_current_frame(self):
        return self.frames[self.index]