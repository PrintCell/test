import pygame

import plane_sprite


class PlaneGame:

    def __init__(self):
        print("游戏初始化")
        # 设置游戏界面
        self.screen = pygame.display.set_mode(plane_sprite.SCREEN_RECT)
        # 设置时钟
        self.clock = pygame.time.Clock()
        # 调用私有方法创建精灵及精灵组
        self.__creat_sprite()
        # 设置计时器，创建敌机
        pygame.time.set_timer(plane_sprite.ENEMY_EVENT, plane_sprite.ENEMY_TIME)
        # 设置子弹的计时器，发射子弹
        pygame.time.set_timer(plane_sprite.BULLET_EVENT, plane_sprite.BULLET_TIME)
        # 设置敌机子弹计时器，敌机发射子弹
        pygame.time.set_timer(plane_sprite.ENEMY_BULLET, plane_sprite.ENEMY_BULLET_TIME)

    def __creat_sprite(self):
        # 创建背景精灵
        bg_1 = plane_sprite.BackGround(1)
        bg_2 = plane_sprite.BackGround(2)
        # 创建背景精灵组
        self.back_group = pygame.sprite.Group(bg_1, bg_2)
        # 创建敌机精灵组
        self.enemy = plane_sprite.Enemy()
        self.enemy_group = pygame.sprite.Group()
        # 创建英雄和它的精灵组
        self.hero = plane_sprite.Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始了...")
        while True:
            # 设置刷新帧率
            self.clock.tick(plane_sprite.FPS)
            # 事件监听
            self.__event_get()
            self.__Fire__()
            # 碰撞检测
            self.__check_meet()
            # 更新/绘制精灵组
            self.__update_sprite()
            # 更新显示
            pygame.display.update()

    def __event_get(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                PlaneGame.game_over()

            elif event.type == plane_sprite.ENEMY_EVENT:
                # 创建敌机对象并把它添加到敌机精灵组中
                self.enemy = plane_sprite.Enemy()
                self.enemy_group.add(self.enemy)

        keys_pressed = pygame.key.get_pressed()
        # 右移
        if keys_pressed[pygame.K_RIGHT]:
            self.hero.x_speed = 3

        # 左移
        elif keys_pressed[pygame.K_LEFT]:
            self.hero.x_speed = -3

        # 上移
        elif keys_pressed[pygame.K_UP]:
            self.hero.y_speed = -3
        # 下移
        elif keys_pressed[pygame.K_DOWN]:
            self.hero.y_speed = 3

        else:
            self.hero.x_speed = 0
            self.hero.y_speed = 0

    def __check_meet(self):
        pygame.sprite.groupcollide(self.enemy_group, self.hero.bullet_group, True, False)
        kill_list1 = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        kill_list2 = pygame.sprite.spritecollide(self.hero, self.enemy.bullet_groups, True)
        if len(kill_list1) + len(kill_list2) > 0:
            self.hero.kill()
            PlaneGame.game_over()

    def __update_sprite(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)
        self.enemy.bullet_groups.update()
        self.enemy.bullet_groups.draw(self.screen)

    def __Fire__(self):
        for event in pygame.event.get():
            if event.type == plane_sprite.BULLET_EVENT:
                self.hero.fire()
                print("英雄发射子弹")
            elif event.type == plane_sprite.ENEMY_BULLET:
                print("敌机发射子弹")
                self.enemy.fire()

    @staticmethod
    def game_over():
        print("游戏退出")
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
