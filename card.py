import pygame
from utils import load_image

class Card:
    def __init__(self, id, name, image_url=None):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.image = load_image(image_url)  # 이미지 로드
        self.is_flipped = False
        self.is_matched = False
    
    def flip(self):
        if not self.is_matched:
            self.is_flipped = not self.is_flipped
            return True
        return False
    
    def match(self):
        self.is_matched = True
        self.is_flipped = True
    
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.id == other.id
        return False
    
    def __str__(self):
        if self.is_flipped or self.is_matched:
            return f"{self.name[:10]:<10}"
        return "🃏        "