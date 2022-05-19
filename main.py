import pygame
import math

PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "game1"

SPEED = 5
XSTRETCH = 10
YSTRETCH = 8

SENSITIVITY = -0.015


class Block(pygame.sprite.Sprite):
    def __init__(self, w: int, h: int, x: int, y: int):
        # Call superclass constructor
        super().__init__()

        self.image = pygame.Surface([w, h])
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Initialize Sprite
        self.image = pygame.Surface([20, 20])
        self.image = self.image.convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300

        # Vector
        self.vel_x = 0
        self.vel_y = 0

        self.movedir = PI   # radians [0, 2pi], movement direction
        self.facedir = 0   # radians [0, 2pi], looking direction
        self.vel = 0

    def update(self):
        if self.movedir < 0:
            self.movedir = self.movedir + 2*PI

        if self.movedir > 2*PI:
            self.movedir = self.movedir - 2*PI

        if self.facedir < 0:
            self.facedir = self.facedir + 2*PI

        if self.facedir > 2*PI:
            self.facedir = self.facedir - 2*PI

        self.rect.x += math.cos(self.movedir) * self.vel
        self.rect.y += math.sin(self.movedir) * self.vel


class RenderObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Initialize Sprite
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))

        self.rect = self.image.get_rect()


def main():
    pygame.init()
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # Create an all_sprites_group object
    all_sprites_group = pygame.sprite.Group()
    block_group = pygame.sprite.Group()

    block1 = Block(20, 20, 200, 200)
    block2 = Block(20, 20, 300, 400)
    player = Player()
    obj1 = RenderObject()

    all_sprites_group.add(block1, block2, player, obj1)
    block_group.add(block1, block2)

    # ----- MAIN LOOP
    while not done:
        # -- Collision\

        # -- Event Handler

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                done = True

            if not done:
                pos = pygame.mouse.get_pos()

                pygame.mouse.set_pos([150, 150])
                pygame.mouse.set_visible(False)
                pygame.event.set_grab(True)

                player.movedir += (150 - pos[0]) * SENSITIVITY
                player.facedir += (150 - pos[0]) * SENSITIVITY

                print(player.facedir)

                if events.type == pygame.KEYDOWN:  # Movements need a bit of fixing for concurrent inputs
                    if events.key == pygame.K_RIGHT:
                        player.vel = SPEED
                        player.movedir += PI
                    elif events.key == pygame.K_LEFT:
                        player.vel = SPEED
                    elif events.key == pygame.K_UP:
                        player.vel = SPEED
                        player.movedir += PI / 2
                    elif events.key == pygame.K_DOWN:
                        player.vel = SPEED
                        player.movedir -= PI / 2

                if events.type == pygame.KEYUP:
                    if events.key == pygame.K_RIGHT:
                        player.vel = 0
                        player.movedir -= PI
                    if events.key == pygame.K_LEFT:
                        player.vel = 0
                    if events.key == pygame.K_UP:
                        player.vel = 0
                        player.movedir -= PI / 2
                    if events.key == pygame.K_DOWN:
                        player.vel = 0
                        player.movedir += PI / 2

        # ----- RENDER 3D OBJECTS
        # assuming player always facing north
        obj1.image.fill((0, 0, 0, 0))

        for block in block_group:
            sides = [(block.rect.topleft, block.rect.topright), (block.rect.topleft, block.rect.bottomleft),
                     (block.rect.topright, block.rect.bottomright), (block.rect.bottomleft, block.rect.bottomright)]

            for side in sides:
                x = -(player.rect.centerx - side[0][0])
                z = player.rect.centery - side[0][1]

                if x == 0:
                    x = -0.0000000000000001

                leftside = math.atan(z/x)

                if x < 0 and z > 0:
                    leftside = PI + leftside
                elif x < 0 and z < 0:
                    leftside = PI + leftside

                if leftside > -player.facedir > leftside - PI or leftside > 2 * PI - player.facedir > leftside - PI :
                    points = []

                    itside = 0
                    invy = 1

                    for i in range(4):
                        x = -(player.rect.centerx - side[itside][0])
                        z = player.rect.centery - side[itside][1]

                        if x == 0:
                            x = -0.0000000000000001

                        angle = math.atan(z/x)

                        if x < 0 and z > 0:
                            angle = PI + angle
                        elif x < 0 and z < 0:
                            angle = PI + angle

                        angle = angle + player.facedir

                        d = math.sqrt(x * x + z * z)

                        x = d * math.cos(angle)
                        z = d * math.sin(angle)

                        y = invy * 50
                        d = math.sqrt(x * x + z * z + y * y)
                        points.append((WIDTH / 2 + x * d / (z + d) * XSTRETCH, HEIGHT / 2 + y * d / (z + d) * YSTRETCH))

                        if i == 0:
                            invy = -1
                        elif i == 1:
                            itside = 1
                        elif i == 2:
                            invy = 1

                    d = math.sqrt(x * x + z * z + y * y)

                    if d > 150:
                        d = 150

                    pygame.draw.polygon(obj1.image, (d, d, d), points)

        # ----- LOGIC

        # Update all sprites
        all_sprites_group.update()

        # ----- RENDER
        screen.fill(WHITE)
        pygame.draw.rect(screen, SKY_BLUE, (0, 0, WIDTH, HEIGHT/2))

        all_sprites_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
