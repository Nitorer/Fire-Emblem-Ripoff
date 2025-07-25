import pygame
import os

def load_images(folder_path="Assets"):
    images = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
            path = os.path.join(folder_path, filename)
            key = os.path.splitext(filename)[0]

            image = pygame.image.load(path).convert_alpha()

            # Skip sprite sheets like Lyn.gif — they'll be scaled manually
            if key.lower() not in ["lyn"]:  # add other sprite sheets here if needed
                images[key] = image  # unscaled
    return images

class SpriteSheet:
    def __init__(self, image_path, frame_width, frame_height):
        self.sheet = pygame.image.load(image_path).convert()
        self.sheet.set_colorkey((149,7,121.255))  # Magenta transparency
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_frame(self, col, row, origin_x=0, origin_y=0):
        SCALE_FACTOR = 4

        start_x = origin_x + col * self.frame_width
        start_y = origin_y + row * self.frame_height

        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.sheet, (0, 0), (start_x, start_y, self.frame_width, self.frame_height))

        scaled_frame = pygame.transform.scale(frame, (self.frame_width * SCALE_FACTOR, self.frame_height * SCALE_FACTOR))
        return scaled_frame
        
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