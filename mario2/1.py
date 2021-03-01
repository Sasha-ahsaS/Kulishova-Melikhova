import pygame
import pygame_gui
import sys
import os
import random

pygame.mixer.pre_init(44100, -16, 1, 512)
file = 'фон1.mp3'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)
pygame.mixer.music.play(-1) # Играет фоновая музыка
s_catch = pygame.mixer.Sound('взятие.mp3')
end = pygame.mixer.Sound('проигрыш.mp3')
win = pygame.mixer.Sound('прохождение уровня.mp3')
winner = pygame.mixer.Sound('победа.mp3')
no = pygame.mixer.Sound('не хватает денег.mp3')
collection_coin1 = 0


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key is -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class Pravila:
    def pravila(self):
        self.y1 = 25
        pygame.font.init()
        sc = pygame.display.set_mode((800, 600))
        sc.fill(("#94ffd6"))
        f1 = pygame.font.Font(None, 49)
        text1 = f1.render('Правила игры', True, (0, 102, 66))
        f2 = pygame.font.Font(None, 30)
        text2 = f2.render("Панда Тишка потерялся и не может найти свой дом из-за ", False, (17, 96, 98))
        text3 = f2.render("мусора. Если хочешь ему помочь, тебе необходи пройти ", False, (17, 96, 98))
        text4 = f2.render("лабиринт и собрать весь мусор на своем пути.", False, (17, 96, 98))
        text5 = f2.render("Чтобы привести героя в движение воспользуйся стрелками", False, (17, 96, 98))
        text7 = f2.render("", False, (17, 96, 98))
        text8 = f2.render("Для движения на искосок зажми  две стрелки.", False, (17, 96, 98))
        text9 = f2.render("Чтобы собрать мусор необходимо его коснуться.", False, (17, 96, 98))
        f1 = pygame.font.Font(None, 49)
        text1 = f1.render('Правила игры', True, (0, 102, 66))
        f2 = pygame.font.Font(None, 30)
        text10 = f2.render('На сложных уровня также есть задача спастись от врага.', False, (17, 96, 98))
        text11 = f2.render('Чтобы уровень считался пройденым необходимо собрать ', False, (17, 96, 98))
        text12 = f2.render('весь мусор и пройти лабиринт.', False, (17, 96, 98))
        text13 = f2.render('', False, (17, 96, 98))
        sc.blit(text13, (10, self.y1 * 15))
        sc.blit(text12, (10, self.y1 * 14))
        sc.blit(text11, (10, self.y1 * 13))
        sc.blit(text10, (10, self.y1 * 12))
        sc.blit(text9, (10, self.y1 * 11))
        sc.blit(text8, (10, self.y1 * 10))
        sc.blit(text7, (10, self.y1 * 9))
        sc.blit(text1, (165, self.y1))
        sc.blit(text2, (10, self.y1 * 3))
        sc.blit(text3, (10, self.y1 * 4))
        sc.blit(text4, (10, self.y1 * 5))
        sc.blit(text5, (10, self.y1 * 6))
        sc.blit(text9, (10, self.y1 * 11))
        sc.blit(text8, (10, self.y1 * 10))
        sc.blit(text7, (10, self.y1 * 9))
        sc.blit(text1, (165, self.y1))
        sc.blit(text2, (10, self.y1 * 3))
        sc.blit(text3, (10, self.y1 * 4))
        sc.blit(text4, (10, self.y1 * 5))
        sc.blit(text5, (10, self.y1 * 6))
        self.run1 = True
        while self.run1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run1 = False
            pygame.display.update()


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, img='p.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.change_x = 0
        self.change_y = 0
        self.walls = None

        # Добавляем пятно
        self.coins = None
        self.collection_coins = 0

        # Добавляем врага
        self.enemies = pygame.sprite.Group()
        # Игрок жив пока не встретит противника
        self.alive = True
        self.pobeda = False

    def update(self):
        global collection_coin1
        #  Движение вправо - влево
        self.rect.x += self.change_x
        # Проверим, что объект не врезается в стену
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Если игрок двигается в право, вернем его правую границу к левой границе препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # Если в лево все наоборот
            else:
                self.rect.left = block.rect.right
        #  Движение вверх - вниз
        self.rect.y += self.change_y
        # Проверим, что объект не врезается в стену
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Вернем игрока за грнацу препятствия
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        if self.rect.y >= 590 and self.rect.x >= 450:
            self.pobeda = True

        # Проверим, что игрок встретил пятно
        coins_hit_list = pygame.sprite.spritecollide(self, self.coin, False)
        for coin in coins_hit_list:
            s_catch.play()
            collection_coin1 += 1
            self.collection_coins += 1
            coin.kill()
        f1 = pygame.font.SysFont(None, 25, True)
        text2 = f1.render(f"Собрано всего мусора: {collection_coin1}", True, (0, 102, 66))
        screen.blit(text2, (40, 40))
        # Проверим, что игрок встретил  противника
        if pygame.sprite.spritecollide(self, self.enemies, False):
            self.alive = False
            collection_coin1 -= self.collection_coins


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# Класс клякс которые нужно собрать
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img='клякса2.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Класс для врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img='мусорка.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direction = 1

    def update(self):
        # спрайт дошел, то стоп и должен повернуть обратно налево
        if self.rect.x >= self.stop:
            self.rect.x = self.stop
            self.direction = -1
        # спрайт дошел, то старт и должен повернуть обратно направо
        if self.rect.x <= self.start:
            self.rect.x = self.start
            self.direction = 1
        # смещать спрайт в указанном направление
        self.rect.x += self.direction * 2


