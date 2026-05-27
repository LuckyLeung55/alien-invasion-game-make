import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from character import Ship
from bullet import Bullet
from monster import Alien
from background import Background

class AlienGameA:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        # 设置小窗口的屏幕
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        #下面这段代码是设置全屏的，如果有需要就得把上面这段代码注释掉

        # self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.backg = Background(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.character = pygame.sprite.Group()
        
        self._create_fleet()
        self.game_active = False
        
        self.play_button = Button(self,"Play")
        
    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()            
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):        
        """ 响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)                    
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
          
    def _check_keydown_events(self,event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    def _check_keyup_events(self,event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _check_play_button(self,mouse_pos):
        """在玩家单机play按钮时开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialien_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            
            self.bullets.empty()
            self.character.empty()

            self._create_fleet()
            self.ship.center_ship()
            
            pygame.mouse.set_visible(False)
            
    def _fire_bullet(self):
        """创建一个子弹,并将其加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        self.bullets.update()
        
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.character,False,True)
        
        if collisions:
            for character in collisions.values():
                self.stats.score += self.settings.alien_points * len(character)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.character:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        
            self.stats.level += 1
            self.sb.prep_level()
        
    def _update_aliens(self):
        """检查是否有敌人位于屏幕边缘，并更新外星舰队中所有敌人的位置"""
        self._check_fleet_edges()
        self.character.update()
        
        if pygame.sprite.spritecollideany(self.ship,self.character):
            self._ship_hit()
        
        self._check_aliens_bottom()
            
    def _create_fleet(self):
        """创建一个外星舰队"""
        char = Alien(self)
        alien_width,alien_height = char.rect.size
    
        current_x,current_y = alien_width,alien_height
        while current_y < (self.settings.screen_height - 6 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width
                
            current_x = alien_width
            current_y += 2 * alien_height
        
    def _create_alien(self,x_position,y_position):
        """创建一个敌人，并将其加入外星舰队"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.character.add(new_alien)
    
    def _check_fleet_edges(self):
        """在有敌人到达边缘时采取相应措施"""
        for char in self.character.sprites():
            if char.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的方向"""
        for char in self.character.sprites():
            char.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _update_background(self):
        self.backg.bliting()
                                      
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self._update_background()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.character.draw(self.screen)
        self.sb.show_score()
        
        if not self.game_active:
            self.play_button.draw_button()
        
        pygame.display.flip() 
    
    def _ship_hit(self):
        """响应角色和敌人的碰撞"""
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.character.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
            
    def _check_aliens_bottom(self):
        """检查是否有敌人到达了屏幕的下边缘"""
        for char in self.character.sprites():
            if char.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
                    
if __name__ == '__main__':
    ai = AlienGameA()
    ai.run_game()