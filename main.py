import pygame
from random import randint, choice
from pygame.locals import *

if __name__ == '__main__':
    pygame.init()
    size = width, height = 1920, 1080
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('data/star_wars.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
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
death_img = pygame.image.load("data/gameOver.png")
death_rect = death_img.get_rect()
death_rect.x = 800
death_rect.y = 100
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
scull = pygame.image.load('data/scull.png')
scull_react = scull.get_rect(center=(1715, 1037))


def draw_explosion(enmy):
    global explosion_pngs

    if got_top:
        if enmy.explosionAnimCount >= 180:
            enmy.explosionAnimCount = 0
            enmy.explosioned = True
            explosioningEnemies.remove(enmy)

        if not enmy.explosioned:
            screen.blit(explosion_pngs[enmy.explosionAnimCount // 15], [enmy.x, enmy.y])
            enmy.explosionAnimCount += 1


def drop_heart(enmy):
    if got_top:
        screen.blit(heart, [enmy.x, enmy.y])


class DroppingHeart:
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.borders = [x - 100, x + 20]
        self.hrt_sprite = pygame.sprite.Group()
        self.heart_sprite = pygame.sprite.Sprite()
        self.hrt_sprite.add(self.heart_sprite)
        self.heart_sprite.image = pygame.image.load(f"data/{filename}")
        self.heart_sprite.rect = self.heart_sprite.image.get_rect()
        self.heart_sprite.rect.x = self.x
        self.heart_sprite.rect.y = self.y
        self.direction = "left"
        if filename == "heart.png":
            self.hpUP = 20
        else:
            self.hpUP = 100

    def draw_heart(self):
        if self.direction == "left":
            self.heart_sprite.rect.x -= 1
        else:
            self.heart_sprite.rect.x += 1
        self.heart_sprite.rect.y += 1
        if self.heart_sprite.rect.x >= self.borders[1]:
            self.direction = "left"
        elif self.heart_sprite.rect.x <= self.borders[0]:
            self.direction = "right"
        self.hrt_sprite.draw(screen)


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
        self.borders = (x, x + 200)
        self.hp = health_points
        self.cnt = 0
        self.drct = ["right", "left"]
        self.sprite_check = pygame.sprite.Group()
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("data/start_button.png")
        self.sprite.rect = self.sprite.image.get_rect()
        self.sprite.rect.x = self.x
        self.sprite.rect.y = self.y + 10
        self.sprite.rect.width -= 100
        self.sprite_check.add(self.sprite)
        self.alive = True
        self.explosioned = False
        self.move_direction = "right"
        self.explosionAnimCount = 0

    def draw_enemy(self, scr):
        if self.animCount >= 64:
            self.animCount = 0

        if self.alive:
            scr.blit(self.sprite_list[self.animCount // 16], [self.x, self.y])
            self.animCount += 1

    def check_death(self):
        global score
        global count_kill
        # global new_enemy
        if self.alive:
            if self.hp <= 0:
                count_kill += 1
                self.alive = False
                self.sprite.kill()
                explosioningEnemies.append(self)
                if self.explosioned:
                    enemies.remove(self)
                if count_kill <= 5:
                    enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                elif count_kill <= 10:
                    if (len(enemies) - len(explosioningEnemies)) == 1:
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                    elif (len(enemies) - len(explosioningEnemies)) == 0:
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                else:
                    if (len(enemies) - len(explosioningEnemies)) == 2:
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                    elif (len(enemies) - len(explosioningEnemies)) == 1:
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                        enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                score += 10
                if randint(0, 5) == 1:
                    if randint(0, 10) == 1:
                        droppingHearts.append(DroppingHeart(self.x, self.y, "goldenheart.png"))
                    else:
                        droppingHearts.append(DroppingHeart(self.x, self.y, "heart.png"))
        else:
            if self.explosioned:
                enemies.remove(self)

    def check_damage(self, sprite_group):
        if self.alive:
            if pygame.sprite.spritecollideany(self.sprite, sprite_group) != None:
                sprts = sprite_group.sprites()
                self.hp -= sprts[0].damage
                sprite_group.remove(pygame.sprite.spritecollideany(self.sprite, sprite_group))

    def move(self):
        if self.alive:
            if 0 <= self.borders[0] <= 500 or 1400 <= self.borders[0] <= 1920:
                if self.y < 200:
                    self.y += 2
                else:
                    if self.drct[self.cnt // 200 % 2] == "right":
                        self.x += 1
                    else:
                        self.x -= 1
                    self.cnt += 1
            else:
                if self.y < 100:
                    self.y += 2
                else:
                    if self.drct[self.cnt // 200 % 2] == "right":
                        self.x += 1
                    else:
                        self.x -= 1
                    self.cnt += 1


# константы или переменные, которые просто есть и нужны для рассчетов
spaceShip = [pygame.transform.rotate(i, 180) for i in pngs]
pressed = False
paused = False
flipped = False
dead = False
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
count_kill = 0
enemies = []
explosioningEnemies = []
droppingHearts = []
HP = 100
die = False


class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(MainCharacter, self).__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("data/animated_spaceship/frame1.png")
        self.rect = self.image.get_rect(center=(x, y))
        self.HP = 100
        self.character_sprite = pygame.sprite.Sprite()
        self.character_sprite.image = pygame.image.load("data/animated_spaceship/frame1.png")
        self.character_sprite.rect = self.character_sprite.image.get_rect()
        self.rect = self.image.get_rect()
        self.character_sprite.rect.x = x
        self.character_sprite.rect.y = y
        self.character_sprite.rect.width -= 70

    def check_damage_main(self, sprite_group):
        if pygame.sprite.spritecollideany(self.character_sprite, sprite_group) != None:
            pygame.sprite.spritecollideany(self.character_sprite, sprite_group).kill()
            person.HP -= 10

    def checkHpUP(self, spriteGroup, obj):
        if pygame.sprite.spritecollideany(self.character_sprite, spriteGroup) != None:
            sprts = spriteGroup.sprites()
            person.HP += obj.hpUP
            if person.HP >= 200:
                person.HP = 200
            pygame.sprite.spritecollideany(self.character_sprite, spriteGroup).kill()

    def death(self):
        global die
        if self.HP <= 0:
            self.character_sprite.kill()
            die = True

    @staticmethod
    def draw_ship():
        global animCount
        if animCount >= 64:
            animCount = 0

        screen.blit(spaceShip[animCount // 16], [main_ship_x, main_ship_y])
        animCount += 1


enemies.append(Enemy("blue_enemy", 870, 100, 100))
person = MainCharacter(870, 700)


# def del_enemy(terrorist):
#     enemies.remove(terrorist)


def update(im, *args):
    global pressed
    if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
            im.rect.collidepoint(args[0].pos):
        pressed = True


while running:
    for bul in bullets.sprites():
        if bul.y < 0 or bul.y > 1080:
            bul.kill()
    for enbul in enemy_bullets.sprites():
        if enbul.y < 0 or enbul.y > 1080:
            enbul.kill()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if not paused:
                    pygame.mixer.music.unpause()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if not die:
                if 820 <= x <= 1110 and 390 <= y <= 540:
                    paused = False
                    pygame.mixer.music.unpause()
                elif 820 <= x <= 1120 and 640 <= y <= 770:
                    running = False
            else:
                if 820 <= x <= 1120 and 770 <= y <= 900:
                    running = False
                elif 700 <= x <= 1252 and 600 <= y <= 730:
                    pygame.mixer.music.unpause()
                    person.HP = 100
                    die = False
                    count_kill = 0
                    score = 0
                    droppingHearts = []
                    enemies.clear()
                    enemies.append(Enemy("blue_enemy", randint(300, 1000), -100, 100))
                    bullets.empty()
                    enemy_bullets.empty()
                    main_ship_x, main_ship_y = 870, 700
                    person.character_sprite.rect.x = 870
                    person.character_sprite.rect.y = 700
    if die:
        game_over_sprites = pygame.sprite.Group()
        game_over_image = pygame.sprite.Sprite()
        game_over_image.image = pygame.image.load('data/gameOver.png')
        game_over_image.rect = game_over_image.image.get_rect()
        game_over_image.rect.x = 710
        game_over_image.rect.y = 100
        game_over_sprites.add(game_over_image)
        game_over_sprites.draw(screen)
        pygame.mixer.music.pause()
        pause_sprites = pygame.sprite.Group()
        exit_button = pygame.sprite.Sprite()
        exit_button.image = pygame.image.load('data/exit_button.png')
        exit_button.rect = exit_button.image.get_rect()
        exit_button.rect.x = 810
        exit_button.rect.y = 770
        tryAgain_button = pygame.sprite.Sprite()
        tryAgain_button.image = pygame.image.load('data/tryAgain.png')
        tryAgain_button.rect = tryAgain_button.image.get_rect()
        tryAgain_button.rect.x = 690
        tryAgain_button.rect.y = 600
        pause_sprites.add(tryAgain_button)
        pause_sprites.add(exit_button)
        pause_sprites.draw(screen)
        if not flipped:
            pygame.display.flip()
            flipped = True
    elif not paused:
        flipped = False
        for bullet in bullets:
            bullet.draw_bullet(screen)
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw_bullet(screen)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and main_ship_x < 1830:
            person.character_sprite.rect.x += 4
            main_ship_x += 4
        if keys[pygame.K_d] and main_ship_x < 1830:
            person.character_sprite.rect.x += 4
            main_ship_x += 4
        if keys[pygame.K_LEFT] and main_ship_x > 5:
            person.character_sprite.rect.x -= 4
            main_ship_x -= 4
        if keys[pygame.K_a] and main_ship_x > 5:
            person.character_sprite.rect.x -= 4
            main_ship_x -= 4
        if keys[pygame.K_UP] and main_ship_y > 10:
            person.character_sprite.rect.y -= 4
            main_ship_y -= 4
        if keys[pygame.K_w] and main_ship_y > 10:
            person.character_sprite.rect.y -= 4
            main_ship_y -= 4
        if keys[pygame.K_DOWN] and main_ship_y < 950:
            person.character_sprite.rect.y += 4
            main_ship_y += 4
        if keys[pygame.K_s] and main_ship_y < 950:
            person.character_sprite.rect.y += 4
            main_ship_y += 4
        # bullets.add() добавляет, логично, пули
        if keys[pygame.K_SPACE]:
            if fire_stop == 0 and got_top and not dead:
                bullets.add(Bullet(main_ship_x + 20, main_ship_y, bullet_image, 10))
                bullets.add(Bullet(main_ship_x + 35, main_ship_y, bullet_image, 10))
        if enemy_fire_stop == 0 and got_top and len(enemies) != 0:
            for enemy in enemies:
                if enemy.alive:
                    enemy_bullets.add(Bullet(enemy.x + 45, enemy.y + 85, enemy_bullet_im, 10, "enemy"))
                    enemy_bullets.add(Bullet(enemy.x + 70, enemy.y + 85, enemy_bullet_im, 10, "enemy"))
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
            person.check_damage_main(enemy_bullets)
            person.draw_ship()
            person.death()

            for enemy in enemies:
                enemy.draw_enemy(screen)
            # создается надпись SCORE для счета
            font = pygame.font.Font("data/karmafuture.ttf", 45)
            text = font.render(
                "Kills:" + str(score // 10), True, (255, 255, 255))
            place = text.get_rect(
                center=(1815, 1030))
            screen.blit(text, place)
        fire_stop += 1
        enemy_fire_stop += 1
        if fire_stop == 27:
            fire_stop = 0
        if enemy_fire_stop == 180:
            enemy_fire_stop = 0
        # отрисовывается все, что есть на экране
        bullets.draw(screen)
        enemy_bullets.draw(screen)
        for enemy in enemies:
            if not enemy.alive:
                enemy.explosionAnimCount += 1
            enemy.check_damage(bullets)
            enemy.check_death()
            enemy.move()
        for enemy in explosioningEnemies:
            draw_explosion(enemy)
        heart_x = 50
        heart_y = 1000
        if got_top:
            for i in range(person.HP // 20):
                heart = pygame.image.load('data/heart.png')
                heart_react = heart.get_rect(center=(heart_x, heart_y))
                heart_x += 40
                screen.blit(heart, heart_react)
                screen.blit(scull, scull_react)
            for ht in droppingHearts:
                ht.draw_heart()
                person.checkHpUP(ht.hrt_sprite, ht)
        pygame.display.flip()
        clock.tick(120)
    else:
        pygame.mixer.music.pause()
        pause_sprites = pygame.sprite.Group()
        pause_image = pygame.sprite.Sprite()
        back = pygame.sprite.Sprite()
        exit_button = pygame.sprite.Sprite()
        exit_button.image = pygame.image.load('data/exit_button.png')
        back.image = pygame.image.load('data/back_button.png')
        pause_image.image = pygame.image.load('data/pause_background.png')
        pause_image.rect = pause_image.image.get_rect()
        pause_image.rect.x = 0
        pause_image.rect.y = 0
        back.rect = back.image.get_rect()
        back.rect.x = 820
        back.rect.y = 390
        exit_button.rect = exit_button.image.get_rect()
        exit_button.rect.x = 820
        exit_button.rect.y = 640
        pause_sprites.add(pause_image)
        pause_sprites.add(back)
        pause_sprites.add(exit_button)
        pause_sprites.draw(screen)
        if not flipped:
            pygame.display.flip()
            flipped = True
