import pygame
import sys
import random

# TODO: CHANGE GRAPHICS
# TODO: IMPLEMENT GRAPHICS

pygame.init()
screen_width = 800
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Star Cat")
clock = pygame.time.Clock()

pixel_font = pygame.font.Font('font/ARCADECLASSIC.TTF', 20)

cat_img = pygame.image.load('graphics/cat.png').convert_alpha()
platform_img = pygame.image.load('graphics/platform.png').convert_alpha()
star_img = pygame.image.load('graphics/star.png').convert_alpha()
background_img = pygame.image.load('graphics/background.png')

class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(cat_img, (70, 70))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False
        self.gravity = 1
        self.scroll = 0
        self.score = 0

    def move(self):
        self.scroll = 0
        dir_x = 0
        dir_y = 0

        # left right movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            dir_x -= 10
            self.flip = False
        if keys[pygame.K_d]:
            dir_x += 10
            self.flip = True

        #stay on screen
        if self.rect.left + dir_x < 0:
            dir_x = -self.rect.left
        if self.rect.right + dir_x > screen_width:
            dir_x = screen_width - self.rect.right

        #jumping
        self.vel_y += self.gravity
        dir_y += self.vel_y

        #check collision with platforms
        for plat in platform_group:
            # collision in the y direction
            if plat.rect.colliderect(self.rect.x, self.rect.y + dir_y, self.width, self.height):
                # check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = plat.rect.top - 40
                        dir_y = 0
                        self.vel_y = -20

        #check collision with platforms
        for star in star_group:
            # collision in the y direction
            if star.rect.colliderect(self.rect.x, self.rect.y, self.width, self.height):
                self.score += 1
                star.kill()



        # check if player has bounced to scroll palce
        if self.rect.top <= 200:
            # print(self.rect.top)
            if self.vel_y < 0:
                self.scroll = -dir_y

        self.rect.x += dir_x
        self.rect.y += dir_y + self.scroll

        return self.scroll


    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 5))

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > screen_height:
            self.kill()

class Stars(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(star_img, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > screen_height:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.surface = pygame.display.get_surface()
        self.clicked = False

    def click(self):
        action = False
        # mouse pos
        pos = pygame.mouse.get_pos()

        #check mouseover and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        self.surface.blit(self.image, (self.rect.x, self.rect.y))\

        return action

def reset_variables(player):
    game_over = False
    player.scroll = 0
    player.score = 0
    player.rect.center = (400, 650)
    platform_group.empty()
    platform = Platform(screen_width // 2 - 50, screen_height - 25, 175)
    platform_group.add(platform)

def draw_text(text, font, color, x, y):
    txt = font.render(text, True, color)
    screen.blit(txt, (x,y))

def draw_info(score):
    draw_text('Stars  Collected   ' + str(score), pixel_font, (255,255,255), 0, 0)

def draw_bg(scroll):
    screen.blit(background_img, (0,0 + bg_scroll))

# game intialization
# generate start platform
platform_group = pygame.sprite.Group()
platform = Platform(screen_width // 2 - 75, screen_height - 25, 175)
platform_group.add(platform)

star_group = pygame.sprite.Group()

player = Player(400, 610)
game_over = False
bg_scroll = 0
def game(game_over, bg_scroll, player):
    run = True
    reset_variables(player)
    while run:
        screen.fill('white')
        scroll = player.move()
        bg_scroll += scroll
        draw_bg(bg_scroll)


        if game_over == False:

            # generate platform
            if len(platform_group) < 8:
                rand_pw = random.randint(150, 250)
                rand_px = random.randint(0, screen_width - rand_pw)
                rand_py = platform_group.sprites()[-1].rect.y - random.randint(150, 200)
                platform = Platform(rand_px, rand_py, rand_pw)
                platform_group.add(platform)
            platform_group.update(scroll)
            platform_group.draw(screen)

            if len(star_group) < 2:
                rand_sx = random.randint(0, screen_width - 10)
                rand_sy = random.randint(0, 250)
                star = Stars(rand_sx, rand_sy)
                star_group.add(star)
            star_group.update(scroll)
            star_group.draw(screen)

            player.draw()

            draw_info(player.score)

            # game over !
            if player.rect.top > screen_height:
                game_over = True

        else:
            reset_variables(player)
            reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause(game_over, bg_scroll)

        pygame.display.update()
        clock.tick(60)

def pause(game_over, bg_scroll):
    click = False

    pause_img = pygame.image.load('graphics/pause.png')
    start_img = pygame.image.load('graphics/play.png')
    quit_img = pygame.image.load('graphics/quit.png')

    resume = Button(170, 325, start_img)
    quit_button = Button(170, 500, quit_img)

    while True:

        screen.blit(pause_img, (0, 0))

        if resume.click():
            game(game_over, bg_scroll)

        if quit_button.click():
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()
        clock.tick(60)


def reset():
    click = False

    death_img = pygame.image.load('graphics/gameover.png')
    start_img = pygame.image.load('graphics/play.png')
    quit_img = pygame.image.load('graphics/quit.png')

    resume = Button(170, 325, start_img)
    quit_button = Button(170, 500, quit_img)

    while True:

        screen.blit(death_img, (0, 0))

        if resume.click():
            game(game_over, bg_scroll, player)
        if quit_button.click():
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True


        pygame.display.update()
        clock.tick(60)

def menu():
    click = False
    keys = pygame.key.get_pressed()

    menu_img = pygame.image.load('graphics/menu.png')
    start_img = pygame.image.load('graphics/play.png')
    quit_img = pygame.image.load('graphics/quit.png')

    start = Button(170, 325, start_img)

    while True:

        screen.blit(menu_img, (0, 0))
        if start.click():
            game(game_over, bg_scroll, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)

menu()