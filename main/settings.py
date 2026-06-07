class Settings:
    """储存游戏《外星人游戏》中所有设置的类"""
    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 1056
        self.screen_height = 655
        
        self.bg_color = (220,220,220)
        
        self.ship_limit = 3
        
        self.bullet_width = 15
        self.bullet_heigth = 30
        self.bullet_color = (255,30,92)
        self.bullets_allowed = 10
        
        self.fleet_drop_speed = 10
        
        self.fleet_direction = 1
        
        self.speedup_scale = 1.1
        
        self.score_scale = 1.5
        self.initialien_dynamic_settings()
        
    def initialien_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 20
        self.bullet_speed = 40
        self.alien_speed = 2.0
        
        self.fleet_direction = 1
        
        self.alien_points = 50
        
    def increase_speed(self):
        """提高速度设置的值和敌人分数"""
        self.ship_speed *= self.speedup_scale
        
        self.alien_speed *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)