# Поражение
class unwinner:
    def okno(self, run1):
        pygame.init()
        screen_size = (800, 600)
        screen2 = pygame.display.set_mode(screen_size)
        screen2.fill(pygame.Color("#94ffd6"))
        screen2.blit(text, (100, 100))
        pygame.draw.rect(screen2, (pygame.Color("#ace5ee")), (250, 300, 300, 80))
        screen2.blit(text_unwinner, (275, 320))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (x <= 550) and (x >= 250) and (y <= 380) and (y >= 300):
                        if run1 == 2:
                            uo2 = urov_2
                            uo2.ur(self)
                        if run1 == 3:
                            uo3 = urov_3
                            uo3.ur(self)
                        if run1 == 4:
                            uo4 = urov_4
                            uo4.ur(self)
                        if run1 == 5:
                            uo5 = urov_5
                            uo5.ur(self)
                pygame.display.update()


PINK = (194, 255, 224)
WHITE = (0, 0, 0)
BLUE = (29, 32, 76)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
font = pygame.font.SysFont('Arial', 50, True)
font1 = pygame.font.SysFont(None, 25, True)
text = font.render('Вы проиграли', True, WHITE)
text_vin = font.render('Лабиринт пройден', True, WHITE)
text_unwinner = font1.render('Начать заново уровень', True, WHITE)


# Финальное окно
class doma:
    def dom1(n, h):
        pygame.init()
        dom = ['l1.png', 'д2.png', 'д3.png', 'l4.png']
        screen_size = (800, 600)
        screen1 = pygame.display.set_mode(screen_size)
        screen1.fill(("#94ffd6"))
        intro_text = ["Спасибо за помощь!"]
        fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
        screen1.blit(fon, (0, 0))
        fon1 = pygame.transform.scale(load_image(dom[n]), (h, 200))
        screen1.blit(fon1, (75, 350))
        font = pygame.font.Font(None, 70)
        text_coord = 95
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(0, 107, 60))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen1.blit(string_rendered, intro_rect)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()


