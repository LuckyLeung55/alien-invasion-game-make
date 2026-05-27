import pygame

class Background:
    """表示壁纸图"""
    def __init__(self,ai_game):
        """初始化壁纸相关属性"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('main/images/yingyu.bmp')
        self.rect = self.image.get_rect()
        
        self.rect.width = self.settings.screen_width
        self.rect.height = self.settings.screen_height
        
    def bliting(self):
        self.screen.blit(self.image,self.rect)