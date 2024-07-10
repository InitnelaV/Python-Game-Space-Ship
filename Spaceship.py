import pygame
import sys
pygame.init()

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 40
cactus_img = pygame.image.load('acier.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('fire_acier.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()

font = pygame.font.SysFont('font', 30)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('SpaceShip')
# background image


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Antagonist:
    antagonist_velocity = 20

    def __init__(self):
        self.antagonist_img = pygame.image.load('antagonist.png')
        self.antagonist_img_rect = self.antagonist_img.get_rect()
        self.antagonist_img_rect.width -= 10
        self.antagonist_img_rect.height -= 10
        self.antagonist_img_rect.top = WINDOW_HEIGHT / 2
        self.antagonist_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.antagonist_img, self.antagonist_img_rect)
        if self.antagonist_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.antagonist_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.antagonist_img_rect.top -= self.antagonist_velocity
        elif self.down:
            self.antagonist_img_rect.top += self.antagonist_velocity


class Flames:
    flames_velocity = 30

    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (30, 30))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = antagonist.antagonist_img_rect.left
        self.flames_img_rect.top = antagonist.antagonist_img_rect.top + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity
###
class Flames_2:
    flames_velocity = 10

    def __init__(self):
        self.flames_2 = pygame.image.load('fireball.png')
        self.flames_2_img = pygame.transform.scale(self.flames, (30, 30))
        self.flames_2_img_rect = self.flames_img.get_rect()
        self.flames_2_img_rect.right = antagonist.antagonist_img_rect.left
        self.flames_2_img_rect.bottom = antagonist.antagonist_img_rect.bottom + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_2_img_rect.left > 0:
            self.flames_2_img_rect.left -= self.flames_velocity
###
class Protagonist:
    velocity = 10

    def __init__(self):
        self.protagonist_img = pygame.image.load('protagonist.png')
        self.protagonist_img_rect = self.protagonist_img.get_rect()
        self.protagonist_img_rect.left = 20
        self.protagonist_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.protagonist_img, self.protagonist_img_rect)
        if self.protagonist_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.protagonist_score:
                self.protagonist_score = SCORE
        if self.protagonist_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.protagonist_score:
                self.protagonist_score = SCORE
        if self.up:
            self.protagonist_img_rect.top -= 10
        if self.down:
            self.protagonist_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('Kaboom.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE in range(30, 40):
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4
    elif SCORE > 40:
        cactus_img_rect.bottom = 250
        fire_img_rect.top = WINDOW_HEIGHT - 250
        LEVEL = 5

def game_loop():
    while True:
        global antagonist
        antagonist = Antagonist()
        flames = Flames()
        protagonist = Protagonist()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('spacesong.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            antagonist.update()
            add_new_flame_counter += 2

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        protagonist.up = True
                        protagonist.down = False
                    elif event.key == pygame.K_DOWN:
                        protagonist.down = True
                        protagonist.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        protagonist.up = False
                        protagonist.down = True
                    elif event.key == pygame.K_DOWN:
                        protagonist.down = True
                        protagonist.up = False

            score_font = font.render('Score:'+str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            protagonist.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(protagonist.protagonist_img_rect):
                    game_over()
                    if SCORE > protagonist.protagonist_score:
                        protagonist.protagonist_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()


