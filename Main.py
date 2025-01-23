import math
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
        self.background_speed = 0.1

    def update_background(self, screen):
        # добавить зависимость от fps
        screen.fill((0, 0, 0))
        screen.blit(self.image1, (0, self.y_pos1))
        screen.blit(self.image2, (0, self.y_pos2))
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

    def set_max_score(self):
        pass


class Entity(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.health = 999
        self.image = pygame.transform.scale(load_image("none.png", "entity", color_key=-1), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.health <= 0:
            self.kill()


class Enemy(Entity):
    pass


class Player(Entity):
    def __init__(self, group, x, y):
        super().__init__(group, x, y)
        self.health = 3
        self.image = load_image("plane.png", "entity", color_key=-1)
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 300

    def update(self):
        pass

    def update_pos(self, pos):
        # привязать мышь к кораблю, скрыть мышь, не давать мыши выходить за рамки экрана
        if 0 <= pos[0] - self.rect.width // 2 and pos[0] + self.rect.width // 2 <= WIDTH:
            self.rect.x = pos[0] - self.rect.width // 2
        if 0 <= pos[1] - self.rect.height // 2 and pos[1] + self.rect.height // 2 <= HEIGHT:
            self.rect.y = pos[1] - self.rect.height // 2

        # path = round(math.sqrt((pos[0] - self.rect.width // 2 - self.rect.x) ** 2 + (pos[1] - self.rect.height // 2 - self.rect.y) ** 2), 5)
        # time = round(path / self.speed, 5)
        # if 0 <= self.rect.x - self.rect.width // 2 and self.rect.x + self.rect.width // 2 <= WIDTH:
        #     self.rect.x += round((((pos[0] - self.rect.width // 2) - self.rect.x) / time) / 1000, 3)
        # if 0 <= self.rect.y - self.rect.height // 2 and self.rect.y + self.rect.height // 2 <= HEIGHT:
        #     self.rect.y += round((((pos[1] - self.rect.height // 2) - self.rect.y) / time) / 1000, 3)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("none.png", "entity", color_key=-1), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = 0
        self.speed = 0


if __name__ == "__main__":
    pygame.init()

    WIDTH = 1000
    HEIGHT = 600

    pygame.event.set_grab(True)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    GameScene = GameScene(WIDTH, HEIGHT)
    all_sprites = pygame.sprite.Group()
    player_sprite_group = pygame.sprite.Group()
    player = Player(player_sprite_group, 100, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                player.update_pos(event.pos)
        GameScene.update_background(screen)
        player_sprite_group.draw(screen)
        pygame.display.flip()

    if GameScene.get_max_score() > int(open("max_score.csv", encoding="utf-8").read().split("\n")[1]):
        with open("max_score.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["max score"])
            writer.writerow([str(GameScene.get_max_score())])

    pygame.quit()