# Открывается магазин для финала игры
class final:
    def fin(self):
        global collection_coin1
        pygame.init()
        screen_size = (800, 600)
        screen3 = pygame.display.set_mode(screen_size)
        screen3.fill(("#94ffd6"))
        fon = pygame.transform.scale(load_image('l1.png'), (282, 200))
        screen3.blit(fon, (50, 30))
        f1 = pygame.font.SysFont(None, 25, True)
        text2 = f1.render(f"Собрано всего мусора: {collection_coin1}", True, (0, 102, 66))
        screen3.blit(text2, (10, 20))
        font1 = pygame.font.Font(None, 50)
        t = font1.render('Недостаточно средств', False, (17, 96, 98))
        text = font1.render('Mагазин домов', False, (17, 96, 98))
        screen3.blit(text, (300, 10))
        font = pygame.font.Font(None, 30)
        text1 = font.render('Дом 1. Цена - 20 мусора', False, (17, 96, 98))
        screen3.blit(text1, (100, 240))
        text2 = font.render('Купить', False, (17, 96, 98))
        pygame.draw.rect(screen3, (pygame.Color("#ace5ee")), (170, 265, 100, 30))
        screen3.blit(text2, (185, 270))
        fon1 = pygame.transform.scale(load_image('д2.png'), (193, 200))
        screen3.blit(fon1, (525, 40))
        text3 = font.render('Дом 2. Цена - 15 мусора', False, (17, 96, 98))
        screen3.blit(text3, (520, 250))
        pygame.draw.rect(screen3, (pygame.Color("#ace5ee")), (575, 275, 100, 30))
        screen3.blit(text2, (590, 280))
        fon2 = pygame.transform.scale(load_image('д3.png'), (272, 200))
        screen3.blit(fon2, (70, 320))
        text4 = font.render('Дом 3. Цена - 10 мусора', False, (17, 96, 98))
        screen3.blit(text4, (100, 530))
        pygame.draw.rect(screen3, (pygame.Color("#ace5ee")), (170, 560, 100, 30))
        screen3.blit(text2, (185, 565))
        fon3 = pygame.transform.scale(load_image('l4.png'), (162, 200))
        screen3.blit(fon3, (545, 320))
        text5 = font.render('Дом 4. Цена - 25 мусора', False, (17, 96, 98))
        screen3.blit(text5, (520, 530))
        pygame.draw.rect(screen3, (pygame.Color("#ace5ee")), (575, 560, 100, 30))
        screen3.blit(text2, (590, 565))
        d = doma
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (x <= 270) and (x >= 170) and (y <= 295) and (y >= 265) and collection_coin1 >= 20:
                        winner.play()
                        d.dom1(0, 282)
                    elif collection_coin1 < 20 and (x <= 270) and (x >= 170) and (y <= 295) and (y >= 265):
                        screen3.blit(t, (250, 300))
                        no.play()
                    if (x <= 675) and (x >= 575) and (y <= 295) and (y >= 265) and collection_coin1 >= 15:
                        d.dom1(1, 193)
                        winner.play()
                    elif collection_coin1 < 15 and (x <= 675) and (x >= 575) and (y <= 295) and (y >= 265):
                        screen3.blit(t, (250, 300))
                        no.play()
                    if (x <= 270) and (x >= 170) and (y <= 590) and (y >= 560) and collection_coin1 >= 10:
                        d.dom1(2, 272)
                        winner.play()
                    elif collection_coin1 < 10 and (x <= 270) and (x >= 170) and (y <= 590) and (y >= 560):
                        screen3.blit(t, (250, 300))
                        no.play()
                    if (x <= 675) and (x >= 575) and (y <= 590) and (y >= 560) and collection_coin1 >= 25:
                        d.dom1(3, 162)
                        winner.play()
                    elif (x <= 675) and (x >= 575) and (y <= 590) and (y >= 560) and collection_coin1 < 25:
                        screen3.blit(t, (250, 300))
                        no.play()
                pygame.display.update()


# Уровень 1
class urov_1():
    def ur1(self):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Тимошка')
        all_sprite_list = pygame.sprite.Group()
        wall_list = pygame.sprite.Group()
        coin_list = pygame.sprite.Group()
        wall_coord = [[0, 0, 10, 600], [790, 0, 10, 600], [10, 0, 790, 10],
                      [0, 200, 100, 10], [0, 590, 600, 10], [450, 400, 10, 200], [550, 450, 250, 10],
                      [180, 180, 110, 10],
                      [140, 250, 10, 190], [560, 100, 250, 10], [500, 160, 10, 150], [500, 300, 150, 10],
                      [280, 480, 170, 10]]
        for coord in wall_coord:
            wall = Wall(coord[0], coord[1], coord[2], coord[3])
            wall_list.add(wall)
            all_sprite_list.add(wall)
        coin_coord = [[100, 380], [40, 50], [200, 140], [520, 250], [330, 520]]
        for coord in coin_coord:
            coin = Coin(coord[0], coord[1])
            coin_list.add(coin)
            all_sprite_list.add(coin)
        # Создаем противника
        enemies_list = pygame.sprite.Group()
        enemies_coord = []
        for coord in enemies_coord:
            enemy = Enemy(coord[0], coord[1])
            enemies_list.add(enemy)
            all_sprite_list.add(enemy)
        player = Player(150, 150)
        player.walls = wall_list
        player.coin = coin_list
        all_sprite_list.add(player)
        player.enemies = enemies_list
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 5
                    elif event.key == pygame.K_UP:
                        player.change_y = -5
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0
            screen.fill(PINK)
            if not player.alive:
                end.play()
                un = unwinner
                un.okno(self, 1)
            else:
                all_sprite_list.update()
                all_sprite_list.draw(screen)
            if player.pobeda:
                win.play()
                screen.blit(text_vin, (100, 100))
                u2 = urov_2
                u2.ur(self)
            pygame.display.flip()
            clock.tick(60)


