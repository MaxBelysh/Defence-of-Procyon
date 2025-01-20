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

    def update(self):
        pass


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
        self.background_speed = 0.5

    def update_background(self, screen):
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


if __name__ == "__main__":
    pygame.init()
    width, height = size = 1000, 600
    screen = pygame.display.set_mode(size)
    GameScene = GameScene(width, height)
    all_sprites = pygame.sprite.Group()
    player = Player(all_sprites, 100, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        GameScene.update_background(screen)
        all_sprites.draw(screen)
        pygame.display.flip()

    if GameScene.get_max_score() > int(open("max_score.csv", encoding="utf-8").read().split("\n")[1]):
        with open("max_score.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(["max score"])
            writer.writerow([str(GameScene.get_max_score())])

    pygame.quit()

