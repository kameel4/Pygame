import os
import sys
import pygame
from pygame.locals import *

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)

# ниже идет создание спрайтов и групп спрайтов
all_sprites = pygame.sprite.Group()
sprites = ["data/space_background", "data/start_button.png"]
background = pygame.sprite.Sprite()
background.image = pygame.image.load("data/normal_space.png")
background.rect = background.image.get_rect()
background.rect.x = 0
background.rect.y = -200
all_sprites.add(background)
start_button = pygame.sprite.Sprite()
start_button.image = pygame.image.load("data/start_button.png")
start_button.rect = start_button.image.get_rect()
start_button.rect.x = 770
start_button.rect.y = 400
# немножко повернем спрайты, чтобы они нормально выглядели
bullet_image = pygame.image.load("data/normal_bullet.png")
bullet_image = pygame.transform.rotate(bullet_image, 90)
enemy_bullet_im = pygame.image.load("data/enemy_bullet.png")
enemy_bullet_im = pygame.transform.rotate(enemy_bullet_im, -90)
# список кадров анимации главногго корабля
pngs = [
    pygame.image.load("data/animated_spaceship/frame1.png"),
    pygame.image.load("data/animated_spaceship/frame2.png"),
    pygame.image.load("data/animated_spaceship/frame3.png"),
    pygame.image.load("data/animated_spaceship/frame4.png"),
    pygame.image.load("data/animated_spaceship/frame5.png"),
    pygame.image.load("data/animated_spaceship/frame6.png"),
    pygame.image.load("data/animated_spaceship/frame7.png"),
    pygame.image.load("data/animated_spaceship/frame8.png"),
    pygame.image.load("data/animated_spaceship/frame9.png"),
]
explosion_pngs = []
for i in range(13):
    explosion_pngs.append(pygame.image.load(
        f"data/small_explosion/enemy_explosion{i}.png"
    ))
