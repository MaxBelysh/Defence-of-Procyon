import os
import sys
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
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


class GameLevel:
    def __init__(self, width, height):
        self.images = os.listdir()
        self.width = width
        self.height = height
        self.size = width, height
        self.y_pos1 = 0
        self.y_pos2 = -height
        self.image1 = pygame.transform.scale(load_image("cosmos.png"), self.size)
        self.image2 = pygame.transform.scale(load_image("cosmos.png"), self.size)
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
                self.alternation = 2
        else:
            if self.y_pos2 >= self.height:
                self.y_pos2 = -self.height
                self.alternation = 1


if __name__ == "__main__":
    pygame.init()
    width, height = size = 800, 600
    screen = pygame.display.set_mode(size)
    GameLevel = GameLevel(width, height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        GameLevel.update_background(screen)
        pygame.display.flip()

    pygame.quit()