# Уровень 2
class urov_2():
    def ur(self):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Тимошка')
        all_sprite_list = pygame.sprite.Group()
        wall_list = pygame.sprite.Group()
        coin_list = pygame.sprite.Group()
        wall_coord = [[0, 0, 10, 600], [790, 0, 10, 600], [10, 0, 790, 10],
                      [0, 200, 100, 10], [0, 590, 600, 10], [450, 400, 10, 200], [550, 450, 250, 10]]
        for coord in wall_coord:
            wall = Wall(coord[0], coord[1], coord[2], coord[3])
            wall_list.add(wall)
            all_sprite_list.add(wall)
        coin_coord = [[350, 450], [480, 40], [690, 390], [10, 560]]
        for coord in coin_coord:
            coin = Coin(coord[0], coord[1])
            coin_list.add(coin)
            all_sprite_list.add(coin)
        # Создаем противника
        enemies_list = pygame.sprite.Group()
        enemies_coord = [[300, 500]]
        for coord in enemies_coord:
            enemy = Enemy(coord[0], coord[1])
            enemies_list.add(enemy)
            all_sprite_list.add(enemy)
        player = Player(150, 150)
        player.walls = wall_list
        player.coin = coin_list
        all_sprite_list.add(player)
        player.enemies = enemies_list
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 5
                    elif event.key == pygame.K_UP:
                        player.change_y = -5
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0
            screen.fill(PINK)
            if not player.alive:
                end.play()
                un = unwinner
                un.okno(self, 2)
            else:
                all_sprite_list.update()
                all_sprite_list.draw(screen)
            if player.pobeda:
                win.play()
                screen.blit(text_vin, (100, 100))
                urov3 = urov_3
                urov3.ur(self)
            pygame.display.flip()
            clock.tick(60)


# Уровень 3
class urov_3():
    def ur(self):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Тимошка')
        all_sprite_list = pygame.sprite.Group()
        wall_list = pygame.sprite.Group()
        coin_list = pygame.sprite.Group()
        wall_coord = [[0, 0, 10, 600], [790, 0, 10, 600], [10, 0, 790, 10],
                  [0, 200, 100, 10], [0, 590, 600, 10], [450, 400, 10, 200], [550, 450, 250, 10]]
        for coord in wall_coord:
            wall = Wall(coord[0], coord[1], coord[2], coord[3])
            wall_list.add(wall)
            all_sprite_list.add(wall)
        coin_coord = [[170, 80], [80, 500], [300, 150]]
        for coord in coin_coord:
            coin = Coin(coord[0], coord[1])
            coin_list.add(coin)
            all_sprite_list.add(coin)
        # Создаем противника
        enemies_list = pygame.sprite.Group()
        enemies_coord = [[10, 500], [400, 50]]
        for coord in enemies_coord:
            enemy = Enemy(coord[0], coord[1])
            enemies_list.add(enemy)
            all_sprite_list.add(enemy)
        player = Player(150, 150)
        player.walls = wall_list
        player.coin = coin_list
        all_sprite_list.add(player)
        player.enemies = enemies_list
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 5
                    elif event.key == pygame.K_UP:
                        player.change_y = -5
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0
            screen.fill(PINK)
            if not player.alive:
                end.play()
                un = unwinner
                un.okno(self, 3)
            else:
                all_sprite_list.update()
                all_sprite_list.draw(screen)
            if player.pobeda:
                win.play()
                screen.blit(text_vin, (100, 100))
                u4 = urov_4
                u4.ur(self)
            pygame.display.flip()
            clock.tick(60)


# Уровень 4
class urov_4():
    def ur(self):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Тимошка')

        all_sprite_list = pygame.sprite.Group()
        wall_list = pygame.sprite.Group()
        coin_list = pygame.sprite.Group()

        wall_coord = [[0, 0, 10, 600], [790, 0, 10, 600], [10, 0, 790, 10],
               [0, 200, 100, 10], [0, 590, 600, 10], [450, 400, 10, 200], [550, 450, 250, 10], [300, 250, 10, 150],
              [210, 400, 250, 10], [100, 200, 10, 200], [450, 140, 100, 10], [450, 10, 10, 140]]
        for coord in wall_coord:
            wall = Wall(coord[0], coord[1], coord[2], coord[3])
            wall_list.add(wall)
            all_sprite_list.add(wall)

        coin_coord = [[300, 70], [120, 250], [350, 450], [20, 550]]
        for coord in coin_coord:
            coin = Coin(coord[0], coord[1])
            coin_list.add(coin)
            all_sprite_list.add(coin)

        # Создаем противника
        enemies_list = pygame.sprite.Group()
        enemies_coord = [[25, 500], [300, 100]]
        for coord in enemies_coord:
            enemy = Enemy(coord[0], coord[1])
            enemies_list.add(enemy)
            all_sprite_list.add(enemy)

        player = Player(150, 150)
        player.walls = wall_list
        player.coin = coin_list
        all_sprite_list.add(player)
        player.enemies = enemies_list

        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 5
                    elif event.key == pygame.K_UP:
                        player.change_y = -5
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0

            screen.fill(PINK)
            if not player.alive:
                end.play()
                un = unwinner
                un.okno(self, 4)
            else:
                all_sprite_list.update()
                all_sprite_list.draw(screen)
            if player.pobeda:
                win.play()
                screen.blit(text_vin, (100, 100))
                k = urov_5
                k.ur(self)
            pygame.display.flip()
            clock.tick(60)


