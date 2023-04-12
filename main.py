import pygame
from os import listdir
from os.path import join, isfile

pygame.init()
fps = 60
player_vel = 5
Width, Height = 1000, 800
screen = pygame.display.set_mode((Width, Height))


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(surface)

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.direction = "left"
        self.fall_count = 0
        self.animation_count = 0

    red_color = (255, 0, 0)
    gravity = 0
    SPRITES = load_sprite_sheets("MainCharacters", "NinjaFrog", 32, True)
    animation_delay = 3

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
        self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
        self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.gravity)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1

    def draw(self, window):
        pygame.draw.rect(window, self.red_color, self.rect)


def background_info(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []
    for i in range(Width // width + 1):
        for j in range(Height // height + 1):
            pos = [i * width, j * height]
            tiles.append(pos)
    return tiles, image


def draw(window, tiles, image, player):
    for pos in tiles:
        window.blit(image, tuple(pos))
    player.draw(screen)
    pygame.display.update()


def movement_controlls(player):
    keys = pygame.key.get_pressed()
    player.x_vel = 0
    if keys[pygame.K_LEFT]:
        player.move_left(player_vel)
    if keys[pygame.K_RIGHT]:
        player.move_right(player_vel)


def main(screen):
    clock = pygame.time.Clock()
    tiles_location, background_image = background_info("Green.png")

    player = Player(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        movement_controlls(player)
        player.loop(fps)
        draw(screen, tiles_location, background_image, player)

    pygame.quit()


if __name__ == "__main__":
    main(screen)

# print([i for i in range(10)])