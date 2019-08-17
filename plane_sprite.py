import random
import pygame

# 屏幕大小常量
SCREEN_RECT = [480, 700]
# 刷新帧率常量
FPS = 60
# 刷敌机的速度
ENEMY_TIME = 3000
# 创建敌机的计时器常量
ENEMY_EVENT = pygame.USEREVENT
# 发射子弹的速度，每0.5秒射一次
BULLET_TIME = 1
# 敌机发射子弹的速度
ENEMY_BULLET_TIME = 1
# 创建子弹的计时器常量
BULLET_EVENT = pygame.USEREVENT + 1
# 敌机发射子弹事件
ENEMY_BULLET = pygame.USEREVENT + 2


class PlaneSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self, *args):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


# 创建背景类
class BackGround(PlaneSprite):
    def __init__(self, weici):
        super().__init__("image/background.png", x_speed=0, y_speed=1)
        self.weici = weici
        if self.weici == 2:
            self.rect.y = -SCREEN_RECT[1]

    def update(self, *args):
        super().update()
        if self.rect.y >= SCREEN_RECT[1]:
            self.rect.y = -self.rect.height


# 敌机类
class Enemy(PlaneSprite):
    def __init__(self):
        super().__init__("image/enemy1.png", x_speed=0, y_speed=1)
        # 指定飞机的飞行速度
        self.y_speed = random.randint(1, 2)
        # self.x_speed = random.randint(0)
        # 指定飞机的出现地点
        self.rect.bottom = 0
        max_x = SCREEN_RECT[0] - self.rect.width
        self.rect.x = random.randint(0, max_x)
        self.bullet_groups = pygame.sprite.Group()

    def update(self, *args):
        super().update()
        # 判断飞出屏幕
        if self.rect.x >= SCREEN_RECT[0] or self.rect.y >= SCREEN_RECT[1]:
            # kill把自己从内存中删除
            self.kill()

    def fire(self):
        bullet = HeroBullet("image/bullet2.png", 0, 4)
        bullet.rect.x = self.rect.centerx
        bullet.rect.y = self.rect.y + 15

        # 把子弹添加到子弹精灵组
        self.bullet_groups.add(bullet)


# 创建英雄类
class Hero(PlaneSprite):
    def __init__(self):
        super().__init__("image/life.png", 0, 0)
        # 笨办法设置飞机的初始位置 放在中间，不知对不对
        self.rect.x = (SCREEN_RECT[0] - 46) / 2
        self.rect.y = SCREEN_RECT[1] - 120
        # 创建子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self, *args):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_RECT[0] - self.rect.width:
            self.rect.x = SCREEN_RECT[0] - self.rect.width
        elif self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_RECT[1] - self.rect.height:
            self.rect.y = SCREEN_RECT[1] - self.rect.height

    def fire(self):
        self.bullet = HeroBullet("image/bullet1.png", 0, -4)
        for i in (-1, 0, 1):
            self.bullet.rect.x = self.rect.centerx + i
            self.bullet.rect.y = self.rect.y - 15

            # 把子弹添加到子弹精灵组
            self.bullet_group.add(self.bullet)


class HeroBullet(PlaneSprite):
    def __init__(self, image_name, x_speed, y_speed):
        super().__init__(image_name, x_speed, y_speed)
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self, *args):
        super().update()
        if 0 > self.rect.y < SCREEN_RECT[1]:
            # kill把自己从内存中删除
            self.kill()
