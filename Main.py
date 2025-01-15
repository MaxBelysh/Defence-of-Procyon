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
    def __init__(self):
        self.images = os.listdir()
        self.size = (800, 600)
        self.y_pos1 = 0
        self.y_pos2 = -600
        self.image1 = pygame.transform.scale(load_image("cosmos.png"), self.size)
        self.image2 = pygame.transform.scale(load_image("cosmos.png"), self.size)
        self.alternation = 0

    def update_background(self, screen):
        screen.blit(self.image1, (0, self.y_pos1))
        screen.blit(self.image2, (0, self.y_pos2))
        self.y_pos1 += 0.1
        self.y_pos2 += 0.1
        if self.alternation == 0:
            if self.y_pos2 == 0:
                self.y_pos1 = -600
                self.alternation = 1
        else:
            if self.y_pos1 == 0:
                self.y_pos2 = -600
                self.alternation = 0




if __name__ == "__main__":
    pygame.init()
    width, height = size = 800, 600
    screen = pygame.display.set_mode(size)
    background = GameLevel()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        background.update_background(screen)
        pygame.display.flip()

    pygame.quit()