# Уровень 5
class urov_5():
    def ur(self):
        pygame.init()
        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('Тимошка')

        all_sprite_list = pygame.sprite.Group()
        wall_list = pygame.sprite.Group()
        coin_list = pygame.sprite.Group()
        wall_coord = [[0, 0, 10, 600], [790, 0, 10, 600], [10, 0, 790, 10],
                      [0, 200, 100, 10], [0, 590, 600, 10], [450, 400, 10, 200], [550, 450, 250, 10],
                      [300, 250, 10, 150],
                      [210, 400, 250, 10], [100, 200, 10, 200], [450, 140, 220, 10], [450, 10, 10, 140],
                      [670, 140, 10, 130], [290, 0, 10, 150],
                      [530, 270, 150, 10], [550, 400, 10, 50], [210, 410, 10, 70], [210, 480, 70, 10]]
        for coord in wall_coord:
            wall = Wall(coord[0], coord[1], coord[2], coord[3])
            wall_list.add(wall)
            all_sprite_list.add(wall)

        coin_coord = [[300, 70], [120, 250], [350, 450], [430, 170], [10, 250], [35, 500], [35, 35], [480, 40], [690, 390]]
        for coord in coin_coord:
            coin = Coin(coord[0], coord[1])
            coin_list.add(coin)
            all_sprite_list.add(coin)

        # Создаем противника
        enemies_list = pygame.sprite.Group()
        enemies_coord = [[25, 500], [300, 100], [510, 490]]
        for coord in enemies_coord:
            enemy = Enemy(coord[0], coord[1])
            enemies_list.add(enemy)
            all_sprite_list.add(enemy)
        player = Player(150, 150)
        player.walls = wall_list
        player.coin = coin_list
        all_sprite_list.add(player)
        player.enemies = enemies_list
        clock = pygame.time.Clock()
        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.change_x = -5
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 5
                    elif event.key == pygame.K_UP:
                        player.change_y = -5
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        player.change_x = 0
                    elif event.key == pygame.K_RIGHT:
                        player.change_x = 0
                    elif event.key == pygame.K_UP:
                        player.change_y = 0
                    elif event.key == pygame.K_DOWN:
                        player.change_y = 0

            screen.fill(PINK)
            if not player.alive:
                end.play()
                un = unwinner
                un.okno(self, 5)
            else:
                all_sprite_list.update()
                all_sprite_list.draw(screen)
            if player.pobeda:
                win.play()
                screen.blit(text_vin, (100, 100))
                p = final
                p.fin(self)
            pygame.display.flip()
            clock.tick(60)




# Класс начальное меню
class Menu:
    def menu1(self):
        pygame.init()
        pygame.display.set_caption('Timosha')
        widow_surface = pygame.display.set_mode((800, 600))
        background = pygame.Surface((800, 600))
        background.fill(pygame.Color("#94ffd6"))
        manager = pygame_gui.UIManager((800, 600))
        urov = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 75), (300, 100)), text="Правила",
                                            manager=manager)
        urov1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 250), (300, 100)),
                                             text="Cтарт", manager=manager)
        clock = pygame.time.Clock()
        run = True
        while run:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == urov:
                            pravila1 = Pravila
                            pravila1.pravila(self)
                        if event.ui_element == urov1:
                            uro = urov_1
                            uro.ur1(self)
                manager.process_events(event)
            manager.update(time_delta)
            widow_surface.blit(background, (0, 0))
            manager.draw_ui(widow_surface)
            pygame.display.update()
        pygame.quit()


pygame.init()
screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 50
clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Спаси домик", "Пандочки Тимоши",]
    fon = pygame.transform.scale(load_image('fon.png'), (800, 600))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 70)
    text_coord = 95
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(0, 107, 60))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    men = Menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                men.menu1()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()
