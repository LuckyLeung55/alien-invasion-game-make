import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """表示单个敌人的类"""
    def __init__(self,ai_game):
        """初始化敌人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        self.image = pygame.image.load('main/images/alice.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.x = float(self.rect.x)
    
    def check_edges(self):
        """如果敌人位于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        return(self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
        
    def update(self):
        """向左或向右移动敌人"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x