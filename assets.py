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