# группы спрайтов пуль гг и мобов
bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bul_x, bul_y, bul_im, bul_dmg, bul_team="character"):
        super(Bullet, self).__init__()
        self.x = bul_x
        self.y = bul_y
        self.image = bul_im
        self.damage = bul_dmg
        self.bul_sprite = pygame.sprite.Group()
        self.bullet_sprite = pygame.sprite.Sprite()
        self.bullet_sprite.image = pygame.image.load("data/normal_bullet.png")
        self.bullet_sprite.rect = self.bullet_sprite.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x = bul_x
        self.rect.y = bul_y
        self.team = bul_team

    def draw_bullet(self, scr):
        if self.team == "character":
            self.rect.y -= 5
        else:
            self.rect.y += 2
        scr.blit(self.image, [self.x, self.y])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, x, y, health_points):
        super(Enemy, self).__init__()
        self.sprite_lst = []
        self.type = enemy_type
        if self.type == "blue_enemy":
            self.frames_num = 6
            self.sprite_lst.append(pygame.image.load("data/animated_blue_enemy/blue_enemy.png"))
        for i in range(1, self.frames_num):
            self.sprite_lst.append(pygame.image.load(f"data/animated_blue_enemy/blue_enemy{i}.png"))
        self.sprite_list = [pygame.transform.rotate(i, 180) for i in self.sprite_lst]
        self.animCount = 0
        self.x, self.y = x, y
        self.hp = health_points
        self.sprite_check = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("data/start_button.png")
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y
        self.sprite_check.add(self.sprite)
        self.alive = True
        self.explosioned = False
        self.move_direction = "right"

    def draw_enemy(self, scr):
        if self.animCount >= 64:
            self.animCount = 0

        if self.alive:
            scr.blit(self.sprite_list[self.animCount // 16], [self.x, self.y])
            self.animCount += 1

    def draw_explosion(self):
        global explosionAnimCount, explosion_pngs

        if explosionAnimCount >= 130:
            explosionAnimCount = 0
            self.explosioned = True

        if not self.explosioned and not self.alive:
            screen.blit(explosion_pngs[explosionAnimCount // 10], [self.x, self.y])
            explosionAnimCount += 1

    def check_death(self):
        global score
        if self.alive:
            if self.hp <= 0:
                self.alive = False
                self.sprite.kill()
                score += 10

    def check_damage(self, sprite_group):
        if self.alive:
            if pygame.sprite.spritecollideany(self.sprite, sprite_group) != None:
                sprts = sprite_group.sprites()
                self.hp -= sprts[0].damage
                sprts[0].kill()
                sprts[1].kill()

    def move(self):
        if self.move_direction == "right":
            self.x += 1
            if self.x == 950:
                self.move_direction = "left"
        elif self.move_direction == "left":
            self.x -= 1
            if self.x == 790:
                self.move_direction = "right"


# константы или переменные, которые просто есть и нужны для рассчетов
spaceShip = [pygame.transform.rotate(i, 180) for i in pngs]
pressed = False
animCount = 0
explosionAnimCount = 0
all_sprites.add(start_button)
clock = pygame.time.Clock()
running = True
count = -200
dif = 1
going_down = False
got_top = False
fire_stop = 0
enemy_fire_stop = 0
main_ship_x = 870
main_ship_y = 700
score = 0
first_enemy = Enemy("blue_enemy", 870, 100, 100)


def update(im, *args):
    global pressed
    if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
            im.rect.collidepoint(args[0].pos):
        pressed = True


def draw_ship():
    global animCount

    if animCount >= 64:
        animCount = 0

    screen.blit(spaceShip[animCount // 16], [main_ship_x, main_ship_y])
    animCount += 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for bullet in bullets:
        bullet.draw_bullet(screen)
    for enemy_bullet in enemy_bullets:
        enemy_bullet.draw_bullet(screen)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and main_ship_x < 1830:
        main_ship_x += 4
    if keys[pygame.K_LEFT] and main_ship_x > 5:
        main_ship_x -= 4
    if keys[pygame.K_UP] and main_ship_y > 10:
        main_ship_y -= 4
    if keys[pygame.K_DOWN] and main_ship_y < 950:
        main_ship_y += 4
# bullets.add() добавляет, логично, пули
    if keys[pygame.K_SPACE]:
        if fire_stop == 0 and got_top:
            bullets.add(Bullet(main_ship_x + 20, main_ship_y, bullet_image, 10))
            bullets.add(Bullet(main_ship_x + 35, main_ship_y, bullet_image, 10))
    if enemy_fire_stop == 0 and got_top and first_enemy.alive:
        enemy_bullets.add(Bullet(first_enemy.x + 45, first_enemy.y + 85, enemy_bullet_im, 10, "enemy"))
        enemy_bullets.add(Bullet(first_enemy.x + 70, first_enemy.y + 85, enemy_bullet_im, 10, "enemy"))
    if pressed:
        start_button.kill()
        going_down = True
        pressed = False
    if going_down:
        background.rect.y += dif
        count += dif
    if count == 0:
        dif = 0
        got_top = True
    all_sprites.draw(screen)
    update(start_button, event)
    # Фон достиг верха экрана (got top) и игра началась
    if got_top:
        draw_ship()
        first_enemy.draw_enemy(screen)
        first_enemy.draw_explosion()
# создается надпись SCORE для счета
        font = pygame.font.Font("data/karmafuture.ttf", 45)
        text = font.render(
            "Score:" + str(score), True, (255, 255, 255))
        place = text.get_rect(
            center=(1815, 1030))
        screen.blit(text, place)
    fire_stop += 1
    enemy_fire_stop += 1
    if fire_stop == 27:
        fire_stop = 0
    if enemy_fire_stop == 180:
        enemy_fire_stop = 0
    for bul in bullets.sprites():
        if bul.y < 0 or bul.y > 1080:
            bul.kill()
# отрисовывается все, что есть на экране
    bullets.draw(screen)
    enemy_bullets.draw(screen)
    first_enemy.check_damage(bullets)
    first_enemy.check_death()
    first_enemy.move()
    pygame.display.flip()
    clock.tick(144)
