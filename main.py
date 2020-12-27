import pygame, sys, random
import pygame.freetype

class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ch.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound("gs.wav")
    def shoot(self):
        self.gunshot.play()
        pygame.sprite.spritecollide(crosshair, target_group, True)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.leftwards = False
        self.rightwards = False
        self.upwards = False
        self.downwards = False
        self.new_x = 0
        self.new_y = 0
        self.image = pygame.image.load("al.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.new_x = pos_x
        self.new_y = pos_y
        if pos_x > screen_width/2:
            self.leftwards = True
        else:
            self.rightwards = True
        if pos_y > screen_height/2:
            self.upwards = True
        else:
            self.downwards = True
    def update(self):
        if self.new_x >= (screen_width - 50):
            self.leftwards = True
            self.rightwards = False
        if self.new_x <= 50:
            self.rightwards = True
            self.leftwards = False
        if self.new_y >= (screen_height - 50):
            self.upwards = True
            self.downwards = False
        if self.new_y <= 50:
            self.downwards = True
            self.upwards = False
        if self.leftwards:
            self.new_x -= 10
        if self.rightwards:
            self.new_x += 10
        if self.upwards:
            self.new_y -= 10
        if self.downwards:
            self.new_y += 10
        self.image = pygame.image.load("al.png").convert_alpha()
        self.rect.center = [self.new_x, self.new_y]

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 100)

screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load("hoc.png").convert_alpha()
pygame.mouse.set_visible(False)

crosshair = Crosshair()
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group = pygame.sprite.Group()

for target in range(20):
    new_target = Target(random.randrange(0, screen_width), random.randrange(0, screen_height))
    target_group.add(new_target)


def rotate(surface, degree):
    rotated_surface = pygame.transform.rotozoom(surface, degree, 1)
    rotated_rect = rotated_surface.get_rect(center=(screen_width/2, (screen_height/2) + 20))
    return rotated_surface, rotated_rect

def title_screen():
    pygame.mouse.set_visible(True)
    big_al = pygame.image.load("big_al.png").convert_alpha()
    al = pygame.transform.scale(big_al, (1200, 800))
    angle = 0
    title_font = pygame.font.SysFont('Comic Sans MS', 200)
    title_surface = title_font.render('Parliament of Fools', False, (255, 255, 255))
    small_font = pygame.font.SysFont('Comic Sans MS', 50)
    small_font_surface = small_font.render('Press any key to play', False, (255, 255, 255))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                running = False

        angle += 1
        screen.fill((0, 0, 0))
        screen.blit(title_surface, (200, 50))
        screen.blit(small_font_surface, (750, 950))
        al_rotated, al_rotated_rect = rotate(al, angle)
        screen.blit(al_rotated, al_rotated_rect)
        pygame.display.flip()
        clock.tick(30)


def stats(remaining):
    text_surface = font.render('Remaining ' + str(remaining), False, (255, 255, 255))
    screen.blit(text_surface, (0, 0))

def game_loop():
    pygame.mixer.music.load("pof.wav")
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()

        pygame.display.flip()
        screen.blit(background, (0, 0))
        target_group.draw(screen)
        target_group.update()
        score = len(target_group.sprites())
        stats(score)
        if score == 0:
            running = False
        crosshair_group.draw(screen)
        crosshair_group.update()
        clock.tick(60)

def end_screen():
    clock.tick(100)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('success.wav')
    pygame.mixer.music.play(0)

    pygame.mouse.set_visible(True)
    title_font = pygame.font.SysFont('Comic Sans MS', 200)
    title_surface = title_font.render('Thanks for playing!', False, (255, 255, 255))
    small_font = pygame.font.SysFont('Comic Sans MS', 50)
    small_font_surface = small_font.render('Please come back again.', False, (255, 255, 255))

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or e.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()


        screen.fill((0, 0, 0))
        screen.blit(title_surface, ((screen_width/2) - 650, (screen_height/2) - 200))
        screen.blit(small_font_surface, (750, 950))
        pygame.display.flip()



title_screen()
game_loop()
end_screen()