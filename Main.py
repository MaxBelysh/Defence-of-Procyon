import random
import os
import sys
import pygame
import csv


def load_image(name, directory, color_key=None):
    fullname = os.path.join("data/" + directory, name)
    if not os.path.isfile(fullname):
        print(f"file with image '{fullname}' not found")
        sys.exit()
    else:
        image = pygame.image.load(fullname)

    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
            image.set_colorkey(color_key)
        else:
            image.convert_alpha()
    return image


class GameScene:
    def __init__(self, width, height):
        # GameScene
        self.score = 0
        self.max_score = int(open("max_score.csv", encoding="utf-8").read().split("\n")[1])
        self.timer = 0
        self.moment = True
        self.time = 0

        # GameLevel
        self.images = os.listdir("data/background")
        self.width = width
        self.height = height
        self.size = width, height
        self.number_of_image = 1
        self.y_pos1 = 0
        self.y_pos2 = -height
        self.image1 = pygame.transform.scale(load_image(self.images[0], "background"), self.size)
        self.image2 = pygame.transform.scale(load_image(self.images[1], "background"), self.size)
        self.alternation = 1
        self.background_speed = 1 * clock.tick() / 1000

    def update_background(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.image1, (0, int(self.y_pos1)))
        screen.blit(self.image2, (0, int(self.y_pos2)))
        self.y_pos1 += self.background_speed
        self.y_pos2 += self.background_speed
        if self.alternation == 1:
            if self.y_pos1 >= self.height:
                self.y_pos1 = -self.height
                if self.number_of_image == len(self.images) - 1:
                    self.number_of_image = 0
                else:
                    self.number_of_image += 1
                self.image1 = pygame.transform.scale(load_image(self.images[self.number_of_image], "background"), self.size)
                self.alternation = 2
        else:
            if self.y_pos2 >= self.height:
                self.y_pos2 = -self.height
                if self.number_of_image == len(self.images) - 1:
                    self.number_of_image = 0
                else:
                    self.number_of_image += 1
                self.image2 = pygame.transform.scale(load_image(self.images[self.number_of_image], "background"), self.size)
                self.alternation = 1

    def get_max_score(self):
        return self.max_score

    def update(self):
        if int(self.timer) % 5 == 0:
            if int(self.timer) == self.time:
                if self.moment:
                    self.spawn_meteorites()
                    self.moment = False
            else:
                self.time = int(self.timer)
                self.moment = True
        self.timer += clock.tick() / 1000

    def spawn_meteorites(self):
        meteorite = Meteorite(meteorite_sprite_group, random.randrange(0, WIDTH - 150), -150)


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.health = 999
        self.width = 100
        self.height = 100
        self.image = pygame.transform.scale(load_image("none.png", "entity", color_key=-1), (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y

    def update(self):
        if self.health <= 0:
            self.kill()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def get_size(self):
        return self.width, self.height

    def get_damage(self, damage):
        self.health -= damage


class Meteorite(Entity):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.width = 150
        self.height = 150
        self.health = 4
        self.image = pygame.transform.scale(load_image("meteorite.png", "entity", color_key=-1), (self.width, self.height))
        self.speed = 50 * clock.tick() / 1000

    def update(self):
        super().update()
        if self.rect.y > HEIGHT:
            self.kill()
        self.y += self.speed


class Player(Entity):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.health = 3
        self.image = pygame.transform.scale(load_image("plane.png", "entity", color_key=-1), (self.width, self.height))
        self.speed = 100 * clock.tick() / 1000
        self.cooldown = 0

    def update(self):
        super().update()
        if self.cooldown > 0:
            self.cooldown -= 1000 * clock.tick() / 1000
        elif self.cooldown < 0:
            self.cooldown = 0
        collided_meteorites = pygame.sprite.spritecollide(self, meteorite_sprite_group, False)
        if collided_meteorites:
            self.health -= 1
            for meteorite in collided_meteorites:
                meteorite.kill()

    def move_up(self):
        if 0 < self.y < self.speed:
            self.y += self.y - self.speed
        elif self.y >= self.speed:
            self.y += -self.speed

    def move_down(self):
        if HEIGHT - self.speed < self.y + self.rect.height < HEIGHT:
            self.rect.y = HEIGHT - self.rect.height
            self.y = self.rect.y
        elif self.y + self.rect.height <= HEIGHT - self.speed:
            self.y += self.speed

    def move_left(self):
        if 0 < self.x < self.speed:
            self.x += self.rect.x - self.speed
        elif self.x >= self.speed:
            self.x += - self.speed

    def move_right(self):
        if WIDTH - self.speed < self.x + self.rect.width < WIDTH:
            self.rect.x = WIDTH - self.rect.width
            self.x = self.rect.x
        elif self.x + self.rect.width <= WIDTH - self.speed:
            self.x += self.speed

    def shot(self):
        if self.cooldown == 0:
            rocket1 = PlayerProjectile(player_projectile_group, self.rect.x + self.rect.width // 2, self.rect.y )
            rocket2 = PlayerProjectile(player_projectile_group, self.rect.x, self.rect.y)
            self.cooldown = 300


class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.width = 50
        self.height = 50
        self.image = pygame.transform.scale(load_image("none.png", "entity", color_key=-1), (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.y = y
        self.damage = 0
        self.speed = 1 * clock.tick() / 1000

    def update(self):
        if self.rect.x + self.rect.width < 0 or self.rect.x - self.rect.width > WIDTH or \
            self.rect.y + self.rect.height < 0 or self.rect.y - self.rect.height > HEIGHT:
            self.kill()
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def get_size(self):
        return self.width, self.height


class PlayerProjectile(Projectile):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.image = pygame.transform.scale(load_image("rocket.png", "projectile", color_key=-1), (self.width, self.height))
        self.damage = 1
        self.speed = 100 * clock.tick() / 1000

    def update(self):
        super().update()
        collided_meteorites = pygame.sprite.spritecollide(self, meteorite_sprite_group, dokill=False)
        if collided_meteorites:
            self.kill()
            for meteorite in collided_meteorites:
                meteorite.get_damage(self.damage)
        self.y -= self.speed


if __name__ == "__main__":
    pygame.init()

    WIDTH = 1000
    HEIGHT = 600
    clock = pygame.time.Clock()

    pygame.event.set_grab(True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    GameScene = GameScene(WIDTH, HEIGHT)

    meteorite_sprite_group = pygame.sprite.Group()

    player_sprite_group = pygame.sprite.Group()
    player_projectile_group = pygame.sprite.Group()
    player = Player(player_sprite_group, 100, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.shot()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move_up()
        if keys[pygame.K_s]:
            player.move_down()
        if keys[pygame.K_d]:
            player.move_right()
        if keys[pygame.K_a]:
            player.move_left()

        GameScene.update()
        GameScene.update_background(screen)

        meteorite_sprite_group.update()

        player.update()
        player_projectile_group.update()

        meteorite_sprite_group.draw(screen)
        player_projectile_group.draw(screen)
        player_sprite_group.draw(screen)

        pygame.display.flip()

    if GameScene.get_max_score() > int(open("max_score.csv", encoding="utf-8").read().split("\n")[1]):
        with open("max_score.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["max score"])
            writer.writerow([str(GameScene.get_max_score())])

    pygame.quit()

